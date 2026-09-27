from typing import List, Dict, Any, Optional, Tuple
from uuid import UUID
from dataclasses import dataclass

@dataclass 
class MealSafetyResult:
    meal_id: UUID
    is_safe: bool
    rejection_reason: Optional[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

class MealSafetyEngine:
    def __init__(self, db_session):
        self.db = db_session
        from engines.safety_engine import SafetyEngine
        from engines.interaction_engine import InteractionEngine
        self.safety_engine = SafetyEngine(db_session)
        self.interaction_engine = InteractionEngine(db_session)
    
    def filter_safe_meals(self, user_context: dict, meals: list) -> list:
        safe = []
        for meal in meals:
            result = self.evaluate_meal_safety(user_context, meal)
            if result.is_safe:
                safe.append(meal)
        return safe
    
    def evaluate_meal_safety(self, user_context: dict, meal) -> MealSafetyResult:
        # 1. Dietary compatibility
        diet_check = self._check_dietary_compatibility(user_context, meal)
        if not diet_check[0]:
            return MealSafetyResult(meal_id=meal.meal_id, is_safe=False, rejection_reason=diet_check[1])
        
        # 2. Allergy check via meal allergens
        allergy_check = self._check_meal_allergies(user_context, meal)
        if not allergy_check[0]:
            return MealSafetyResult(meal_id=meal.meal_id, is_safe=False, rejection_reason=allergy_check[1])
        
        # 3. Check ingredient-level food safety (drug interactions, condition rules)
        ingredient_check = self._check_ingredient_safety(user_context, meal)
        if not ingredient_check[0]:
            return MealSafetyResult(meal_id=meal.meal_id, is_safe=False, rejection_reason=ingredient_check[1], warnings=ingredient_check[2])
        
        # 4. Check disliked foods
        dislike_check = self._check_disliked_foods(user_context, meal)
        if not dislike_check[0]:
            return MealSafetyResult(meal_id=meal.meal_id, is_safe=False, rejection_reason=dislike_check[1])
        
        return MealSafetyResult(meal_id=meal.meal_id, is_safe=True, warnings=ingredient_check[2] if len(ingredient_check) > 2 else [])
    
    def _check_dietary_compatibility(self, user_context: dict, meal) -> Tuple[bool, Optional[str]]:
        diet_type = user_context.get('diet_type', '').upper()
        if not diet_type:
            return (True, None)
        
        if diet_type == 'VEGETARIAN' and not meal.is_vegetarian:
            return (False, 'Non-vegetarian meal conflicts with vegetarian diet')
        if diet_type == 'VEGAN' and not meal.is_vegan:
            return (False, 'Non-vegan meal conflicts with vegan diet')
        if diet_type == 'JAIN' and not meal.is_jain_friendly:
            return (False, 'Meal not compatible with Jain dietary restrictions')
        if diet_type == 'EGGETARIAN':
            if not meal.is_vegetarian and not meal.is_egg_based:
                return (False, 'Non-vegetarian non-egg meal conflicts with eggetarian diet')
        return (True, None)
    
    def _check_meal_allergies(self, user_context: dict, meal) -> Tuple[bool, Optional[str]]:
        user_allergies = [a.lower() for a in user_context.get('allergies', [])]
        if not user_allergies:
            return (True, None)
        
        if not self.db:
            return (True, None)
            
        from models.meal import MealAllergen
        from models.food import Allergen
        meal_allergens = self.db.query(Allergen.name).join(MealAllergen).filter(
            MealAllergen.meal_id == meal.meal_id
        ).all()
        
        for (alg_name,) in meal_allergens:
            if alg_name.lower() in user_allergies:
                return (False, f'Allergy conflict: {alg_name}')
        return (True, None)
    
    def _check_ingredient_safety(self, user_context: dict, meal) -> Tuple[bool, Optional[str], List[str]]:
        warnings = []
        if not self.db:
            return (True, None, warnings)
        
        from models.meal import MealIngredient, Ingredient
        meal_ingredients = self.db.query(Ingredient).join(MealIngredient).filter(
            MealIngredient.meal_id == meal.meal_id
        ).all()
        
        for ingredient in meal_ingredients:
            if ingredient.food_id:
                safety_result = self.safety_engine.evaluate(user_context, ingredient.food_id)
                if not safety_result.is_safe_to_recommend:
                    return (False, f'Ingredient {ingredient.name}: {safety_result.veto_reason}', warnings)
                if safety_result.warnings:
                    warnings.extend(safety_result.warnings)
        
        return (True, None, warnings)
    
    def _check_disliked_foods(self, user_context: dict, meal) -> Tuple[bool, Optional[str]]:
        disliked = [d.lower() for d in user_context.get('disliked_foods', [])]
        if not disliked:
            return (True, None)
        
        meal_name_lower = meal.name.lower()
        for d in disliked:
            if d in meal_name_lower:
                return (False, f'User dislikes: {d}')
        return (True, None)
