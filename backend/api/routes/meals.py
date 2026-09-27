from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
from typing import Optional, List
import re

from api.deps import get_db, get_current_user
from api.schemas.meal import MealListResponse, MealDetail, MealSummary, MealNutritionResponse, MealVideoResponse
from models.user import User
from models.meal import Meal, MealIngredient, MealAllergen, Ingredient
from models.food import Allergen

router = APIRouter()

@router.get("/", response_model=MealListResponse)
def list_meals(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    meal_type: Optional[str] = None,
    cuisine_region: Optional[str] = None,
    diet: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Meal).filter(Meal.is_active == True)
    
    if meal_type:
        query = query.filter(Meal.meal_type == meal_type.upper())
    if cuisine_region:
        query = query.filter(Meal.cuisine_region == cuisine_region.upper())
        
    if diet:
        d = diet.lower()
        if d == "vegetarian":
            query = query.filter(Meal.is_vegetarian == True)
        elif d == "vegan":
            query = query.filter(Meal.is_vegan == True)
        elif d == "jain":
            query = query.filter(Meal.is_jain_friendly == True)
        elif d == "non_veg":
            query = query.filter(Meal.is_vegetarian == False)
        elif d == "eggetarian":
            query = query.filter(Meal.is_egg_based == True)
            
    if search:
        search_filter = f"%{search}%"
        query = query.filter(or_(
            Meal.name.ilike(search_filter),
            Meal.local_name.ilike(search_filter),
            Meal.description.ilike(search_filter)
        ))
        
    # tags filtering is omitted for simplicity unless using postgres array/jsonb operators
    
    if sort_by:
        if sort_by == "calories":
            query = query.order_by(Meal.calories)
        elif sort_by == "protein":
            query = query.order_by(Meal.protein_g.desc())
        elif sort_by == "name":
            query = query.order_by(Meal.name)
            
    total = query.count()
    meals = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return MealListResponse(
        meals=[MealSummary.model_validate(m) for m in meals],
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/{meal_id}", response_model=MealDetail)
def get_meal(
    meal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id, Meal.is_active == True).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    detail = MealDetail.model_validate(meal)
    
    # Allergens
    allergen_names = []
    for ma in meal.allergens:
        if ma.allergen:
            allergen_names.append(ma.allergen.name)
    detail.allergen_warnings = allergen_names
    
    return detail

@router.get("/{meal_id}/recipe", response_model=MealDetail)
def get_meal_recipe(
    meal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_meal(meal_id, db, current_user)

@router.get("/{meal_id}/nutrition", response_model=MealNutritionResponse)
def get_meal_nutrition(
    meal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id, Meal.is_active == True).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    return MealNutritionResponse.model_validate(meal)

@router.get("/{meal_id}/video", response_model=MealVideoResponse)
def get_meal_video(
    meal_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id, Meal.is_active == True).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    embed_url = None
    if meal.video_url:
        # Check youtube url
        youtube_regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(youtube_regex, meal.video_url)
        if match:
            video_id = match.group(1)
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            
    return MealVideoResponse(
        meal_id=meal.meal_id,
        name=meal.name,
        video_url=meal.video_url,
        embed_url=embed_url,
        available=bool(embed_url or meal.video_url)
    )
