from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from api.schemas.meal import ProfileUpdate, ProfileResponse, NutritionTargetsResponse
from models.user import User, UserProfile
from engines.nutrition_engine import NutritionEngine

router = APIRouter()


@router.get("/profile", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.user_id,
        UserProfile.is_current == True
    ).first()
    
    if not profile:
        # Create default profile
        profile = UserProfile(user_id=current_user.user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return profile


@router.put("/profile", response_model=ProfileResponse)
def update_my_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.user_id,
        UserProfile.is_current == True
    ).first()
    
    if not profile:
        profile = UserProfile(user_id=current_user.user_id)
        db.add(profile)
        db.flush()
    
    update_data = profile_data.model_dump(exclude_unset=True, exclude={'allergies', 'conditions', 'medications'})
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/targets", response_model=NutritionTargetsResponse)
@router.get("/profile/targets", response_model=NutritionTargetsResponse)
@router.get("/nutrition-targets", response_model=NutritionTargetsResponse)
def get_nutrition_targets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.user_id,
        UserProfile.is_current == True
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Complete onboarding first.")
    
    if not profile.weight_kg or not profile.height_cm or not profile.age:
        raise HTTPException(status_code=400, detail="Profile incomplete. Age, height, and weight are required.")
    
    engine = NutritionEngine()
    targets = engine.calculate_targets(profile)
    
    return NutritionTargetsResponse(
        bmi=targets.bmi,
        bmr=targets.bmr,
        tdee=targets.tdee,
        target_calories=targets.target_calories,
        daily_calories=targets.target_calories,
        protein_g=targets.protein_g,
        daily_protein_g=targets.protein_g,
        carbs_g=targets.carbs_g,
        daily_carbs_g=targets.carbs_g,
        fat_g=targets.fat_g,
        daily_fat_g=targets.fat_g,
        fiber_g=targets.fiber_g,
        daily_fiber_g=targets.fiber_g,
        water_ml=targets.water_ml,
        calcium_mg=targets.calcium_mg,
        iron_mg=targets.iron_mg,
        vitamin_c_mg=targets.vitamin_c_mg,
        vitamin_d_mcg=targets.vitamin_d_mcg,
        vitamin_b12_mcg=targets.vitamin_b12_mcg,
        folate_mcg=targets.folate_mcg,
        meal_distribution=targets.meal_distribution,
        disclaimer=targets.disclaimer
    )
