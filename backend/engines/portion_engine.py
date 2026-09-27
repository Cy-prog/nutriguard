from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class PortionedMeal:
    meal: object
    portion_multiplier: float
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    serving_description: str

class PortionEngine:
    MIN_PORTION = 0.5
    MAX_PORTION = 2.5
    
    def calculate_portion(self, meal, target_calories: float, target_protein: float) -> PortionedMeal:
        base_calories = float(meal.calories or 0)
        base_protein = float(meal.protein_g or 0)
        
        if base_calories <= 0:
            return self._default_portion(meal)
        
        cal_multiplier = target_calories / base_calories
        
        if base_protein > 0 and target_protein > 0:
            prot_multiplier = target_protein / base_protein
            multiplier = (cal_multiplier * 0.6 + prot_multiplier * 0.4)
        else:
            multiplier = cal_multiplier
        
        multiplier = max(self.MIN_PORTION, min(self.MAX_PORTION, multiplier))
        multiplier = round(multiplier, 2)
        
        return PortionedMeal(
            meal=meal,
            portion_multiplier=multiplier,
            calories=round(base_calories * multiplier, 1),
            protein_g=round(float(meal.protein_g or 0) * multiplier, 1),
            carbs_g=round(float(meal.carbohydrates_g or 0) * multiplier, 1),
            fat_g=round(float(meal.fat_g or 0) * multiplier, 1),
            fiber_g=round(float(meal.fiber_g or 0) * multiplier, 1),
            serving_description=self._format_serving(meal, multiplier)
        )
    
    def _default_portion(self, meal) -> PortionedMeal:
        return PortionedMeal(
            meal=meal, portion_multiplier=1.0,
            calories=float(meal.calories or 0),
            protein_g=float(meal.protein_g or 0),
            carbs_g=float(meal.carbohydrates_g or 0),
            fat_g=float(meal.fat_g or 0),
            fiber_g=float(meal.fiber_g or 0),
            serving_description=meal.serving_description or '1 serving'
        )
    
    def _format_serving(self, meal, multiplier: float) -> str:
        base_desc = meal.serving_description or '1 serving'
        if abs(multiplier - 1.0) < 0.05:
            return base_desc
        return f'{multiplier:.1f}x ({base_desc})'
