from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import date, timedelta
import random

from models.meal import Meal
from models.meal_plan import DailyMealPlan, DailyMealPlanItem
from models.user import UserProfile, UserCondition, UserMedication, UserAllergy
from models.food import Allergen

from engines.nutrition_engine import NutritionEngine, NutritionTargets
from engines.meal_safety_engine import MealSafetyEngine
from engines.diversity_engine import DiversityEngine
from engines.portion_engine import PortionEngine
from engines.scoring.meal_scorer import score_meal

class RecommendationEngine:
    def __init__(self, db_session):
        self.db = db_session
        self.nutrition_engine = NutritionEngine()
        self.meal_safety_engine = MealSafetyEngine(db_session)
        self.diversity_engine = DiversityEngine()
        self.portion_engine = PortionEngine()

    def _build_user_context(self, user_id: UUID, profile: UserProfile) -> dict:
        conditions = self.db.query(UserCondition).filter(UserCondition.user_id == user_id).all()
        medications = self.db.query(UserMedication).filter(UserMedication.user_id == user_id).all()
        allergies = self.db.query(UserAllergy).filter(UserAllergy.user_id == user_id).all()

        cond_list = [{'name': c.notes or 'Unknown'} for c in conditions] # Simplifying, relies on rule engine structure
        med_list = [{'generic_name': m.notes or 'Unknown'} for m in medications] # Simplifying

        allergy_names = []
        for a in allergies:
            if a.allergen_id:
                allergen = self.db.query(Allergen).filter(Allergen.allergen_id == a.allergen_id).first()
                if allergen:
                    allergy_names.append(allergen.name)
            elif a.notes:
                allergy_names.append(a.notes)

        return {
            'diet_type': profile.diet_type,
            'allergies': allergy_names,
            'conditions': cond_list,
            'medications': med_list,
            'disliked_foods': profile.disliked_foods or [],
            'favorite_foods': profile.favorite_foods or []
        }

    def generate_daily_plan(self, user_id: UUID, target_date: date) -> Optional[DailyMealPlan]:
        profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id, UserProfile.is_current == True).first()
        if not profile:
            return None

        user_context = self._build_user_context(user_id, profile)
        targets = self.nutrition_engine.calculate_targets(profile)
        
        all_meals = self.db.query(Meal).filter(Meal.is_active == True).all()
        if not all_meals:
            return None

        safe_meals = self.meal_safety_engine.filter_safe_meals(user_context, all_meals)
        
        selected_meals = {}
        for meal_type in ['BREAKFAST', 'LUNCH', 'DINNER', 'SNACK']:
            candidates = [m for m in safe_meals if m.meal_type == meal_type]
            if not candidates:
                continue
                
            cal_target = self.nutrition_engine.get_meal_calorie_target(targets, meal_type)
            prot_target = self.nutrition_engine.get_meal_protein_target(targets, meal_type)
            
            scored_candidates = []
            for c in candidates:
                score = score_meal(c, cal_target, prot_target, user_context)
                scored_candidates.append((c, score))
            
            scored_candidates.sort(key=lambda x: x[1], reverse=True)
            
            top_candidates = [c[0] for c in scored_candidates[:10]]
            diverse_cands = self.diversity_engine.filter_diverse_candidates(top_candidates, list(selected_meals.values()))
            
            if diverse_cands:
                selected_meals[meal_type] = diverse_cands[0]
            elif top_candidates:
                selected_meals[meal_type] = top_candidates[0]

        plan = DailyMealPlan(
            user_id=user_id,
            date=target_date,
            target_calories=targets.target_calories,
            target_protein_g=targets.protein_g,
            target_carbs_g=targets.carbs_g,
            target_fat_g=targets.fat_g,
            target_fiber_g=targets.fiber_g,
            actual_calories=0, actual_protein_g=0, actual_carbs_g=0, actual_fat_g=0, actual_fiber_g=0
        )
        self.db.add(plan)
        self.db.flush()

        for m_type, meal in selected_meals.items():
            cal_target = self.nutrition_engine.get_meal_calorie_target(targets, m_type)
            prot_target = self.nutrition_engine.get_meal_protein_target(targets, m_type)
            portioned = self.portion_engine.calculate_portion(meal, cal_target, prot_target)
            
            item = DailyMealPlanItem(
                plan_id=plan.plan_id,
                meal_id=meal.meal_id,
                meal_type=m_type,
                servings=1.0,
                portion_multiplier=portioned.portion_multiplier,
                calories=portioned.calories,
                protein_g=portioned.protein_g,
                carbs_g=portioned.carbs_g,
                fat_g=portioned.fat_g,
                fiber_g=portioned.fiber_g,
                recommendation_score=85.0
            )
            self.db.add(item)
            
            plan.actual_calories = float(plan.actual_calories or 0) + portioned.calories
            plan.actual_protein_g = float(plan.actual_protein_g or 0) + portioned.protein_g
            plan.actual_carbs_g = float(plan.actual_carbs_g or 0) + portioned.carbs_g
            plan.actual_fat_g = float(plan.actual_fat_g or 0) + portioned.fat_g
            plan.actual_fiber_g = float(plan.actual_fiber_g or 0) + portioned.fiber_g

        self.db.commit()
        return plan

    def randomize_meal(self, user_id: UUID, current_meal_type: str, all_safe_meals: list, user_context: dict) -> Optional[Meal]:
        candidates = [m for m in all_safe_meals if m.meal_type == current_meal_type]
        if not candidates:
            return None
            
        return random.choice(candidates)

    def generate_weekly_plan(self, user_id: UUID, start_date: date) -> List[DailyMealPlan]:
        plans = []
        for i in range(7):
            plan_date = start_date + timedelta(days=i)
            plan = self.generate_daily_plan(user_id, plan_date)
            if plan:
                plans.append(plan)
        return plans
