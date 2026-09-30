from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from engines.safety_engine import SafetyEngine
from engines.rule_engine import RuleEngine
# In a real app we would depend on get_db
# from core.database import get_db

from api.deps import get_current_user
from models.user import User

router = APIRouter()

from core.database import get_db
from services.recommendation_service import RecommendationService

@router.post("/evaluate/{food_id}")
async def evaluate_food(
    food_id: UUID, 
    user_context: Dict[str, Any], 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Evaluates a specific food against the user's clinical context.
    """
    service = RecommendationService(db)
    det_results = await service.generate_recommendations(user_context, [food_id])
    
    if not det_results or not det_results.get("foods"):
        raise HTTPException(status_code=404, detail="Food item not found or evaluation failed")
        
    res = det_results["foods"][0]
    return {
        "food_id": str(food_id),
        "classification": res.get("classification"),
        "explanation": res.get("explanation") or res.get("reason"),
        "fired_rules": res.get("fired_rules", []),
        "interactions": res.get("interactions", [])
    }

from core.database import get_db
from api.schemas.meal_schemas import DayPlanResponse, NutrientGapResponse
from core.exceptions import UserProfileIncompleteError, FoodPoolEmptyError
from services.recommendation_service import RecommendationService
import logging
logger = logging.getLogger(__name__)

@router.post("/meals/generate", response_model=DayPlanResponse)
async def generate_meal_plan(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate a full day meal plan for the authenticated user.
    Runs the complete deterministic pipeline:
      targets → pool → meals → timing → gaps → safety validation
    """
    try:
        recommendation_service = RecommendationService(db)
        plan = await recommendation_service.generate_day_plan(
            user_id=current_user.user_id
        )
        return plan
    except UserProfileIncompleteError:
        raise HTTPException(
            status_code=422,
            detail="Profile incomplete. Please add at least one "
                   "condition or medication before generating a plan."
        )
    except FoodPoolEmptyError:
        raise HTTPException(
            status_code=422,
            detail="No safe foods could be identified for your current "
                   "profile. Please review your conditions and allergies, "
                   "or consult a dietitian."
        )
    except Exception as e:
        logger.error(f"Meal plan generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Meal plan generation failed. Your profile has "
                   "not been changed."
        )

@router.get("/meals/{plan_id}/gaps", response_model=NutrientGapResponse)
async def get_meal_gaps(
    plan_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve the nutrient gap report for a stored meal plan.
    """
    from models.meal_plan import MealPlan
    plan = db.query(MealPlan).filter(
        MealPlan.id == plan_id,
        MealPlan.user_id == current_user.user_id
    ).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return plan.gap_report

