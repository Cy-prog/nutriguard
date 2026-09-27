from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from api.deps import get_db, get_current_admin
from api.schemas.meal import MealCreateRequest, MealUpdateRequest, MealDetail
from models.user import User
from models.meal import Meal

router = APIRouter()

@router.post("/", response_model=MealDetail)
def create_meal(
    meal_data: MealCreateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    meal_dict = meal_data.model_dump(exclude_unset=True)
    meal = Meal(**meal_dict)
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return MealDetail.model_validate(meal)

@router.put("/{meal_id}", response_model=MealDetail)
def update_meal(
    meal_id: UUID,
    meal_data: MealUpdateRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    update_data = meal_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal, field, value)
        
    db.commit()
    db.refresh(meal)
    return MealDetail.model_validate(meal)

@router.delete("/{meal_id}")
def delete_meal(
    meal_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
        
    meal.is_active = False
    db.commit()
    
    return {"message": "Meal deleted successfully"}
