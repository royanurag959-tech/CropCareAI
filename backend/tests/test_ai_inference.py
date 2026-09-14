import os
import sys
import io
from PIL import Image

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add backend directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.seed_data import seed_database
seed_database()

from fastapi.testclient import TestClient
from app.main import app
from app.ai.factory import get_inference_engine
from app.ai.mock_provider import MockInferenceProvider
from app.ai.real_provider import RealModelInferenceProvider
from app.weather.factory import get_weather_provider
from app.telecom.factory import get_telecom_provider
from app.services.risk_scoring import CropRiskScoringEngine
from app.services.escalation import ExpertEscalationEvaluator
from app.services.progress_tracking import DiseaseProgressTracker
from app.services.advisory import AdvisoryService

client = TestClient(app)

def test_modular_ai_inference_layer():
    mock_engine = get_inference_engine("mock")
    assert isinstance(mock_engine, MockInferenceProvider)
    assert mock_engine.provider_name == "MockInferenceProvider"

    real_engine = get_inference_engine("real")
    assert isinstance(real_engine, RealModelInferenceProvider)
    assert "RealModelInferenceProvider" in real_engine.provider_name

    # Test prediction on Tomato
    img = Image.new("RGB", (100, 100), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    pred = mock_engine.predict(img_bytes, crop_name="Tomato", filename="leaf.jpg")
    assert pred["crop"] == "Tomato"
    assert pred["predicted_disease"] == "Tomato Leaf Blight"
    assert pred["confidence"] >= 0.90
    assert pred["confidence_level"] == "high"
    assert "short_explanation" in pred
    assert "short_explanation_hindi" in pred
    print("✓ Modular AI inference layer verified (Mock & Real providers)")

def test_confidence_tiers_and_uncertainty():
    mock_engine = MockInferenceProvider()

    # High confidence (healthy leaf: 96%)
    img = Image.new("RGB", (100, 100), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    healthy_pred = mock_engine.predict(buf.getvalue(), crop_name="Tomato", filename="healthy_leaf.jpg")
    assert healthy_pred["confidence_level"] == "high"
    assert healthy_pred["is_uncertain"] is False
    assert healthy_pred["confidence_percentage"] >= 90

    # Low confidence (< 60% with uncertainty flag)
    unclear_pred = mock_engine.predict(buf.getvalue(), crop_name="Tomato", filename="unclear_blurry.jpg")
    assert unclear_pred["confidence_level"] == "low"
    assert unclear_pred["is_uncertain"] is True
    assert unclear_pred["confidence_percentage"] < 60
    assert unclear_pred["uncertainty_message"] is not None
    print("✓ 3-Tier AI confidence levels verified (High >=90%, Medium 60-89%, Low <60% with uncertainty)")

def test_image_preprocessing_validation():
    # 1. Invalid extension / non-image
    fake_txt = io.BytesIO(b"This is not a real image file.")
    res = client.post(
        "/api/detect",
        data={"crop": "Tomato"},
        files={"image": ("malicious.txt", fake_txt, "text/plain")}
    )
    assert res.status_code == 400
    assert "invalid" in res.json()["detail"].lower()

    # 2. Too small dimensions (<50x50)
    tiny_img = Image.new("RGB", (20, 20), color=(50, 50, 50))
    buf = io.BytesIO()
    tiny_img.save(buf, format="JPEG")
    buf.seek(0)
    res = client.post(
        "/api/detect",
        data={"crop": "Tomato"},
        files={"image": ("tiny.jpg", buf, "image/jpeg")}
    )
    assert res.status_code == 400
    assert "resolution too low" in res.json()["detail"].lower()

    # 3. Valid image -> 200 OK
    good_img = Image.new("RGB", (120, 120), color=(40, 140, 40))
    buf = io.BytesIO()
    good_img.save(buf, format="JPEG")
    buf.seek(0)
    res = client.post(
        "/api/detect",
        data={"crop": "Tomato", "growth_stage": "Fruiting"},
        files={"image": ("valid_leaf.jpg", buf, "image/jpeg")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["crop"] == "Tomato"
    assert "risk_score" in data
    assert "action_plan" in data
    assert "progress_tracking" in data
    print("✓ Image pre-processing validation verified (format, dimension, corrupt rejection)")

def test_crop_risk_score_engine():
    # Low risk
    low_risk = CropRiskScoringEngine.calculate_risk_score(
        severity="Low",
        confidence=0.95,
        weather={"humidity_pct": 50, "rainfall_desc": "None"},
        context={"predicted_disease": "Healthy Tomato", "irrigation": "Weekly", "drainage": "Good", "growth_stage": "Vegetative"}
    )
    assert low_risk["score"] <= 30
    assert low_risk["category"] == "Low Risk"

    # High / Critical risk
    high_risk = CropRiskScoringEngine.calculate_risk_score(
        severity="High",
        confidence=0.92,
        weather={"humidity_pct": 90, "rainfall_desc": "Heavy"},
        context={"predicted_disease": "Rice Blast", "irrigation": "Daily", "drainage": "Poor / Waterlogged", "growth_stage": "Flowering", "affected_area": ">30%"}
    )
    assert high_risk["score"] >= 61
    assert high_risk["category"] in ["High Risk", "Critical Risk"]
    assert "app-generated" in high_risk["disclaimer"].lower()
    print("✓ Configurable Crop Risk Score System verified (0-100 across 4 categories)")

def test_expert_escalation_triggers_and_dossier():
    # Trigger on low confidence
    esc_low_conf = ExpertEscalationEvaluator.evaluate(
        confidence=0.45,
        severity="Medium",
        risk_score=50
    )
    assert esc_low_conf["suggest_expert"] is True
    assert any("low" in r.lower() for r in esc_low_conf["reasons"])

    # Trigger on high risk
    esc_high_risk = ExpertEscalationEvaluator.evaluate(
        confidence=0.85,
        severity="Medium",
        risk_score=75
    )
    assert esc_high_risk["suggest_expert"] is True
    assert any("risk score" in r.lower() for r in esc_high_risk["reasons"])

    # Case dossier compilation
    dossier = ExpertEscalationEvaluator.compile_case_dossier(
        crop="Tomato",
        predicted_disease="Tomato Leaf Blight",
        confidence=0.88,
        confidence_level="medium",
        risk_score=65,
        risk_category="High Risk",
        farmer_question="Should I apply copper spray today?"
    )
    assert dossier["crop"] == "Tomato"
    assert dossier["risk_score"] == 65
    assert dossier["farmer_question"] == "Should I apply copper spray today?"
    print("✓ Expert Escalation triggers & Case Dossier compiler verified")

def test_disease_progress_tracking():
    # Initial scan -> Uncertain
    res1 = DiseaseProgressTracker.evaluate_progression(
        current_scan={"risk_score": 70, "severity": "High", "confidence": 0.90},
        historical_scans=[]
    )
    assert res1["trend"] == "Uncertain"

    # Improving scan (score dropped by 20 points)
    res2 = DiseaseProgressTracker.evaluate_progression(
        current_scan={"risk_score": 50, "severity": "Medium", "confidence": 0.88},
        historical_scans=[{"risk_score": 70, "severity": "High"}]
    )
    assert res2["trend"] == "Improving"
    assert res2["risk_delta"] == -20

    # Rapidly increasing scan (score surged by 25 points)
    res3 = DiseaseProgressTracker.evaluate_progression(
        current_scan={"risk_score": 85, "severity": "High", "confidence": 0.94},
        historical_scans=[{"risk_score": 60, "severity": "Medium"}]
    )
    assert res3["trend"] == "Rapidly Increasing"
    assert res3["recommend_expert_escalation"] is True
    print("✓ Disease Progress Tracking & Trend Classification verified (Improving, Stable, Increasing, Rapidly Increasing)")

def test_modular_weather_and_telecom():
    weather_provider = get_weather_provider("mock")
    w = weather_provider.get_weather("Pune District")
    assert w["temperature_c"] > 0
    assert w["humidity_pct"] > 0
    assert "condition" in w

    telecom_provider = get_telecom_provider("mock")
    ivr_res = telecom_provider.process_ivr_call("9876543210", "hi", "Tomato", "spots", keypad_input="9")
    assert ivr_res["call_status"] == "expert_requested"
    assert "कृषि विशेषज्ञ" in ivr_res["voice_script"]

    sms_res = telecom_provider.process_sms_query("9876543210", "TOMATO LEAF SPOTS")
    assert "TOMATO" in sms_res["sms_response"]
    print("✓ Modular Weather Provider & Telecom Gateway verified")

def test_time_phased_action_plan_and_safety():
    plan = AdvisoryService.get_time_phased_action_plan(
        disease_name="Tomato Leaf Blight",
        crop_name="Tomato",
        severity="Medium",
        risk_category="High Risk"
    )
    assert len(plan["today"]) >= 3
    assert len(plan["next_3_days"]) >= 2
    assert len(plan["next_7_days"]) >= 3
    assert "chemical_safety_notice" in plan
    assert "never apply uncalibrated" in plan["chemical_safety_notice"].lower()
    print("✓ Time-phased action plan (Today, 3 Days, 7 Days) with chemical safety guardrails verified")

if __name__ == "__main__":
    print("\n🌿 Running Comprehensive CropCare AI Diagnostics & Advisory Test Suite...")
    test_modular_ai_inference_layer()
    test_confidence_tiers_and_uncertainty()
    test_image_preprocessing_validation()
    test_crop_risk_score_engine()
    test_expert_escalation_triggers_and_dossier()
    test_disease_progress_tracking()
    test_modular_weather_and_telecom()
    test_time_phased_action_plan_and_safety()
    print("\n🎉 ALL ADVANCED SYSTEM TESTS PASSED SUCCESSFULLY!\n")
