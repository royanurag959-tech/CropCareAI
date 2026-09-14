import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.database.models import User, Subscription, PricingConfig
from app.schemas.schemas import PricingPlanItem, UpgradePlanRequest
from app.api.auth import get_current_user, get_optional_current_user
from app.services.payment_mock import MockPaymentService
from app.core.config import settings

router = APIRouter(prefix="/subscription", tags=["Subscriptions & Monetization"])

@router.get("")
def get_user_subscription(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        return {
            "plan": "free",
            "scan_count_month": 0,
            "scan_limit": settings.FREE_TIER_MONTHLY_LIMIT,
            "remaining_scans": settings.FREE_TIER_MONTHLY_LIMIT,
            "is_logged_in": False
        }

    limit = settings.FREE_TIER_MONTHLY_LIMIT
    if current_user.subscription_plan == "plus":
        limit = settings.PLUS_TIER_MONTHLY_LIMIT
    elif current_user.subscription_plan == "pro":
        limit = settings.PRO_TIER_MONTHLY_LIMIT

    active_sub = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()

    return {
        "user_id": current_user.id,
        "name": current_user.name,
        "plan": current_user.subscription_plan,
        "scan_count_month": current_user.scan_count_month,
        "scan_limit": limit,
        "remaining_scans": max(0, limit - current_user.scan_count_month),
        "end_date": active_sub.end_date.isoformat() if active_sub and active_sub.end_date else None,
        "is_logged_in": True
    }

@router.get("/pricing", response_model=List[PricingPlanItem])
def get_pricing_plans(db: Session = Depends(get_db)):
    configs = db.query(PricingConfig).all()
    plans = [
        PricingPlanItem(
            plan_name="free",
            price_inr=0.0,
            scan_limit=settings.FREE_TIER_MONTHLY_LIMIT,
            description="Essential early disease detection for smallholder farmers",
            features=[
                f"{settings.FREE_TIER_MONTHLY_LIMIT} disease scans per month",
                "Basic symptoms & possible causes",
                "Standard prevention tips",
                "Access to Disease Library",
                "Offline PWA access"
            ]
        )
    ]
    for c in configs:
        plans.append(
            PricingPlanItem(
                plan_name=c.plan_name,
                price_inr=c.price_inr,
                scan_limit=c.scan_limit,
                description=c.description or "",
                features=json.loads(c.features) if c.features else []
            )
        )
    return plans

@router.post("/upgrade")
def upgrade_subscription(
    payload: UpgradePlanRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        # For demo purposes, upgrade default user 1 if not logged in
        current_user = db.query(User).filter(User.id == 1).first()

    result = MockPaymentService.process_subscription_upgrade(
        db=db,
        user=current_user,
        plan_name=payload.plan_name,
        payment_method=payload.payment_method or "UPI / Card (Mock)"
    )
    return result

@router.put("/pricing/{plan_name}")
def update_pricing_by_admin(
    plan_name: str,
    price_inr: float,
    scan_limit: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Allows administrator to adjust Plus and Pro prices dynamically without redeploying code.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required")

    config = db.query(PricingConfig).filter(PricingConfig.plan_name == plan_name.lower()).first()
    if not config:
        config = PricingConfig(plan_name=plan_name.lower(), price_inr=price_inr, scan_limit=scan_limit)
        db.add(config)
    else:
        config.price_inr = price_inr
        config.scan_limit = scan_limit

    db.commit()
    return {"status": "success", "message": f"Updated pricing for {plan_name} to ₹{price_inr}/mo ({scan_limit} scans)."}
