# NutriGuard AI — Production-Grade AI Nutrition & Indian Meal Recommendation Platform

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg)](https://vitejs.dev)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com)
[![Tests](https://img.shields.io/badge/Pytest-87%2F87%20Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

NutriGuard is an AI-powered nutrition intelligence and Indian meal planning platform. Unlike generic Western calorie-counting apps, NutriGuard is purpose-built for Indian kitchens—measuring meals in rotis, katoris, dals, and sabzis across regional cuisines (North, South, West, East, and Pan-Indian) while enforcing deterministic clinical safety guardrails against prescription medications and chronic health conditions.

---

## Key Highlights

- **Authentic Indian Culinary Intelligence**: 120+ authentic Indian recipes and 60+ staple raw food profiles calibrated from ICMR-NIN Indian Food Composition Tables (IFCT 2017).
- **Deterministic Clinical Safety Guardrails**: Hard-coded safety engines enforce medical vetoes (e.g. Warfarin + Vitamin K greens, Stage 4+ CKD potassium caps, Metformin B12 depletion warnings, food allergen blocks). Generative AI **never** overrides clinical rules.
- **Household Measurement Modeling**: Portions defined in katoris, rotis, cups, plates, and pieces with verified macronutrient and micronutrient scaling.
- **Hybrid AI Architecture**: Google Gemini (1.5/2.0 Flash) provides natural language chat parsing, substitution suggestions, and educational explanations, with 100% deterministic rule-based fallback when offline.
- **Enterprise-Grade Observability**: Comprehensive `/health` telemetry, live admin clinical reviewer simulator, data source attribution, and 82/82 passing automated regression tests.

---

## System Architecture

```
User Input / Web Portal
         │
         ▼
[ FastAPI Gateway (ASGI) ] ── (JWT Bearer Auth & CORS Middleware)
         │
    ┌────┴───────────────────────────┐
    ▼                                ▼
[ NLP Entity Extraction ]   [ Clinical Safety Engine ]
(Gemini Flash / Regex)      (Deterministic Hard Blocks: Allergens & Drug Vetoes)
    │                                │
    └───────────────┬────────────────┘
                    ▼
       [ Recommendation Engine ]
   (Mifflin-St Jeor BMR, TDEE, ICMR RDAs, Diversity)
                    │
                    ▼
     [ Explanations & Citations ]
  (IFCT 2017 / USDA FDC Attributions)
                    │
                    ▼
 [ React + Vite UI (Tailwind CSS) ]
```

---

## Directory Structure

```
nutriguard/
├── backend/
│   ├── ai/                 # Gemini LLM integration, prompt templates, NLP entity extractors
│   ├── alembic/            # Linear database migration versions (5 migrations)
│   ├── api/
│   │   ├── routes/         # Endpoints: auth, profile, meal_plan, meals, chat, admin, nlp
│   │   └── schemas/        # Pydantic validation schemas
│   ├── core/               # App configuration, database session, logging, exceptions
│   ├── data/               # Seed datasets (IFCT foods, medications, conditions, meals)
│   ├── engines/            # Safety, diversity, portion, recommendation, substitution engines
│   ├── models/             # SQLAlchemy ORM models (Food, Meal, User, Profile, Rule, etc.)
│   ├── services/           # Orchestration services (RecommendationService, MealPlanService)
│   ├── tests/              # 82 Pytest suites (unit, integration, clinical regression)
│   ├── migrate_and_seed.py # Automated Alembic migration & idempotent seed runner
│   └── requirements.txt    # Production Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios API client & typed endpoint services
│   │   ├── components/     # Layout, MealCard, NutritionProgress, EmptyState, etc.
│   │   ├── context/        # AuthContext for session management
│   │   └── pages/          # Landing, Dashboard, AIAssistant, FoodDB, Admin, Health, etc.
│   ├── dist/               # Production Vite build artifacts
│   ├── package.json        # Frontend scripts and dependencies
│   └── vite.config.js      # Vite dev server & production bundler config
├── ARCHITECTURE.md         # Detailed architectural & clinical logic specification
├── DEPLOYMENT.md           # Step-by-step Render & Vercel deployment guide
└── DATA_SOURCES.md         # Full attribution, versions & licensing documentation
```

---

## Getting Started

### Prerequisites

- **Python**: 3.11, 3.12, or 3.14
- **Node.js**: v18+ (tested on Node v24)
- **Database**: PostgreSQL (production) or SQLite (local development)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env to supply your DATABASE_URL, JWT_SECRET, and optional GEMINI_API_KEY

# Run database migrations and seed authoritative data
python migrate_and_seed.py

# Launch development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend is now accessible at `http://localhost:8000`.
- Swagger API Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/health`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

The frontend will run at `http://localhost:5173`. Requests to `/api` and `/health` are proxied directly to the backend.

### 3. Production Build

To verify the production frontend build:
```bash
cd frontend
npm run build
```

---

## Environment Variables

| Variable | Required | Default / Example | Purpose |
|---|---|---|---|
| `DATABASE_URL` | **Yes** | `postgresql://user:pass@host:5432/nutriguard` | Relational database connection string |
| `JWT_SECRET` | **Yes** | `your-secure-random-32-char-key` | Signs authentication tokens |
| `JWT_ALGORITHM` | No | `HS256` | JWT signature algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `10080` (7 days) | Token expiration duration |
| `GEMINI_API_KEY` | No | `AIzaSy...` | Enables Google Gemini Flash for chat & NLP |
| `PORT` | No | `8000` | Port for ASGI server (used by Render/Railway) |
| `ENVIRONMENT` | No | `production` | Runtime mode (`development` / `production`) |
| `CORS_ORIGINS` | No | `["http://localhost:5173"]` | Allowed CORS origins for frontend clients |

---

## Running the Automated Test Suite

NutriGuard features 87 unit, integration, and clinical safety regression tests:

```bash
cd backend
python -m pytest tests/ -v
```

Test coverage includes:
- **Clinical Safety Tests**: Verification that allergen vetoes, drug-food interactions, and condition restrictions cannot be bypassed.
- **Engine Tests**: Portion scaling, diversity engine, substitution logic, and Mifflin-St Jeor TDEE calculations.
- **API Tests**: Authentication, onboarding, meal planning, and admin endpoints.
- **Regression Profiles**: 5 distinct clinical persona pipelines (CKD + Anemia, Hypothyroid + Gout, Vegan + PCOS, etc.).

---

## Clinical & Medical Disclaimer

NutriGuard is designed as an educational nutrition planning and AI dietary exploration platform based on authoritative scientific data from the Indian Council of Medical Research (ICMR) and National Institute of Nutrition (NIN). It does **not** provide medical diagnoses, treatment prescriptions, or clinical therapy. Users managing chronic illnesses, pregnancy, or prescription medications must consult a qualified physician or registered dietitian before modifying their dietary routine.

---

## License

This project is licensed under the MIT License. Data sources retain their respective institutional licenses (see [DATA_SOURCES.md](DATA_SOURCES.md)).
