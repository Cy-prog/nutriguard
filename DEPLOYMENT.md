# NutriGuard Production Deployment Guide

This guide details step-by-step instructions for deploying the **NutriGuard** platform to production using **Render** (Backend API & PostgreSQL Database) and **Vercel** (Frontend React Application).

---

## 1. Backend Deployment (Render)

### Step 1: Create a PostgreSQL Database on Render
1. Log in to [Render](https://dashboard.render.com/).
2. Click **New +** and select **PostgreSQL**.
3. Configure the database:
   - **Name**: `nutriguard-db`
   - **Database**: `nutriguard`
   - **User**: `nutriguard_user`
   - **Region**: Choose closest to target users (e.g., Singapore / Frankfurt)
   - **Plan**: Free or Starter
4. Click **Create Database**.
5. Copy the **Internal Database URL** (or **External Database URL** if deploying across providers).
   > **Note:** Render PostgreSQL URLs start with `postgres://`. NutriGuard's `backend/core/database.py` automatically normalizes this to `postgresql://` for SQLAlchemy compatibility.

---

### Step 2: Deploy Backend as a Render Web Service
1. In the Render Dashboard, click **New +** and select **Web Service**.
2. Connect your Git repository (`https://github.com/Cy-prog/nutriguard`).
3. Fill in the service configuration:
   - **Name**: `nutriguard-api`
   - **Region**: Same region as the database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     python migrate_and_seed.py && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
     > `migrate_and_seed.py` linearizes and executes all 5 Alembic database migrations up to head (`a7b2c3d4e5f6`) and idempotently seeds Indian food profiles, medications, conditions, and meals before booting Uvicorn.

---

### Step 3: Configure Backend Environment Variables
In the Render Web Service settings, navigate to **Environment** and add:

| Key | Value | Description |
|---|---|---|
| `DATABASE_URL` | `<Your Render PostgreSQL URL>` | PostgreSQL connection string |
| `JWT_SECRET` | `<Generate random 32+ char string>` | Key used for signing JWT tokens |
| `JWT_ALGORITHM` | `HS256` | Token hashing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` | 7-day token expiration |
| `GEMINI_API_KEY` | `<Your Google Gemini API Key>` | Optional: Enables Gemini Flash AI features |
| `ENVIRONMENT` | `production` | Sets production mode |
| `CORS_ORIGINS` | `https://nutriguard.vercel.app,http://localhost:5173` | Allowed frontend domains (comma-separated string or JSON array) |

---

### Step 4: Configure Health Check Path
Under **Advanced Settings** in Render:
- **Health Check Path**: `/health`
- Expected response: `200 OK` with JSON:
  ```json
  {
    "status": "UP",
    "database": "UP",
    "ai": "CONFIGURED",
    "version": "2.0.0"
  }
  ```

---

## 2. Frontend Deployment (Vercel)

### Step 1: Import Project into Vercel
1. Log in to [Vercel](https://vercel.com/).
2. Click **Add New...** -> **Project**.
3. Select the `nutriguard` repository.

### Step 2: Configure Build Settings
- **Framework Preset**: `Vite`
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 3: Configure SPA Routing (`vercel.json`)
Ensure `frontend/vercel.json` exists with rewrite rules to proxy API requests to Render and handle React Router client-side routes:

```json
{
  "rewrites": [
    {
      "source": "/api/v1/:path*",
      "destination": "https://nutriguard-api.onrender.com/api/v1/:path*"
    },
    {
      "source": "/health",
      "destination": "https://nutriguard-api.onrender.com/health"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

Replace `https://nutriguard-api.onrender.com` with your actual Render service URL.

---

## 3. Post-Deployment Verification Checklist

- [ ] **Health Endpoint**: Navigate to `https://<backend-url>/health` and ensure `"database": "UP"`.
- [ ] **Swagger Documentation**: Open `https://<backend-url>/docs` and verify all endpoints load.
- [ ] **User Registration & Login**: Test user registration and JWT login via the frontend UI.
- [ ] **Meal Plan Generation**: Verify that generating a daily plan returns authentic Indian meals with valid macro rollups.
- [ ] **Clinical Safety Simulator**: Navigate to `/admin` on the frontend and run a simulation (e.g. Warfarin + Spinach) to verify deterministic veto enforcement.
- [ ] **Food Database Explorer**: Verify `/foods` displays the 60+ Indian food profiles from ICMR-NIN IFCT 2017.
- [ ] **AI Assistant**: Test a natural language food query at `/assistant`.
