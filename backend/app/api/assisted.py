import os
import io
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, Form, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from PIL import Image

from app.database.session import get_db
from app.database.models import User, ScanHistory
from app.api.auth import get_optional_current_user
from app.ai.factory import get_inference_engine
from app.weather.factory import get_weather_provider
from app.services.risk_scoring import CropRiskScoringEngine
from app.ai.explainability import ExplainableAIEngine
from app.services.advisory import AdvisoryService

router = APIRouter(prefix="/assisted", tags=["Assisted Diagnosis (Krishi Mitra)"])

@router.post("/diagnose")
async def assisted_diagnosis_by_worker(
    farmer_name: str = Form(...),
    farmer_phone: str = Form(...),
    village: str = Form(...),
    crop: str = Form(...),
    image: Optional[UploadFile] = File(None),
    image_sample_name: Optional[str] = Form(None),
    growth_stage: Optional[str] = Form("Vegetative"),
    crop_age: Optional[str] = Form("1-2 months"),
    rainfall: Optional[str] = Form("Moderate"),
    irrigation: Optional[str] = Form("Every 2-3 days"),
    drainage: Optional[str] = Form("Good"),
    duration: Optional[str] = Form("3-5 days"),
    affected_area: Optional[str] = Form("10-30%"),
    farmer_notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    Extension Worker / Krishi Mitra workflow:
    Worker captures photo on their device on behalf of a smallholder farmer without a smartphone.
    Associates the diagnosis and risk assessment directly with the farmer's mobile phone,
    storing the record in ScanHistory and generating a printable paper and SMS receipt.
    """
    filename = image_sample_name or (image.filename if image else "assisted_scan.jpg")
    
    if image and image.filename:
        filename = image.filename
        image_bytes = await image.read()
    elif image_sample_name:
        filename = image_sample_name
        sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_leaves", image_sample_name)
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                image_bytes = f.read()
        else:
            buf = io.BytesIO()
            Image.new("RGB", (100, 100), color=(40, 120, 40)).save(buf, "JPEG")
            image_bytes = buf.getvalue()
    else:
        buf = io.BytesIO()
        Image.new("RGB", (100, 100), color=(40, 120, 40)).save(buf, "JPEG")
        image_bytes = buf.getvalue()

    context = {
        "growth_stage": growth_stage,
        "crop_age": crop_age,
        "rainfall": rainfall,
        "irrigation": irrigation,
        "drainage": drainage,
        "duration": duration,
        "affected_area": affected_area,
        "location": village,
        "farmer_notes": farmer_notes
    }

    # 1. Weather Data
    weather = get_weather_provider().get_weather(village, context)

    # 2. AI Inference
    inference_engine = get_inference_engine()
    ai_result = inference_engine.predict(
        image_bytes=image_bytes,
        crop_name=crop,
        filename=filename,
        context=context
    )

    # 3. Risk Scoring
    risk_assessment = CropRiskScoringEngine.calculate_risk_score(
        severity=ai_result["severity"],
        confidence=ai_result["confidence"],
        weather=weather,
        context={**context, "predicted_disease": ai_result["predicted_disease"]}
    )

    # 4. Explainable AI
    explainability = ExplainableAIEngine.generate_explanation(
        disease_name=ai_result["predicted_disease"],
        crop_name=crop,
        context=context,
        weather=weather
    )

    # 5. Structured Advisory & Action Plan
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

    # 6. Save record attributing to worker and linking to farmer
    worker_id = current_user.id if current_user else 2  # default Krishi Mitra ID
    scan = ScanHistory(
        user_id=worker_id,
        farmer_name=farmer_name,
        farmer_phone=farmer_phone,
        crop=crop,
        image_url=f"/sample_leaves/{filename}",
        predicted_disease=ai_result["predicted_disease"],
        confidence=ai_result["confidence"],
        confidence_level=ai_result.get("confidence_level", "high"),
        severity=ai_result["severity"],
        is_uncertain=ai_result.get("is_uncertain", False),
        risk_score=risk_assessment["score"],
        risk_category=risk_assessment["category"],
        plot_id=f"assisted_{farmer_phone}",
        farmer_notes=farmer_notes,
        short_explanation=ai_result.get("short_explanation"),
        follow_up_data=json.dumps(context),
        farm_conditions_summary=json.dumps(explainability.get("farm_conditions", {})),
        generated_explanation=explainability["primary_summary"],
        symptoms_summary=json.dumps(advisory["symptoms"]),
        immediate_actions_summary=json.dumps(advisory["immediate_actions"]),
        prevention_summary=json.dumps(advisory["prevention"]),
        district=village,
        is_synced=True
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # 7. Generate printable & SMS farmer receipt
    sms_receipt = (
        f"🌱 CropCare AI Receipt #{scan.id}\n"
        f"Farmer: {farmer_name} ({village})\n"
        f"Crop: {crop} | Diagnosis: {ai_result['predicted_disease']} ({int(ai_result['confidence']*100)}%)\n"
        f"Risk Score: {risk_assessment['score']}/100 ({risk_assessment['category']})\n"
        f"Today's Action: {action_plan['today'][0]}\n"
        f"Helpline: 1800-180-1551"
    )

    return {
        "success": True,
        "scan_id": scan.id,
        "farmer_name": farmer_name,
        "farmer_phone": farmer_phone,
        "village": village,
        "crop": crop,
        "predicted_disease": ai_result["predicted_disease"],
        "hindi_name": advisory["hindi_name"],
        "confidence": ai_result["confidence"],
        "confidence_percentage": int(round(ai_result["confidence"] * 100)),
        "confidence_level": ai_result.get("confidence_level", "high"),
        "severity": ai_result["severity"],
        "is_uncertain": ai_result.get("is_uncertain", False),
        "risk_score": risk_assessment,
        "action_plan": action_plan,
        "why_did_it_happen": explainability,
        "sms_receipt": sms_receipt,
        "worker_name": current_user.name if current_user else "Krishi Mitra Center"
    }
