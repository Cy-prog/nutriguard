from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.routes import recommendations, nlp, chat, auth, admin
from api.routes import profile, meal_plan, meals, grocery, admin_meals, foods
from core.config import settings
from core.logging import logger
from sqlalchemy import text
import uuid

app = FastAPI(
    title="NutriGuard AI API",
    description="AI-Powered Personalized Diet & Medication Nutrition System with Indian Meal Planning",
    version="2.0.0",
    # Disable docs in production for security
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# CORS — use the properly parsed origins list
origins = settings.cors_origins_list
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    req_id = str(uuid.uuid4())
    logger.error(
        f"Unhandled exception: {type(exc).__name__}",
        extra={"request_id": req_id, "endpoint": request.url.path},
        exc_info=True
    )
    # Never leak internal details to clients
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later."
            },
            "request_id": req_id
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Existing routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"]
)

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["recommendations"]
)

app.include_router(
    nlp.router,
    prefix="/api/v1/nlp",
    tags=["nlp"]
)

app.include_router(
    chat.router,
    prefix="/api/v1/chat",
    tags=["chat"]
)

app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["admin"]
)

# Meal planning routers
app.include_router(
    profile.router,
    prefix="/api/v1/me",
    tags=["profile"]
)
app.include_router(
    profile.router,
    prefix="/api/v1",
    tags=["profile-compat"]
)

app.include_router(
    meal_plan.router,
    prefix="/api/v1/me/meal-plan",
    tags=["meal-plan"]
)
app.include_router(
    meal_plan.router,
    prefix="/api/v1/meal-plan",
    tags=["meal-plan-compat"]
)

app.include_router(
    meals.router,
    prefix="/api/v1/meals",
    tags=["meals"]
)

app.include_router(
    foods.router,
    prefix="/api/v1/foods",
    tags=["foods"]
)
app.include_router(
    foods.router,
    prefix="/api/foods",
    tags=["foods-compat"]
)

app.include_router(
    meals.router,
    prefix="/api/v1/recipes",
    tags=["recipes"]
)
app.include_router(
    meals.router,
    prefix="/api/recipes",
    tags=["recipes-compat"]
)

app.include_router(
    grocery.router,
    prefix="/api/v1/me/grocery",
    tags=["grocery"]
)
app.include_router(
    grocery.router,
    prefix="/api/v1/grocery",
    tags=["grocery-compat"]
)

app.include_router(
    admin_meals.router,
    prefix="/api/v1/admin/meals",
    tags=["admin-meals"]
)

@app.get("/health")
@app.get("/api/v1/health")
def health_check():
    """Basic application health check for Render/monitoring."""
    from core.database import SessionLocal
    db_status = "UP"
    db = None
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "DOWN"
    finally:
        if db:
            db.close()
        
    ai_status = "CONFIGURED" if settings.GEMINI_API_KEY else "KEYWORD_FALLBACK"
    return {
        "status": "UP" if db_status == "UP" else "DEGRADED",
        "database": db_status,
        "ai": ai_status,
        "version": "2.0.0"
    }

@app.get("/health/ready")
@app.get("/api/v1/health/ready")
def readiness_check():
    """Readiness probe — verifies database connectivity."""
    from core.database import SessionLocal
    db = None
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "healthy"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")
    finally:
        if db:
            db.close()

@app.get("/")
def read_root():
    return {
        "name": "NutriGuard AI API",
        "version": "2.0.0",
        "description": "Production-Grade AI Nutrition & Indian Meal Recommendation Platform",
        "docs_url": "/docs" if settings.ENVIRONMENT != "production" else None
    }
