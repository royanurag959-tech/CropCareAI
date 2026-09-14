import json
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    language = Column(String(10), default="en")  # 'en' or 'hi'
    role = Column(String(20), default="farmer")   # 'farmer', 'worker', 'expert', 'b2b_org', 'admin'
    subscription_plan = Column(String(20), default="free")  # 'free', 'plus', 'pro'
    scan_count_month = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    scans = relationship("ScanHistory", back_populates="user")
    expert_requests = relationship("ExpertRequest", foreign_keys="ExpertRequest.user_id", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    hindi_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), default="leaf")

    diseases = relationship("Disease", back_populates="crop")

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    name = Column(String(150), nullable=False)
    hindi_name = Column(String(150), nullable=False)
    scientific_name = Column(String(150), nullable=True)
    severity_level = Column(String(20), default="Medium")  # Low, Medium, High
    description = Column(Text, nullable=False)
    
    # JSON-encoded lists for flexible multi-item attributes
    symptoms = Column(Text, nullable=False)  # JSON string of list
    possible_causes = Column(Text, nullable=False)  # JSON string of list
    favorable_conditions = Column(Text, nullable=False)  # JSON string of list
    immediate_actions = Column(Text, nullable=False)  # JSON string of list
    general_management = Column(Text, nullable=False)  # JSON string of list
    prevention = Column(Text, nullable=False)  # JSON string of list
    when_to_contact_expert = Column(Text, nullable=True)

    crop = relationship("Crop", back_populates="diseases")

    def to_dict(self):
        return {
            "id": self.id,
            "crop_id": self.crop_id,
            "crop_name": self.crop.name if self.crop else "",
            "name": self.name,
            "hindi_name": self.hindi_name,
            "scientific_name": self.scientific_name,
            "severity_level": self.severity_level,
            "description": self.description,
            "symptoms": json.loads(self.symptoms) if self.symptoms else [],
            "possible_causes": json.loads(self.possible_causes) if self.possible_causes else [],
            "favorable_conditions": json.loads(self.favorable_conditions) if self.favorable_conditions else [],
            "immediate_actions": json.loads(self.immediate_actions) if self.immediate_actions else [],
            "general_management": json.loads(self.general_management) if self.general_management else [],
            "prevention": json.loads(self.prevention) if self.prevention else [],
            "when_to_contact_expert": self.when_to_contact_expert
        }

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    farmer_name = Column(String(100), nullable=True)  # Useful for assisted field diagnosis
    farmer_phone = Column(String(20), nullable=True)
    crop = Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=True)
    predicted_disease = Column(String(150), nullable=False)
    confidence = Column(Float, nullable=False)  # 0.0 - 1.0 (e.g. 0.94)
    confidence_level = Column(String(20), default="high")  # 'high', 'medium', 'low'
    severity = Column(String(20), nullable=False)
    is_uncertain = Column(Boolean, default=False)
    
    # Risk Score & Progress Tracking
    plot_id = Column(String(100), nullable=True)  # Plot/Batch identifier for monitoring timelines
    parent_scan_id = Column(Integer, nullable=True)
    risk_score = Column(Integer, nullable=True)  # 0 - 100
    risk_category = Column(String(50), nullable=True)  # Low, Moderate, High, Critical
    trend = Column(String(50), nullable=True)  # Improving, Stable, Increasing, Rapidly Increasing, Uncertain
    farmer_notes = Column(Text, nullable=True)

    # Explainable AI & Advisory details
    short_explanation = Column(Text, nullable=True)
    follow_up_data = Column(Text, nullable=True)  # JSON: growth_stage, rainfall, irrigation, duration
    farm_conditions_summary = Column(Text, nullable=True)  # JSON: weather, moisture, drainage
    generated_explanation = Column(Text, nullable=True)
    symptoms_summary = Column(Text, nullable=True)  # JSON
    immediate_actions_summary = Column(Text, nullable=True)  # JSON
    prevention_summary = Column(Text, nullable=True)  # JSON
    
    is_synced = Column(Boolean, default=True)
    district = Column(String(100), default="District A")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="scans")
    expert_requests = relationship("ExpertRequest", back_populates="scan")

class ExpertRequest(Base):
    __tablename__ = "expert_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scan_history.id"), nullable=True)
    farmer_name = Column(String(100), nullable=True)
    farmer_phone = Column(String(20), nullable=True)
    farmer_notes = Column(Text, nullable=True)
    farmer_question = Column(Text, nullable=True)
    dossier_data = Column(Text, nullable=True)  # JSON snapshot of full case dossier
    status = Column(String(30), default="pending")  # pending, assigned, in_review, resolved
    expert_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    expert_notes = Column(Text, nullable=True)
    fee = Column(Float, default=99.0)  # in INR
    platform_fee = Column(Float, default=19.8)  # 20% platform cut
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", foreign_keys=[user_id], back_populates="expert_requests")
    expert = relationship("User", foreign_keys=[expert_id])
    scan = relationship("ScanHistory", back_populates="expert_requests")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan = Column(String(50), nullable=False)  # free, plus, pro
    price = Column(Float, default=0.0)
    start_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="active")

    user = relationship("User", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="completed")  # completed, pending, failed
    transaction_reference = Column(String(100), nullable=False)
    payment_method = Column(String(50), default="UPI / Card (Mock)")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    subscription = relationship("Subscription", back_populates="payments")

class PricingConfig(Base):
    __tablename__ = "pricing_config"

    id = Column(Integer, primary_key=True, index=True)
    plan_name = Column(String(50), unique=True, nullable=False)  # plus, pro
    price_inr = Column(Float, nullable=False)
    scan_limit = Column(Integer, nullable=False)
    description = Column(String(255), nullable=True)
    features = Column(Text, nullable=True)  # JSON list
