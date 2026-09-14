import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User, ScanHistory
from app.schemas.schemas import ScanHistoryItem, SyncBatchRequest
from app.api.auth import get_optional_current_user
from app.services.sync_service import SyncService
from app.services.progress_tracking import DiseaseProgressTracker

router = APIRouter(prefix="/scans", tags=["Scan History & Reports"])

@router.get("", response_model=List[ScanHistoryItem])
def get_user_scans(
    crop: Optional[str] = None,
    plot_id: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(ScanHistory)
    
    if current_user:
        if current_user.role in ["worker", "admin", "b2b_org"]:
            pass  # Extension workers & orgs can see regional scans
        else:
            query = query.filter(ScanHistory.user_id == current_user.id)
    else:
        # Default guest/public recent demo scans
        query = query.limit(20)

    if crop:
        query = query.filter(ScanHistory.crop.ilike(f"%{crop}%"))

    if plot_id:
        query = query.filter(ScanHistory.plot_id == plot_id)

    scans = query.order_by(ScanHistory.created_at.desc()).all()
    
    return [
        {
            "id": s.id,
            "crop": s.crop,
            "predicted_disease": s.predicted_disease,
            "confidence": s.confidence,
            "confidence_level": s.confidence_level or ("high" if s.confidence >= 0.90 else ("medium" if s.confidence >= 0.60 else "low")),
            "severity": s.severity,
            "is_uncertain": s.is_uncertain if s.is_uncertain is not None else (s.confidence < 0.60),
            "risk_score": s.risk_score,
            "risk_category": s.risk_category or "Moderate Risk",
            "trend": s.trend or "Stable",
            "plot_id": s.plot_id,
            "image_url": s.image_url,
            "short_explanation": s.short_explanation or s.generated_explanation,
            "farmer_notes": s.farmer_notes,
            "generated_explanation": s.generated_explanation,
            "farmer_name": s.farmer_name,
            "farmer_phone": s.farmer_phone,
            "district": s.district,
            "created_at": s.created_at.isoformat() if s.created_at else ""
        }
        for s in scans
    ]

@router.get("/timeline")
def get_crop_monitoring_timeline(
    crop: Optional[str] = Query("Tomato"),
    plot_id: Optional[str] = None,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Returns the chronological monitoring timeline for a crop or plot,
    evaluating disease progression trend across repeat scans.
    """
    query = db.query(ScanHistory)
    if plot_id:
        query = query.filter(ScanHistory.plot_id == plot_id)
    elif crop:
        query = query.filter(ScanHistory.crop.ilike(f"%{crop}%"))

    if current_user and current_user.role not in ["worker", "admin", "b2b_org"]:
        query = query.filter(ScanHistory.user_id == current_user.id)

    records = query.order_by(ScanHistory.created_at.asc()).all()

    timeline = [
        {
            "id": r.id,
            "crop": r.crop,
            "predicted_disease": r.predicted_disease,
            "confidence": r.confidence,
            "confidence_percentage": int(round(r.confidence * 100)),
            "severity": r.severity,
            "risk_score": r.risk_score or 50,
            "risk_category": r.risk_category or "Moderate Risk",
            "image_url": r.image_url,
            "farmer_notes": r.farmer_notes,
            "created_at": r.created_at.isoformat() if r.created_at else ""
        }
        for r in records
    ]

    if len(timeline) >= 2:
        current_entry = timeline[-1]
        history_entries = list(reversed(timeline[:-1]))
        progression = DiseaseProgressTracker.evaluate_progression(current_entry, history_entries)
    else:
        progression = {
            "trend": "Uncertain",
            "trend_hindi": "प्रारंभिक स्कैन",
            "trend_description": "First monitoring scan recorded. Re-scan in 3-5 days to track trend.",
            "trend_description_hindi": "पहला बेसलाइन स्कैन। प्रगति जानने के लिए 3-5 दिनों बाद दोबारा स्कैन करें।",
            "previous_risk_score": None,
            "current_risk_score": timeline[0]["risk_score"] if timeline else 50,
            "risk_delta": 0,
            "recommend_expert_escalation": False,
            "total_historical_records": len(timeline)
        }

    return {
        "crop": crop,
        "plot_id": plot_id or f"plot_{crop.lower()}",
        "total_scans": len(timeline),
        "progression": progression,
        "timeline": timeline
    }

@router.get("/{scan_id}")
def get_scan_report(
    scan_id: int,
    db: Session = Depends(get_db)
):
    scan = db.query(ScanHistory).filter(ScanHistory.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found")

    return {
        "id": scan.id,
        "crop": scan.crop,
        "predicted_disease": scan.predicted_disease,
        "confidence": scan.confidence,
        "confidence_level": scan.confidence_level or "high",
        "severity": scan.severity,
        "is_uncertain": scan.is_uncertain if scan.is_uncertain is not None else False,
        "risk_score": scan.risk_score,
        "risk_category": scan.risk_category,
        "trend": scan.trend,
        "plot_id": scan.plot_id,
        "farmer_notes": scan.farmer_notes,
        "short_explanation": scan.short_explanation,
        "image_url": scan.image_url,
        "follow_up_data": json.loads(scan.follow_up_data) if scan.follow_up_data else {},
        "farm_conditions": json.loads(scan.farm_conditions_summary) if scan.farm_conditions_summary else {},
        "generated_explanation": scan.generated_explanation,
        "symptoms": json.loads(scan.symptoms_summary) if scan.symptoms_summary else [],
        "immediate_actions": json.loads(scan.immediate_actions_summary) if scan.immediate_actions_summary else [],
        "prevention": json.loads(scan.prevention_summary) if scan.prevention_summary else [],
        "farmer_name": scan.farmer_name,
        "farmer_phone": scan.farmer_phone,
        "district": scan.district,
        "created_at": scan.created_at.isoformat() if scan.created_at else ""
    }

@router.post("/sync")
def sync_offline_scans(
    payload: SyncBatchRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Ingests scans captured offline by the PWA client once internet returns.
    """
    return SyncService.sync_offline_scans(db=db, user=current_user, scans=payload.scans)
