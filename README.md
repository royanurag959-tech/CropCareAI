# 🌱 CropCare AI — AI-Powered Crop Disease Detection, Advisory & Farmer Support Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.110-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18_%2B_Tailwind_CSS-61DAFB?logo=react)](https://react.dev)
[![Vite](https://img.shields.io/badge/Bundler-Vite_5-646CFF?logo=vite)](https://vitejs.dev)
[![PWA](https://img.shields.io/badge/Architecture-Offline--First_PWA-5A0FC8?logo=pwa)](https://web.dev/progressive-web-apps/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **"Detect Early. Protect Crops. Empower Farmers."**  
> Core Philosophy: **DETECT → EXPLAIN → SOLVE → PREVENT**

---

## 1. Project Overview

CropCare AI is a complete, production-grade, cloud-deployable agricultural intelligence platform engineered for real-world farming environments across India and emerging economies.

Unlike superficial disease classifiers, CropCare AI bridges the gap between diagnosis and field survival by answering the critical question: **"Why did this happen?"** It identifies disease vectors, calculates causal factor contributions (excess moisture, humidity, lack of aeration, pest vectors), provides safe step-by-step remedies following approved agricultural standards, and protects smallholders without smartphones through IVR and SMS helplines.

---

## 2. Problem Statement & Rural Challenges

1. **Delayed Detection**: Farmers often detect fungal and viral diseases too late, after 30-40% of foliar area has collapsed, causing massive yield devastation.
2. **Rural Connectivity Void**: Most AI solutions assume persistent 4G/5G broadband. In deep rural belts, cellular connectivity is intermittent or non-existent.
3. **Smartphone Divide**: Over 40% of smallholder farmers operate basic 2G feature phones without touchscreens or app store access.
4. **Lack of Explainability**: Simple prediction labels like *"Tomato Leaf Blight"* do not explain *why* it occurred or how irrigation and microclimate triggered the sporulation.
5. **Language Barrier**: Scientific and English terminology disconnects rural farmers who prefer Hindi or regional languages.

---

## 3. The Solution & Core Pillars

```
Farmer / Crop Photo
       ↓
  [DETECT]  → AI Vision classification identifies pathogen (94% confidence)
       ↓
 [EXPLAIN]  → "Why did this happen?" causal attribution (Microclimate, Humidity, Airflow)
       ↓
  [SOLVE]   → Immediate remedies & safe agricultural extension guidelines
       ↓
 [PREVENT]  → Cultural practices, crop rotation, and resistant hybrid guidance
       ↓
[CONSULT]   → 1-on-1 Agronomist triage if confidence is low or severity is high
```

---

## 4. Key Platform Features

- 🌿 **Precision Crop Vision**: Detection for Tomato, Potato, Rice, Apple, Corn, Wheat, and Cotton with confidence scoring and severity alerts.
- 💡 **Explainable AI Engine**: Breaks down causal vectors based on optional field context (growth stage, recent rainfall, irrigation frequency, symptom duration).
- 🌐 **Offline-First PWA**: Service Worker caching, IndexedDB local storage of entire disease library, and an offline scan queue that auto-synchronizes when internet returns.
- 🟢 **Live Network Status Indicator**: Real-time `🟢 Online` / `🔴 Offline` banner with sync queue counter.
- 📞 **Feature Phone IVR Helpline (1800)**: Interactive Voice Response simulator using browser Speech Synthesis (TTS) in Hindi and English.
- 💬 **SMS Query Assistant (51969)**: 160-character cellular SMS query responder (`TOMATO LEAF SPOTS`).
- 🤝 **Krishi Mitra Extension Portal**: Specialized workflow for village CSC operators and agricultural workers to diagnose crops on behalf of farmers and print physical paper receipts.
- 🗣️ **Bilingual i18n**: Seamless **English | हिंदी** language toggle across all diagnostic labels, advisories, and navigation.
- 💰 **Sustainable Freemium & B2B Monetization**:
  - Free Tier (5 scans/month)
  - CropCare Plus (₹49/month)
  - CropCare Pro (₹99/month)
  - Expert Consultation Fee-Sharing (80% expert / 20% platform)
  - B2B Regional Disease Surveillance Dashboard for FPOs, NGOs, and cooperatives.
- 🛡️ **Safety Guardrails**: Clear non-universal pesticide dosing notices and automatic fallback warnings when confidence < 70%:
  > *"The result is uncertain. Please upload a clearer image or consult an agricultural expert."*

---

## 5. Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite 5, Tailwind CSS, Lucide Icons, Web Speech API |
| **Offline Storage** | Service Worker, IndexedDB, CacheStorage API, localStorage |
| **Backend** | Python 3.11 / 3.13, FastAPI, Uvicorn, Pydantic v2 |
| **Database** | SQLite (Default for zero-setup local hackathon run) / PostgreSQL via SQLAlchemy |
| **Security** | JWT (python-jose), Passlib (Bcrypt), CORS Middleware |
| **AI / ML Layer** | Modular `BaseInferenceEngine`, `DemoInferenceEngine`, hooks for PyTorch / TFLite |
| **DevOps & Cloud** | Docker, Docker Compose, Nginx, Linux Containers |

---

## 6. Project Directory Structure

```
cropcare-ai/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI route controllers (auth, detect, diseases, scans, expert, etc.)
│   │   ├── core/            # App settings, JWT, security hashing
│   │   ├── database/        # SQLAlchemy engine, models, and seed data
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── ai/              # Modular AI engines (Base, DemoEngine, Explainability)
│   │   ├── services/        # Advisory engine, sync service, mock payments
│   │   └── main.py          # FastAPI application entrypoint
│   ├── tests/               # Automated backend test suite (test_api.py)
│   ├── requirements.txt     # Python backend dependencies
│   ├── run_backend.py       # Backend runner script
│   └── generate_samples.py  # Sample leaf image generator
│
├── frontend/
│   ├── public/              # Static assets, manifest.json, sw.js, sample leaves
│   ├── src/
│   │   ├── components/      # Navbar, SeverityBadge, CameraCapture, ExplainabilityCard, etc.
│   │   ├── contexts/        # AuthContext, LanguageContext, OfflineContext
│   │   ├── pages/           # Home, Detect, Result, Library, Dashboard, Assisted, Telecom, etc.
│   │   ├── services/        # API client, IndexedDB offlineStorage, i18n dictionaries
│   │   ├── App.jsx          # Root layout and router
│   │   └── main.jsx         # React mounting
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── ml-model/
│   ├── inference/           # Production PyTorch model loader (model_loader.py)
│   └── training/            # Training architecture & quantization guide (README_TRAINING.md)
│
├── docker-compose.yml       # Multi-container full-stack composition
├── Dockerfile.backend       # FastAPI backend container
├── Dockerfile.frontend      # React + Nginx container
├── .env.example             # Environment variables template
├── HACKATHON_PITCH.md       # Pitch deck and business presentation
└── README.md                # Comprehensive documentation
```

---

## 7. Database Schema & Models

- **Users**: `id`, `name`, `phone`, `email`, `password_hash`, `language`, `role` (`farmer`, `worker`, `expert`, `b2b_org`, `admin`), `subscription_plan` (`free`, `plus`, `pro`), `scan_count_month`, `created_at`.
- **Crops**: `id`, `name`, `hindi_name`, `description`, `icon`.
- **Diseases**: `id`, `crop_id`, `name`, `hindi_name`, `scientific_name`, `severity_level`, `description`, `symptoms` (JSON), `possible_causes` (JSON), `favorable_conditions` (JSON), `immediate_actions` (JSON), `general_management` (JSON), `prevention` (JSON), `when_to_contact_expert`.
- **ScanHistory**: `id`, `user_id`, `farmer_name`, `farmer_phone`, `crop`, `image_url`, `predicted_disease`, `confidence`, `severity`, `follow_up_data`, `generated_explanation`, `symptoms_summary`, `immediate_actions_summary`, `prevention_summary`, `district`, `is_synced`, `created_at`.
- **ExpertRequests**: `id`, `user_id`, `scan_id`, `farmer_name`, `farmer_phone`, `farmer_notes`, `status`, `expert_id`, `expert_notes`, `fee`, `platform_fee`.
- **Subscriptions**: `id`, `user_id`, `plan`, `price`, `start_date`, `end_date`, `status`.
- **Payments**: `id`, `user_id`, `subscription_id`, `amount`, `status`, `transaction_reference`, `payment_method`.
- **PricingConfig**: `id`, `plan_name`, `price_inr`, `scan_limit`, `description`, `features`.

---

## 8. Quick Start / Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### Step 1: Start the Backend
```bash
cd backend

# Create & activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt httpx

# Run automated tests to verify seeds & API
python tests/test_api.py

# Launch FastAPI server (runs on http://127.0.0.1:8000)
python run_backend.py
```

### Step 2: Start the Frontend
In a new terminal:
```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server (runs on http://localhost:5173)
npm run dev
```

Open `http://localhost:5173` in your browser!

---

## 9. Demo Credentials

| Role | Email | Password | Phone |
| :--- | :--- | :--- | :--- |
| **Farmer** | `farmer@cropcare.ai` | `password123` | `9876543210` |
| **Krishi Mitra (Extension)** | `mitra@cropcare.ai` | `password123` | `9876543211` |
| **Agronomist (Expert)** | `expert@cropcare.ai` | `password123` | `9876543212` |
| **FPO Enterprise Partner** | `fpo@cropcare.ai` | `password123` | `9876543213` |
| **Platform Administrator** | `admin@cropcare.ai` | `admin123` | `9876543214` |

*(You can also use the 1-click login buttons on the Sign In page!)*

---

## 10. Sample Demo Journey (Tomato Leaf Blight)

1. Open **CropCare AI** at `http://localhost:5173`.
2. Click **Scan Crop** from the navbar or hero.
3. Select **Tomato (टमाटर)**.
4. Under photo options, click **"Tomato Blight (Demo)"** sample leaf (or take/upload a photo).
5. Open **Field Context** questions: Set Rainfall to *"Moderate"*, Growth Stage to *"Fruiting"*.
6. Click **Run CropCare AI Diagnosis**.
7. Observe results:
   - **Disease**: Tomato Leaf Blight (टमाटर पत्ता झुलसा)
   - **Confidence**: 94%
   - **Severity**: Medium
   - **Why Did This Happen?**: Identifies excess surface moisture, high humidity, and poor canopy aeration.
   - **Immediate Actions**: Safe pruning, avoid overhead watering.
   - **Prevention**: Certified seed stock, crop rotation.
8. Click **Save to Dashboard** or **Print / Save PDF Report**.
9. Test **Talk to an Agriculture Expert** flow.
10. Test switching languages with the top right **English | हिंदी** toggle.
11. Navigate to **IVR / SMS Helpline** to test the 2G basic phone dialer and short-code chat!

---

## 11. Cloud Deployment (Docker)

To deploy the entire production stack with Nginx and FastAPI:
```bash
docker-compose up --build -d
```
The application will be live at `http://localhost`.

---

## 12. Future Scope & Roadmap

- [ ] Real-time satellite NDVI vegetation index overlay.
- [ ] Direct integration with Indian Telecom Gateways (Exotel / Twilio / BSNL).
- [ ] Regional language expansion to Tamil, Telugu, Marathi, Kannada, Bengali, and Punjabi.
- [ ] Micro-weather station IoT telemetry integration.
- [ ] Drone-assisted field aerial surveying for FPO clusters.
