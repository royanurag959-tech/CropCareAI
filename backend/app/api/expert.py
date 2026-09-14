import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User, ExpertRequest, ScanHistory
from app.schemas.schemas import ExpertCreateRequest, ExpertResolveRequest
from app.api.auth import get_optional_current_user

router = APIRouter(prefix="/expert", tags=["Expert Consultation"])

@router.post("/request")
def create_expert_request(
    payload: ExpertCreateRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Farmer or Extension Worker submits a case dossier for 1-on-1 Agronomist triage.
    Escalated automatically on low confidence, high severity, critical risk score, or worsening trend.
    """
    user_id = current_user.id if current_user else 1
    farmer_name = current_user.name if current_user else "Farmer"
    farmer_phone = payload.farmer_phone or (current_user.phone if current_user else "9876543210")

    dossier_json = None
    if payload.dossier_data:
        dossier_json = json.dumps(payload.dossier_data)
    elif payload.scan_id:
        scan = db.query(ScanHistory).filter(ScanHistory.id == payload.scan_id).first()
        if scan:
            dossier_dict = {
                "crop": scan.crop,
                "predicted_disease": scan.predicted_disease,
                "confidence_percentage": int(round(scan.confidence * 100)),
                "confidence_level": scan.confidence_level or "medium",
                "risk_score": scan.risk_score or 50,
                "risk_category": scan.risk_category or "Moderate Risk",
                "image_url": scan.image_url,
                "farmer_info": {"name": farmer_name, "phone": farmer_phone},
                "farmer_answers": json.loads(scan.follow_up_data) if scan.follow_up_data else {},
                "weather_conditions": json.loads(scan.farm_conditions_summary) if scan.farm_conditions_summary else {},
                "farmer_question": payload.farmer_question or "What immediate steps should I take to prevent this from spreading?"
            }
            dossier_json = json.dumps(dossier_dict)

    req = ExpertRequest(
        user_id=user_id,
        scan_id=payload.scan_id,
        farmer_name=farmer_name,
        farmer_phone=farmer_phone,
        farmer_notes=payload.farmer_notes or "Farmer requested agronomy review for crop condition.",
        farmer_question=payload.farmer_question or "Please examine this crop scan and advise on treatment.",
        dossier_data=dossier_json,
        status="pending",
        fee=99.0,
        platform_fee=19.8
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    return {
        "success": True,
        "request_id": req.id,
        "status": req.status,
        "consultation_fee_inr": req.fee,
        "platform_share_inr": req.platform_fee,
        "expert_share_inr": round(req.fee - req.platform_fee, 2),
        "message": "Consultation request queued. An agricultural specialist will review your complete case dossier and contact you shortly."
    }

@router.get("/requests")
def get_expert_requests(
    status: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ExpertRequest)
    if status:
        query = query.filter(ExpertRequest.status == status)
    
    requests = query.order_by(ExpertRequest.created_at.desc()).all()
    results = []
    for r in requests:
        scan_info = None
        if r.scan:
            scan_info = {
                "crop": r.scan.crop,
                "predicted_disease": r.scan.predicted_disease,
                "confidence": r.scan.confidence,
                "severity": r.scan.severity,
                "risk_score": r.scan.risk_score,
                "risk_category": r.scan.risk_category,
                "image_url": r.scan.image_url
            }

        dossier_parsed = None
        if r.dossier_data:
            try:
                dossier_parsed = json.loads(r.dossier_data)
            except Exception:
                dossier_parsed = None

        results.append({
            "id": r.id,
            "farmer_name": r.farmer_name,
            "farmer_phone": r.farmer_phone,
            "farmer_notes": r.farmer_notes,
            "farmer_question": r.farmer_question,
            "status": r.status,
            "fee": r.fee,
            "expert_notes": r.expert_notes,
            "scan": scan_info,
            "dossier": dossier_parsed,
            "created_at": r.created_at.isoformat() if r.created_at else ""
        })
    return results

@router.post("/resolve/{request_id}")
def resolve_expert_request(
    request_id: int,
    payload: ExpertResolveRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    req = db.query(ExpertRequest).filter(ExpertRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Consultation request not found")

    req.status = "resolved"
    req.expert_notes = payload.expert_notes
    if current_user and current_user.role == "expert":
        req.expert_id = current_user.id

    db.commit()
    return {
        "success": True,
        "request_id": req.id,
        "status": req.status,
        "expert_notes": req.expert_notes,
        "message": "Consultation case resolved successfully. Recommendations dispatched to farmer."
    }
