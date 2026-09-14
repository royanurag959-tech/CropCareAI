import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.database.seed_data import seed_database
from app.api import auth, detect, diseases, scans, expert, subscriptions, analytics, assisted, ivr_sms

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure database tables & seed data are initialized
    print(f"[INFO] Initializing {settings.PROJECT_NAME} v{settings.VERSION}...")
    seed_database()
    yield
    # Shutdown
    print("[INFO] Shutting down CropCare AI backend.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Crop Disease Detection, Advisory & Farmer Support Platform",
    lifespan=lifespan
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure sample leaves & storage directories exist
sample_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_leaves")
os.makedirs(sample_dir, exist_ok=True)
os.makedirs(settings.STORAGE_DIR, exist_ok=True)

app.mount("/uploaded_scans", StaticFiles(directory=settings.STORAGE_DIR), name="uploaded_scans")
app.mount("/sample_leaves", StaticFiles(directory=sample_dir), name="sample_leaves")

# Register API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(detect.router, prefix=settings.API_V1_STR)
app.include_router(diseases.router, prefix=settings.API_V1_STR)
app.include_router(scans.router, prefix=settings.API_V1_STR)
app.include_router(expert.router, prefix=settings.API_V1_STR)
app.include_router(subscriptions.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(assisted.router, prefix=settings.API_V1_STR)
app.include_router(ivr_sms.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "platform": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "philosophy": "DETECT -> EXPLAIN -> SOLVE -> PREVENT",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "demo_mode": settings.DEMO_MODE,
        "database": settings.DATABASE_URL.split(":")[0]
    }
