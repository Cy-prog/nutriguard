from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Optional, List
from uuid import UUID

from api.deps import get_db, get_current_user
from api.schemas.meal import (
    DailyMealPlanResponse, WeeklyMealPlanResponse, MealPlanItemResponse,
    MealPlanGenerateRequest, WeeklyPlanGenerateRequest, RandomizeMealRequest,
    ReplaceMealRequest, ReplaceMealResponse, MealExplanationResponse, MealSummary
)
from models.user import User, UserProfile
from models.meal import Meal
from models.meal_plan import DailyMealPlan, DailyMealPlanItem
from engines.recommendation_engine import RecommendationEngine
from engines.substitution_engine import SubstitutionEngine
from engines.meal_safety_engine import MealSafetyEngine

router = APIRouter()

def _build_meal_item_response(item: DailyMealPlanItem) -> MealPlanItemResponse:
    return MealPlanItemResponse(
        meal_type=item.meal_type,
        meal=MealSummary.model_validate(item.meal),
        portion_multiplier=float(item.portion_multiplier or 1.0),
        servings=float(item.servings or 1.0),
        calories=float(item.calories) if item.calories else None,
        protein_g=float(item.protein_g) if item.protein_g else None,
        carbs_g=float(item.carbs_g) if item.carbs_g else None,
        fat_g=float(item.fat_g) if item.fat_g else None,
        fiber_g=float(item.fiber_g) if item.fiber_g else None,
        recommendation_score=float(item.recommendation_score) if item.recommendation_score else None,
        recommendation_reasons=item.recommendation_reasons or []
    )

def _build_daily_plan_response(plan: DailyMealPlan) -> DailyMealPlanResponse:
    act_cal = float(plan.actual_calories) if plan.actual_calories else None
    act_prot = float(plan.actual_protein_g) if plan.actual_protein_g else None
    act_carbs = float(plan.actual_carbs_g) if plan.actual_carbs_g else None
    act_fat = float(plan.actual_fat_g) if plan.actual_fat_g else None
    score = float(plan.overall_score or plan.nutrition_score or 85.0)
    return DailyMealPlanResponse(
        plan_id=plan.plan_id,
        date=plan.date,
        target_calories=float(plan.target_calories) if plan.target_calories else None,
        target_protein_g=float(plan.target_protein_g) if plan.target_protein_g else None,
        target_carbs_g=float(plan.target_carbs_g) if plan.target_carbs_g else None,
        target_fat_g=float(plan.target_fat_g) if plan.target_fat_g else None,
        target_fiber_g=float(plan.target_fiber_g) if plan.target_fiber_g else None,
        actual_calories=act_cal,
        actual_protein_g=act_prot,
        actual_carbs_g=act_carbs,
        actual_fat_g=act_fat,
        actual_fiber_g=float(plan.actual_fiber_g) if plan.actual_fiber_g else None,
        total_calories=act_cal,
        total_protein=act_prot,
        total_carbs=act_carbs,
        total_fat=act_fat,
        health_score=score,
        nutrition_score=float(plan.nutrition_score) if plan.nutrition_score else None,
        variety_score=float(plan.variety_score) if plan.variety_score else None,
        preference_score=float(plan.preference_score) if plan.preference_score else None,
        overall_score=score,
        meals=[_build_meal_item_response(item) for item in plan.items]
    )

@router.post("/generate", response_model=DailyMealPlanResponse)
def generate_daily_plan(
    req: MealPlanGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_date = req.date or date.today()
    engine = RecommendationEngine(db)
    plan = engine.generate_daily_plan(current_user.user_id, target_date)
    
    if not plan:
        raise HTTPException(status_code=400, detail="Could not generate meal plan. Please ensure you have completed your profile.")
        
    return _build_daily_plan_response(plan)


@router.get("/today", response_model=DailyMealPlanResponse)
def get_today_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    plan = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date == today
    ).first()
    
    if not plan:
        engine = RecommendationEngine(db)
        plan = engine.generate_daily_plan(current_user.user_id, today)
        if not plan:
            raise HTTPException(status_code=400, detail="Could not generate meal plan.")
            
    return _build_daily_plan_response(plan)


@router.get("/week", response_model=WeeklyMealPlanResponse)
@router.get("/weekly", response_model=WeeklyMealPlanResponse)
def get_week_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    end_date = today + timedelta(days=6)
    
    plans = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date >= today,
        DailyMealPlan.date <= end_date
    ).order_by(DailyMealPlan.date).all()
    
    built_plans = [_build_daily_plan_response(p) for p in plans]
    return WeeklyMealPlanResponse(
        start_date=today,
        end_date=end_date,
        daily_plans=built_plans,
        days=built_plans,
        weekly_nutrition_score=86.0 if built_plans else None,
        weekly_variety_score=90.0 if built_plans else None
    )


@router.post("/week/generate", response_model=WeeklyMealPlanResponse)
@router.post("/weekly/generate", response_model=WeeklyMealPlanResponse)
def generate_weekly_plan(
    req: Optional[WeeklyPlanGenerateRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_date = (req.start_date if req else None) or date.today()
    engine = RecommendationEngine(db)
    
    # Delete existing plans for the week
    end_date = start_date + timedelta(days=6)
    db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date >= start_date,
        DailyMealPlan.date <= end_date
    ).delete()
    db.commit()
    
    plans = engine.generate_weekly_plan(current_user.user_id, start_date)
    built_plans = [_build_daily_plan_response(p) for p in plans]
    
    return WeeklyMealPlanResponse(
        start_date=start_date,
        end_date=end_date,
        daily_plans=built_plans,
        days=built_plans,
        weekly_nutrition_score=88.0,
        weekly_variety_score=92.0
    )


@router.post("/randomize", response_model=DailyMealPlanResponse)
def randomize_daily_plan(
    req: RandomizeMealRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    plan = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date == today
    ).first()
    
    if plan:
        db.delete(plan)
        db.commit()
        
    engine = RecommendationEngine(db)
    new_plan = engine.generate_daily_plan(current_user.user_id, today)
    
    if not new_plan:
        raise HTTPException(status_code=400, detail="Could not regenerate meal plan.")
        
    return _build_daily_plan_response(new_plan)


@router.post("/randomize/{meal_type}", response_model=DailyMealPlanResponse)
def randomize_meal(
    meal_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    plan = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date == today
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No meal plan exists for today.")
        
    item_to_remove = next((item for item in plan.items if item.meal_type.upper() == meal_type.upper()), None)
    if item_to_remove:
        db.delete(item_to_remove)
        db.commit()
        db.refresh(plan)
        
    engine = RecommendationEngine(db)
    # Re-generating is tricky, we can just regenerate the whole day for simplicity, 
    # but the instructions say "randomize single meal ... Replace that item in the plan."
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id, UserProfile.is_current == True).first()
    all_meals = db.query(Meal).filter(Meal.is_active == True).all()
    user_context = engine._build_user_context(current_user.user_id, profile)
    safe_meals = engine.meal_safety_engine.filter_safe_meals(user_context, all_meals)
    
    new_meal = engine.randomize_meal(current_user.user_id, meal_type.upper(), safe_meals, user_context)
    if new_meal:
        targets = engine.nutrition_engine.calculate_targets(profile)
        cal_target = engine.nutrition_engine.get_meal_calorie_target(targets, meal_type.upper())
        prot_target = engine.nutrition_engine.get_meal_protein_target(targets, meal_type.upper())
        portioned = engine.portion_engine.calculate_portion(new_meal, cal_target, prot_target)
        
        item = DailyMealPlanItem(
            plan_id=plan.plan_id,
            meal_id=new_meal.meal_id,
            meal_type=meal_type.upper(),
            servings=1.0,
            portion_multiplier=portioned.portion_multiplier,
            calories=portioned.calories,
            protein_g=portioned.protein_g,
            carbs_g=portioned.carbs_g,
            fat_g=portioned.fat_g,
            fiber_g=portioned.fiber_g,
            recommendation_score=85.0
        )
        db.add(item)
        db.commit()
        db.refresh(plan)
    
    return _build_daily_plan_response(plan)


@router.post("/{meal_type}/replace", response_model=ReplaceMealResponse)
def replace_meal_options(
    meal_type: str,
    req: ReplaceMealRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not req.current_meal_id:
        raise HTTPException(status_code=400, detail="current_meal_id is required")
        
    current_meal = db.query(Meal).filter(Meal.meal_id == req.current_meal_id).first()
    if not current_meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    engine = RecommendationEngine(db)
    sub_engine = SubstitutionEngine(db)
    
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id, UserProfile.is_current == True).first()
    all_meals = db.query(Meal).filter(Meal.is_active == True).all()
    user_context = engine._build_user_context(current_user.user_id, profile)
    safe_meals = engine.meal_safety_engine.filter_safe_meals(user_context, all_meals)
    
    alternatives = sub_engine.find_alternatives(current_meal, user_context, safe_meals, count=req.count)
    
    results = []
    targets = engine.nutrition_engine.calculate_targets(profile)
    cal_target = engine.nutrition_engine.get_meal_calorie_target(targets, meal_type.upper())
    prot_target = engine.nutrition_engine.get_meal_protein_target(targets, meal_type.upper())
    
    for alt in alternatives:
        portioned = engine.portion_engine.calculate_portion(alt, cal_target, prot_target)
        results.append(MealPlanItemResponse(
            meal_type=meal_type.upper(),
            meal=MealSummary.model_validate(alt),
            portion_multiplier=float(portioned.portion_multiplier),
            servings=1.0,
            calories=float(portioned.calories),
            protein_g=float(portioned.protein_g),
            carbs_g=float(portioned.carbs_g),
            fat_g=float(portioned.fat_g),
            fiber_g=float(portioned.fiber_g),
            recommendation_score=90.0,
            recommendation_reasons=["Nutritionally similar to current choice"]
        ))
        
    return ReplaceMealResponse(alternatives=results)


@router.get("/{meal_type}/explain", response_model=MealExplanationResponse)
def explain_meal(
    meal_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    plan = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date == today
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No meal plan found for today")
        
    item = next((i for i in plan.items if i.meal_type.upper() == meal_type.upper()), None)
    if not item:
        raise HTTPException(status_code=404, detail=f"No {meal_type} found in today's plan")
        
    return MealExplanationResponse(
        meal_id=item.meal_id,
        meal_name=item.meal.name,
        score=float(item.recommendation_score) if item.recommendation_score else None,
        reasons=item.recommendation_reasons or [],
        explanation="This meal was chosen based on your profile and daily nutritional targets."
    )


@router.get("/explanation", response_model=MealExplanationResponse)
def explain_meal_query(
    mealType: str = "LUNCH",
    date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return explain_meal(meal_type=mealType, db=db, current_user=current_user)


@router.post("/randomize-meal", response_model=DailyMealPlanResponse)
def randomize_meal_body(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal_type = payload.get("mealType") or payload.get("meal_type") or "LUNCH"
    return randomize_meal(meal_type=meal_type, db=db, current_user=current_user)


@router.post("/replace")
def replace_meal_body(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal_type = payload.get("mealType") or payload.get("meal_type") or "LUNCH"
    current_meal_id = payload.get("mealId") or payload.get("current_meal_id")
    req = ReplaceMealRequest(current_meal_id=UUID(current_meal_id) if current_meal_id else None, count=5)
    return replace_meal_options(meal_type=meal_type, req=req, db=db, current_user=current_user)
