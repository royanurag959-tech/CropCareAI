import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.database.models import User, Subscription, Payment, PricingConfig

class MockPaymentService:
    """
    Mock payment processing for hackathon evaluation simulating
    UPI / Razorpay / Card checkout. Stores transaction audit trail
    and upgrades user subscription limits immediately.
    """

    @staticmethod
    def process_subscription_upgrade(
        db: Session,
        user: User,
        plan_name: str,
        payment_method: str = "UPI / Card (Mock)"
    ) -> Dict[str, Any]:
        plan_clean = plan_name.lower().strip()
        
        # Look up price in pricing_config
        pricing = db.query(PricingConfig).filter(PricingConfig.plan_name == plan_clean).first()
        amount = pricing.price_inr if pricing else (49.0 if plan_clean == "plus" else 99.0)
        
        # Generate mock transaction reference
        tx_ref = f"PAY_CC_{uuid.uuid4().hex[:12].upper()}"

        # Create or update subscription record
        now = datetime.now(timezone.utc)
        sub = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.status == "active"
        ).first()

        if not sub:
            sub = Subscription(
                user_id=user.id,
                plan=plan_clean,
                price=amount,
                start_date=now,
                end_date=now + timedelta(days=30),
                status="active"
            )
            db.add(sub)
        else:
            sub.plan = plan_clean
            sub.price = amount
            sub.end_date = now + timedelta(days=30)

        db.flush()

        # Create payment record
        payment = Payment(
            user_id=user.id,
            subscription_id=sub.id,
            amount=amount,
            status="completed",
            transaction_reference=tx_ref,
            payment_method=payment_method,
            created_at=now
        )
        db.add(payment)

        # Update user tier
        user.subscription_plan = plan_clean
        db.commit()

        return {
            "success": True,
            "transaction_reference": tx_ref,
            "plan": plan_clean,
            "amount_paid_inr": amount,
            "status": "completed",
            "message": f"Successfully activated CropCare {plan_clean.capitalize()} plan!",
            "expires_at": sub.end_date.isoformat()
        }
