import os
import sys
import io

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

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")

def test_crops_and_diseases_catalog():
    response = client.get("/api/diseases/crops")
    assert response.status_code == 200
    crops = response.json()
    assert len(crops) >= 5
    crop_names = [c["name"] for c in crops]
    assert "Tomato" in crop_names
    assert "Potato" in crop_names
    print(f"✓ Retrieved {len(crops)} crops: {crop_names}")

    response = client.get("/api/diseases?crop=Tomato")
    assert response.status_code == 200
    diseases = response.json()
    assert len(diseases) >= 1
    assert "Tomato Leaf Blight" in [d["name"] for d in diseases]
    print(f"✓ Retrieved {len(diseases)} tomato diseases")

def test_detection_journey_tomato_leaf_blight():
    from PIL import Image
    # Simulate exact demo journey
    form_data = {
        "crop": "Tomato",
        "growth_stage": "Fruiting",
        "rainfall": "Moderate",
        "irrigation": "Every 2 days",
        "duration": "4 days",
        "affected_area": "10-30%",
        "location": "Pune District"
    }
    
    # 100x100 valid test image
    img = Image.new("RGB", (100, 100), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    files = {"image": ("sample_tomato_blight.jpg", buf, "image/jpeg")}

    response = client.post("/api/detect", data=form_data, files=files)
    assert response.status_code == 200
    data = response.json()
    
    assert data["crop"] == "Tomato"
    assert data["predicted_disease"] == "Tomato Leaf Blight"
    assert data["confidence_percentage"] == 94
    assert data["severity"] == "Medium"
    assert "why_did_it_happen" in data
    assert len(data["why_did_it_happen"]["contributing_factors"]) >= 3
    assert len(data["symptoms"]) > 0
    assert len(data["immediate_actions"]) > 0
    assert len(data["prevention"]) > 0
    print("✓ Tomato Leaf Blight journey passed with 94% confidence, explainability, and full advisory!")

def test_uncertain_prediction_handling():
    from PIL import Image
    # Test low confidence trigger when image is unclear
    form_data = {"crop": "Tomato"}
    img = Image.new("RGB", (100, 100), color=(100, 100, 100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    files = {"image": ("blurry_unclear_photo.jpg", buf, "image/jpeg")}

    response = client.post("/api/detect", data=form_data, files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["is_uncertain"] is True
    assert "clearer" in data["uncertainty_message"].lower() or "expert" in data["uncertainty_message"].lower()
    print("✓ Uncertain / low-confidence detection flagged properly with warning!")

def test_telecom_ivr_and_sms():
    # IVR test
    ivr_payload = {
        "caller_phone": "9876543210",
        "language": "hi",
        "crop": "Tomato",
        "symptoms_key": "spots"
    }
    response = client.post("/api/telecom/ivr", json=ivr_payload)
    assert response.status_code == 200
    ivr_data = response.json()
    assert "झुलसा" in ivr_data["voice_script"] or "टमाटर" in ivr_data["voice_script"]
    print("✓ IVR Hindi speech response verified")

    # SMS test
    sms_payload = {
        "sender_phone": "9876543210",
        "message": "TOMATO LEAF SPOTS"
    }
    response = client.post("/api/telecom/sms", json=sms_payload)
    assert response.status_code == 200
    sms_data = response.json()
    assert "CropCare SMS:" in sms_data["sms_response"]
    print(f"✓ SMS response generated: {sms_data['sms_response']}")

def test_subscription_and_mock_payment():
    response = client.get("/api/subscription/pricing")
    assert response.status_code == 200
    plans = response.json()
    assert len(plans) >= 3  # Free, Plus, Pro
    print(f"✓ Retrieved pricing plans: {[p['plan_name'] for p in plans]}")

    upgrade_payload = {"plan_name": "plus", "payment_method": "UPI / PhonePe (Mock)"}
    response = client.post("/api/subscription/upgrade", json=upgrade_payload)
    assert response.status_code == 200
    pay_data = response.json()
    assert pay_data["success"] is True
    assert pay_data["plan"] == "plus"
    assert "PAY_CC_" in pay_data["transaction_reference"]
    print(f"✓ Mock payment successful with ref: {pay_data['transaction_reference']}")

def test_assisted_diagnosis():
    assisted_payload = {
        "farmer_name": "Babu Lal",
        "farmer_phone": "9812345678",
        "village": "Hoshangabad",
        "crop": "Tomato",
        "growth_stage": "Vegetative"
    }
    response = client.post("/api/assisted/diagnose", data=assisted_payload)
    assert response.status_code == 200
    assisted_data = response.json()
    assert assisted_data["farmer_name"] == "Babu Lal"
    assert "CropCare AI Receipt" in assisted_data["sms_receipt"]
    print("✓ Krishi Mitra assisted diagnosis verified with receipt")

def test_analytics_and_b2b():
    response = client.get("/api/analytics/regional")
    assert response.status_code == 200
    analytics = response.json()
    assert len(analytics["districts"]) >= 4
    print(f"✓ Regional surveillance analytics returned {len(analytics['districts'])} districts")

if __name__ == "__main__":
    print("\n🌿 Running CropCare AI Backend Automated Tests...")
    test_health_check()
    test_crops_and_diseases_catalog()
    test_detection_journey_tomato_leaf_blight()
    test_uncertain_prediction_handling()
    test_telecom_ivr_and_sms()
    test_subscription_and_mock_payment()
    test_assisted_diagnosis()
    test_analytics_and_b2b()
    print("\n🎉 ALL BACKEND TESTS PASSED SUCCESSFULLY!\n")
