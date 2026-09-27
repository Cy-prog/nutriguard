from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from collections import defaultdict
from typing import List

from api.deps import get_db, get_current_user
from api.schemas.meal import GroceryListResponse, GroceryItem
from models.user import User
from models.meal_plan import DailyMealPlan, DailyMealPlanItem
from models.meal import Meal, MealIngredient, Ingredient

router = APIRouter()

def _generate_grocery_list(items: List[DailyMealPlanItem], period: str, date_range: str) -> GroceryListResponse:
    grocery_map = defaultdict(lambda: {"total": 0.0, "local_name": None, "category": None})
    
    for item in items:
        if not item.meal:
            continue
            
        multiplier = float(item.portion_multiplier or 1.0)
        
        for mi in item.meal.ingredients:
            if not mi.ingredient:
                continue
                
            key = (mi.ingredient.name, mi.unit)
            qty = float(mi.quantity or 0.0) * multiplier
            
            grocery_map[key]["total"] += qty
            if not grocery_map[key]["local_name"] and mi.ingredient.local_name:
                grocery_map[key]["local_name"] = mi.ingredient.local_name
            if not grocery_map[key]["category"] and mi.ingredient.category:
                grocery_map[key]["category"] = mi.ingredient.category
                
    grocery_items = []
    for (name, unit), data in grocery_map.items():
        if data["total"] > 0:
            grocery_items.append(
                GroceryItem(
                    ingredient_name=name,
                    local_name=data["local_name"],
                    total_quantity=round(data["total"], 2),
                    unit=unit or "unit",
                    category=data["category"]
                )
            )
            
    # Sort by category then name
    grocery_items.sort(key=lambda x: (x.category or "Z", x.ingredient_name))
    
    return GroceryListResponse(
        period=period,
        date_range=date_range,
        items=grocery_items,
        total_items=len(grocery_items)
    )

@router.get("/daily", response_model=GroceryListResponse)
def get_daily_grocery_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    plan = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date == today
    ).first()
    
    items = plan.items if plan else []
    return _generate_grocery_list(items, "daily", str(today))

@router.get("/weekly", response_model=GroceryListResponse)
def get_weekly_grocery_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    end_date = today + timedelta(days=6)
    
    plans = db.query(DailyMealPlan).filter(
        DailyMealPlan.user_id == current_user.user_id,
        DailyMealPlan.date >= today,
        DailyMealPlan.date <= end_date
    ).all()
    
    items = []
    for plan in plans:
        items.extend(plan.items)
        
    date_range = f"{today} to {end_date}"
    return _generate_grocery_list(items, "weekly", date_range)
