from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user
from api.schemas.meal import ProfileUpdate, ProfileResponse, NutritionTargetsResponse
from models.user import User, UserProfile
from engines.nutrition_engine import NutritionEngine

router = APIRouter()


def _build_profile_response(profile: UserProfile, db: Session, user_id) -> ProfileResponse:
    from models.user import UserAllergy, UserCondition, UserMedication
    from models.food import Allergen
    from models.condition import Condition
    from models.medication import Medication

    u_algs = db.query(UserAllergy).filter_by(user_id=user_id).all()
    allergy_names = []
    for ua in u_algs:
        if ua.allergen_id:
            a = db.query(Allergen).filter_by(allergen_id=ua.allergen_id).first()
            if a:
                allergy_names.append(a.name)
        elif ua.notes:
            allergy_names.append(ua.notes)

    u_conds = db.query(UserCondition).filter_by(user_id=user_id).all()
    cond_list = []
    for uc in u_conds:
        c = db.query(Condition).filter_by(condition_id=uc.condition_id).first()
        cond_list.append({
            "name": c.name if c else (uc.notes or "Unknown"),
            "severity": uc.severity,
            "disease_stage": uc.disease_stage,
            "lab_values": uc.lab_values or {}
        })

    u_meds = db.query(UserMedication).filter_by(user_id=user_id).all()
    med_list = []
    for um in u_meds:
        m = db.query(Medication).filter_by(medication_id=um.medication_id).first()
        med_list.append({
            "name": m.generic_name if m else (um.notes or "Unknown"),
            "dose": f"{um.dose_amount} {um.dose_unit}" if um.dose_amount else None,
            "timing": um.timing_relative_to_meal
        })

    res = ProfileResponse.model_validate(profile)
    res.allergies = allergy_names
    res.conditions = cond_list
    res.medications = med_list
    res.health_conditions = ", ".join([c["name"] for c in cond_list]) if cond_list else None
    res.disliked_ingredients = profile.disliked_foods or []
    res.goal = profile.fitness_goal
    res.region_preference = profile.regional_preference
    return res


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
        profile = UserProfile(user_id=current_user.user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return _build_profile_response(profile, db, current_user.user_id)


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
    
    # Map compatibility fields if provided
    if profile_data.goal and not profile_data.fitness_goal:
        profile.fitness_goal = profile_data.goal
    if profile_data.region_preference and not profile_data.regional_preference:
        profile.regional_preference = profile_data.region_preference
    if profile_data.disliked_ingredients and not profile_data.disliked_foods:
        profile.disliked_foods = profile_data.disliked_ingredients

    update_data = profile_data.model_dump(
        exclude_unset=True, 
        exclude={'allergies', 'conditions', 'medications', 'health_conditions', 'goal', 'region_preference', 'disliked_ingredients'}
    )
    for field, value in update_data.items():
        setattr(profile, field, value)

    # Health data updates
    from models.user import UserAllergy, UserCondition, UserMedication
    from models.food import Allergen
    from models.condition import Condition
    from models.medication import Medication

    # 1. Allergies
    if profile_data.allergies is not None:
        db.query(UserAllergy).filter_by(user_id=current_user.user_id).delete()
        for alg_name in profile_data.allergies:
            norm_name = alg_name.strip().lower()
            if not norm_name:
                continue
            allergen = db.query(Allergen).filter(Allergen.name.ilike(norm_name)).first()
            if not allergen:
                allergen = Allergen(name=norm_name)
                db.add(allergen)
                db.flush()
            db.add(UserAllergy(
                user_id=current_user.user_id,
                allergen_id=allergen.allergen_id,
                confirmed=True,
                notes=alg_name.strip()
            ))

    # 2. Health conditions
    conds_to_process = []
    if profile_data.conditions is not None:
        conds_to_process = profile_data.conditions
    elif profile_data.health_conditions is not None:
        for c_str in profile_data.health_conditions.split(","):
            if c_str.strip():
                conds_to_process.append({"name": c_str.strip()})

    if profile_data.conditions is not None or profile_data.health_conditions is not None:
        db.query(UserCondition).filter_by(user_id=current_user.user_id).delete()
        for c_item in conds_to_process:
            c_name = c_item.get("name", "").strip() if isinstance(c_item, dict) else str(c_item).strip()
            if not c_name:
                continue
            cond = db.query(Condition).filter(Condition.name.ilike(c_name)).first()
            if not cond:
                cond = Condition(name=c_name)
                db.add(cond)
                db.flush()
            db.add(UserCondition(
                user_id=current_user.user_id,
                condition_id=cond.condition_id,
                severity=c_item.get("severity") if isinstance(c_item, dict) else None,
                disease_stage=c_item.get("disease_stage") if isinstance(c_item, dict) else None,
                lab_values=c_item.get("lab_values", {}) if isinstance(c_item, dict) else {},
                diagnosed=True,
                notes=c_name
            ))

    # 3. Medications
    if profile_data.medications is not None:
        db.query(UserMedication).filter_by(user_id=current_user.user_id).delete()
        for m_item in profile_data.medications:
            m_name = m_item.get("name", "").strip() if isinstance(m_item, dict) else str(m_item).strip()
            if not m_name:
                continue
            med = db.query(Medication).filter(Medication.generic_name.ilike(m_name)).first()
            if not med:
                med = Medication(generic_name=m_name)
                db.add(med)
                db.flush()
            db.add(UserMedication(
                user_id=current_user.user_id,
                medication_id=med.medication_id,
                notes=m_name
            ))
    
    db.commit()
    db.refresh(profile)
    return _build_profile_response(profile, db, current_user.user_id)


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
