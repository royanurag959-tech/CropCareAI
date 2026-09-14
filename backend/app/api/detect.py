import os
import io
import json
import uuid
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from PIL import Image

from app.database.session import get_db
from app.database.models import User, ScanHistory
from app.schemas.schemas import DetectionResponse
from app.api.auth import get_optional_current_user
from app.ai.factory import get_inference_engine
from app.weather.factory import get_weather_provider
from app.services.risk_scoring import CropRiskScoringEngine
from app.services.escalation import ExpertEscalationEvaluator
from app.services.progress_tracking import DiseaseProgressTracker
from app.ai.explainability import ExplainableAIEngine
from app.services.advisory import AdvisoryService
from app.core.config import settings

router = APIRouter(prefix="/detect", tags=["Disease Detection"])

ALLOWED_IMAGE_MIMES = ["image/jpeg", "image/png", "image/webp", "image/bmp", "image/jpg"]
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".bmp"]

@router.post("", response_model=DetectionResponse)
async def detect_crop_disease(
    crop: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_sample_name: Optional[str] = Form(None),
    growth_stage: Optional[str] = Form("Vegetative"),
    crop_age: Optional[str] = Form(None),
    rainfall: Optional[str] = Form("Moderate"),
    irrigation: Optional[str] = Form("Every 2-3 days"),
    drainage: Optional[str] = Form("Good"),
    duration: Optional[str] = Form("4-7 days"),
    affected_area: Optional[str] = Form("10-30%"),
    location: Optional[str] = Form("Pune District"),
    plot_id: Optional[str] = Form(None),
    farmer_notes: Optional[str] = Form(None),
    farmer_name: Optional[str] = Form(None),
    farmer_phone: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    # 1. Quota Check for registered users
    if current_user:
        limit = settings.FREE_TIER_MONTHLY_LIMIT
        if current_user.subscription_plan == "plus":
            limit = settings.PLUS_TIER_MONTHLY_LIMIT
        elif current_user.subscription_plan == "pro":
            limit = settings.PRO_TIER_MONTHLY_LIMIT

        if current_user.scan_count_month >= limit:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Monthly scan limit ({limit} scans) reached for your {current_user.subscription_plan.upper()} plan. Please upgrade to continue scans."
            )

    # 2. Extract and Validate image bytes
    filename = ""
    saved_image_url = None
    image_bytes = None

    if image and image.filename:
        filename = image.filename
        ext = os.path.splitext(filename)[1].lower()

        # Pre-processing validation: Content-Type & Extension
        if image.content_type and image.content_type not in ALLOWED_IMAGE_MIMES and not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image type '{image.content_type}'. Please upload a valid JPG, PNG, or WEBP photo."
            )
        if ext and ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file extension '{ext}'. Only JPG, PNG, and WEBP images are supported."
            )

        image_bytes = await image.read()

        # Pre-processing validation: File size (max 10MB, non-zero)
        if not image_bytes or len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty (0 bytes).")
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image file exceeds the 10MB maximum limit.")

        # Pre-processing validation: Pillow header and dimension check
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            pil_img.verify()
            # Reopen to read dimensions after verify
            pil_img = Image.open(io.BytesIO(image_bytes))
            w, h = pil_img.size
            if w < 50 or h < 50:
                raise HTTPException(
                    status_code=400,
                    detail=f"Image resolution too low ({w}x{h}px). Minimum 50x50px required for foliar disease pattern recognition."
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid or corrupted image file: {str(e)}")

        # Save locally
        unique_name = f"{uuid.uuid4().hex[:8]}_{filename}"
        local_path = os.path.join(settings.STORAGE_DIR, unique_name)
        try:
            with open(local_path, "wb") as f:
                f.write(image_bytes)
            saved_image_url = f"/uploaded_scans/{unique_name}"
        except Exception:
            saved_image_url = f"/sample_leaves/{filename}"

    elif image_sample_name:
        filename = image_sample_name
        saved_image_url = f"/sample_leaves/{image_sample_name}"
        sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_leaves", image_sample_name)
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()
        else:
            buf = io.BytesIO()
            Image.new("RGB", (100, 100), color=(40, 120, 40)).save(buf, "JPEG")
            image_bytes = buf.getvalue()
    else:
        # Default sample image fallback
        filename = f"sample_{crop.lower()}_scan.jpg"
        saved_image_url = f"/sample_leaves/{filename}"
        buf = io.BytesIO()
        Image.new("RGB", (100, 100), color=(40, 120, 40)).save(buf, "JPEG")
        image_bytes = buf.getvalue()

    # 3. Context dictionary
    context = {
        "growth_stage": growth_stage or "Vegetative",
        "crop_age": crop_age or "Not specified",
        "rainfall": rainfall or "Moderate",
        "irrigation": irrigation or "Every 2-3 days",
        "drainage": drainage or "Good",
        "duration": duration or "4-7 days",
        "affected_area": affected_area or "10-30%",
        "location": location or "Pune District",
        "plot_id": plot_id,
        "farmer_notes": farmer_notes
    }

    # 4. Modular Weather Provider
    weather_provider = get_weather_provider()
    weather_data = weather_provider.get_weather(location=context["location"], context=context)

    # 5. Modular AI Inference Engine
    inference_engine = get_inference_engine()
    ai_result = inference_engine.predict(
        image_bytes=image_bytes,
        crop_name=crop,
        filename=filename,
        context=context
    )

    # 6. Configurable Crop Risk Score Engine (0-100)
    risk_assessment = CropRiskScoringEngine.calculate_risk_score(
        severity=ai_result["severity"],
        confidence=ai_result["confidence"],
        weather=weather_data,
        context={**context, "predicted_disease": ai_result["predicted_disease"]}
    )

    # 7. Disease Progress Tracking (Timeline comparison)
    effective_plot_id = plot_id or f"plot_{crop.lower()}_{current_user.id if current_user else 'guest'}"
    historical_scans_query = db.query(ScanHistory).filter(
        (ScanHistory.plot_id == effective_plot_id) |
        ((ScanHistory.crop.ilike(crop)) & (ScanHistory.user_id == (current_user.id if current_user else None)))
    ).order_by(ScanHistory.created_at.desc()).limit(10).all()

    historical_scans = [
        {
            "id": s.id,
            "risk_score": s.risk_score or 50,
            "confidence": s.confidence,
            "severity": s.severity,
            "predicted_disease": s.predicted_disease,
            "created_at": s.created_at.isoformat() if s.created_at else ""
        }
        for s in historical_scans_query
    ]

    current_scan_dict = {
        "risk_score": risk_assessment["score"],
        "confidence": ai_result["confidence"],
        "severity": ai_result["severity"],
        "predicted_disease": ai_result["predicted_disease"]
    }
    progress_result = DiseaseProgressTracker.evaluate_progression(current_scan_dict, historical_scans)

    # 8. Automated Expert Escalation Evaluator
    escalation_result = ExpertEscalationEvaluator.evaluate(
        confidence=ai_result["confidence"],
        severity=ai_result["severity"],
        risk_score=risk_assessment["score"],
        trend=progress_result["trend"],
        manual_request=False
    )

    # 9. Explainable AI Engine ("Why Did This Happen?")
    explainability = ExplainableAIEngine.generate_explanation(
        disease_name=ai_result["predicted_disease"],
        crop_name=crop,
        context=context,
        weather=weather_data
    )

    # 10. Structured Advisory & Time-Phased Action Plan
    advisory = AdvisoryService.get_advisory_for_disease(
        db=db,
        crop_name=crop,
        predicted_disease=ai_result["predicted_disease"]
    )
    action_plan = AdvisoryService.get_time_phased_action_plan(
        disease_name=ai_result["predicted_disease"],
        crop_name=crop,
        severity=ai_result["severity"],
        risk_category=risk_assessment["category"],
        context=context
    )

    # 11. Record Scan in Database
    new_scan = ScanHistory(
        user_id=current_user.id if current_user else None,
        farmer_name=farmer_name or (current_user.name if current_user else "Guest Farmer"),
        farmer_phone=farmer_phone or (current_user.phone if current_user else None),
        crop=crop,
        image_url=saved_image_url,
        predicted_disease=ai_result["predicted_disease"],
        confidence=ai_result["confidence"],
        confidence_level=ai_result.get("confidence_level", "high"),
        severity=ai_result["severity"],
        is_uncertain=ai_result.get("is_uncertain", False),
        plot_id=effective_plot_id,
        risk_score=risk_assessment["score"],
        risk_category=risk_assessment["category"],
        trend=progress_result["trend"],
        farmer_notes=farmer_notes,
        short_explanation=ai_result.get("short_explanation"),
        follow_up_data=json.dumps(context),
        farm_conditions_summary=json.dumps(explainability.get("farm_conditions", {})),
        generated_explanation=explainability["primary_summary"],
        symptoms_summary=json.dumps(advisory["symptoms"]),
        immediate_actions_summary=json.dumps(advisory["immediate_actions"]),
        prevention_summary=json.dumps(advisory["prevention"]),
        district=context["location"],
        is_synced=True
    )
    db.add(new_scan)

    if current_user:
        current_user.scan_count_month += 1

    db.commit()
    db.refresh(new_scan)

    confidence_pct = int(round(ai_result["confidence"] * 100))

    return {
        "crop": crop,
        "crop_hindi": ai_result.get("crop_hindi", crop),
        "predicted_disease": ai_result["predicted_disease"],
        "hindi_name": advisory["hindi_name"],
        "scientific_name": advisory.get("scientific_name"),
        "confidence": ai_result["confidence"],
        "confidence_percentage": confidence_pct,
        "confidence_level": ai_result.get("confidence_level", "high"),
        "confidence_level_label": ai_result.get("confidence_level_label", "High Confidence"),
        "confidence_level_label_hindi": ai_result.get("confidence_level_label_hindi", "उच्च विश्वास"),
        "severity": ai_result["severity"],
        "is_uncertain": ai_result.get("is_uncertain", False),
        "uncertainty_message": ai_result.get("uncertainty_message"),
        "short_explanation": ai_result.get("short_explanation", ""),
        "short_explanation_hindi": ai_result.get("short_explanation_hindi", ""),
        "provider_name": ai_result.get("provider_name", "MockInferenceProvider"),
        "risk_score": risk_assessment,
        "weather": weather_data,
        "farm_conditions": explainability.get("farm_conditions"),
        "action_plan": action_plan,
        "progress_tracking": progress_result,
        "escalation": escalation_result,
        "why_did_it_happen": explainability,
        "symptoms": advisory["symptoms"],
        "possible_causes": advisory["possible_causes"],
        "immediate_actions": advisory["immediate_actions"],
        "general_management": advisory["general_management"],
        "prevention": advisory["prevention"],
        "when_to_contact_expert": advisory.get("when_to_contact_expert"),
        "scan_id": new_scan.id,
        "image_url": saved_image_url,
        "disclaimer": advisory["disclaimer"]
    }
