import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "CropCare AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "cropcare-secret-key-for-hackathon-2026-production-ready")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # PostgreSQL Database URL (Neon serverless)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_wrT0qeG8bXSh@ep-damp-bar-ae5hgeff-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )
    
    # Storage directory for uploaded leaf scans
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "./uploaded_scans")
    
    # Demo and ML mode
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")
    MODEL_WEIGHTS_PATH: Optional[str] = os.getenv("MODEL_WEIGHTS_PATH", None)
    
    # Weather Provider
    WEATHER_PROVIDER: str = os.getenv("WEATHER_PROVIDER", "mock")
    WEATHER_API_KEY: Optional[str] = os.getenv("WEATHER_API_KEY", None)

    # Telecom Provider
    TELECOM_PROVIDER: str = os.getenv("TELECOM_PROVIDER", "mock")

    # Confidence Threshold (below 0.60 is low confidence)
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))
    
    # Scan Quotas
    FREE_TIER_MONTHLY_LIMIT: int = 5
    PLUS_TIER_MONTHLY_LIMIT: int = 50
    PRO_TIER_MONTHLY_LIMIT: int = 500

settings = Settings()

# Ensure storage directory exists
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
