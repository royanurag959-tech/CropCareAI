from typing import Optional, List, Any, Dict
from pydantic import BaseModel

# Auth Schemas
class UserRegister(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    password: str
    language: Optional[str] = "en"
    role: Optional[str] = "farmer"

class UserLogin(BaseModel):
    identifier: str  # phone or email
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    language: str
    role: str
    subscription_plan: str
    scan_count_month: int

# Disease & Crop Schemas
class CropResponse(BaseModel):
    id: int
    name: str
    hindi_name: str
    description: Optional[str] = None
    icon: str

class DiseaseResponse(BaseModel):
    id: int
    crop_id: int
    crop_name: str
    name: str
    hindi_name: str
    scientific_name: Optional[str] = None
    severity_level: str
    description: str
    symptoms: List[str]
    possible_causes: List[str]
    favorable_conditions: List[str]
    immediate_actions: List[str]
    general_management: List[str]
    prevention: List[str]
    when_to_contact_expert: Optional[str] = None

# Detection & Advisory Schemas
class FollowUpContext(BaseModel):
    growth_stage: Optional[str] = None      # e.g., Seedling, Vegetative, Flowering, Fruiting, Harvesting
    crop_age: Optional[str] = None          # e.g., 2-4 weeks, 1-2 months, >3 months
    rainfall: Optional[str] = None          # None, Light, Moderate, Heavy, Continuous
    irrigation: Optional[str] = None        # Daily, Every 2-3 days, Weekly, Overhead / Flood
    drainage: Optional[str] = None          # Good, Poor / Waterlogged
    duration: Optional[str] = None          # <3 days, 4-7 days, 1-2 weeks, >2 weeks
    affected_area: Optional[str] = None     # <10%, 10-30%, >30%
    location: Optional[str] = "Pune District"
    plot_id: Optional[str] = None
    farmer_notes: Optional[str] = None

class RiskScoreResponse(BaseModel):
    score: int
    category: str
    category_hindi: str
    color: str
    explanation: str
    explanation_hindi: str
    contributing_breakdown: Dict[str, int]
    disclaimer: str

class TimePhasedActionPlan(BaseModel):
    today: List[str]
    today_hindi: List[str]
    next_3_days: List[str]
    next_3_days_hindi: List[str]
    next_7_days: List[str]
    next_7_days_hindi: List[str]
    rescan_recommended_days: int
    chemical_safety_notice: str
    chemical_safety_notice_hindi: str

class ProgressTrackingResponse(BaseModel):
    trend: str
    trend_hindi: str
    trend_description: str
    trend_description_hindi: str
    previous_risk_score: Optional[int] = None
    current_risk_score: int
    risk_delta: int
    recommend_expert_escalation: bool
    total_historical_records: int

class EscalationRecommendation(BaseModel):
    suggest_expert: bool
    trigger_count: int
    reasons: List[str]
    reasons_hindi: List[str]
    primary_prompt: str
    primary_prompt_hindi: str

class DetectionResponse(BaseModel):
    crop: str
    crop_hindi: Optional[str] = None
    predicted_disease: str
    hindi_name: str
    scientific_name: Optional[str] = None
    confidence: float
    confidence_percentage: int
    confidence_level: str = "high"  # 'high', 'medium', 'low'
    confidence_level_label: str = "High Confidence"
    confidence_level_label_hindi: str = "उच्च विश्वास (सटीक)"
    severity: str
    is_uncertain: bool
    uncertainty_message: Optional[str] = None
    short_explanation: str
    short_explanation_hindi: Optional[str] = None
    provider_name: Optional[str] = None

    # Risk Score & Farm Conditions
    risk_score: RiskScoreResponse
    weather: Optional[Dict[str, Any]] = None
    farm_conditions: Optional[Dict[str, Any]] = None

    # Time-Phased Action Plan
    action_plan: TimePhasedActionPlan

    # Disease Progress Tracking & Escalation
    progress_tracking: Optional[ProgressTrackingResponse] = None
    escalation: EscalationRecommendation

    # Explainable AI
    why_did_it_happen: Dict[str, Any]
    
    # Comprehensive Advisory
    symptoms: List[str]
    possible_causes: List[str]
    immediate_actions: List[str]
    general_management: List[str]
    prevention: List[str]
    when_to_contact_expert: Optional[str] = None
    
    # Meta
    scan_id: Optional[int] = None
    image_url: Optional[str] = None
    disclaimer: str

# Scan History Schemas
class ScanHistoryItem(BaseModel):
    id: int
    crop: str
    predicted_disease: str
    confidence: float
    confidence_level: Optional[str] = "high"
    severity: str
    is_uncertain: Optional[bool] = False
    risk_score: Optional[int] = None
    risk_category: Optional[str] = None
    trend: Optional[str] = None
    plot_id: Optional[str] = None
    image_url: Optional[str] = None
    short_explanation: Optional[str] = None
    farmer_notes: Optional[str] = None
    generated_explanation: Optional[str] = None
    farmer_name: Optional[str] = None
    farmer_phone: Optional[str] = None
    district: Optional[str] = None
    created_at: str

# Expert Request Schemas
class ExpertCreateRequest(BaseModel):
    scan_id: Optional[int] = None
    farmer_phone: Optional[str] = None
    farmer_notes: Optional[str] = None
    farmer_question: Optional[str] = None
    dossier_data: Optional[Dict[str, Any]] = None

class ExpertResolveRequest(BaseModel):
    expert_notes: str

# Pricing & Subscription Schemas
class PricingPlanItem(BaseModel):
    plan_name: str
    price_inr: float
    scan_limit: int
    description: str
    features: List[str]

class UpgradePlanRequest(BaseModel):
    plan_name: str
    payment_method: Optional[str] = "UPI / Card (Mock)"

# Offline Sync Schemas
class OfflineScanPayload(BaseModel):
    crop: str
    predicted_disease: str
    confidence: float
    severity: str
    follow_up_data: Optional[Dict[str, Any]] = None
    generated_explanation: Optional[str] = None
    client_timestamp: Optional[str] = None
    farmer_name: Optional[str] = None
    farmer_phone: Optional[str] = None

class SyncBatchRequest(BaseModel):
    scans: List[OfflineScanPayload]

# Telecom (IVR & SMS) Schemas
class IVRCallRequest(BaseModel):
    caller_phone: str
    language: str  # 'hi' or 'en'
    crop: str
    symptoms_key: str  # e.g., 'spots', 'curling', 'yellowing', 'rot'
    keypad_input: Optional[str] = "1"

class SMSQueryRequest(BaseModel):
    sender_phone: str
    message: str  # e.g., 'TOMATO LEAF SPOTS' or 'धान पत्ता धब्बा'
