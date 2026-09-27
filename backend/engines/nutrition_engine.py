from dataclasses import dataclass
from typing import Dict, Optional

ACTIVITY_MULTIPLIERS = {
    'SEDENTARY': 1.2,
    'LIGHTLY_ACTIVE': 1.375,
    'MODERATELY_ACTIVE': 1.55,
    'VERY_ACTIVE': 1.725,
    'EXTRA_ACTIVE': 1.9
}

@dataclass
class NutritionTargets:
    bmi: float
    bmr: float
    tdee: float
    target_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    water_ml: float
    calcium_mg: float
    iron_mg: float
    vitamin_c_mg: float
    vitamin_d_mcg: float
    vitamin_b12_mcg: float
    folate_mcg: float
    meal_distribution: Dict[str, float]
    disclaimer: str = "These are estimates based on standard nutritional formulas (Mifflin-St Jeor). Not medical prescriptions. Consult a dietitian for personalized clinical advice."

class NutritionEngine:
    """Deterministic nutrition requirement calculator using established formulas."""
    
    def calculate_targets(self, profile) -> NutritionTargets:
        # Extract profile data with safe defaults
        weight_kg = float(profile.weight_kg or 70)
        height_cm = float(profile.height_cm or 170)
        age = int(profile.age or 30)
        sex = (profile.sex or 'male').lower()
        activity_level = (profile.activity_level or 'MODERATELY_ACTIVE').upper()
        fitness_goal = (profile.fitness_goal or 'GENERAL_HEALTH').upper()
        
        bmi = self.calculate_bmi(weight_kg, height_cm)
        bmr = self.calculate_bmr(weight_kg, height_cm, age, sex)
        tdee = self.calculate_tdee(bmr, activity_level)
        target_calories = self.adjust_calories_for_goal(tdee, fitness_goal)
        protein_g = self.calculate_protein_target(weight_kg, fitness_goal)
        fat_g = self.calculate_fat_target(target_calories)
        carbs_g = self.calculate_carbs_target(target_calories, protein_g, fat_g)
        fiber_g = self.calculate_fiber_target(sex, age)
        water_ml = self.calculate_water_target(weight_kg)
        micros = self.calculate_micronutrient_targets(sex, age)
        meal_dist = self.get_meal_distribution()
        
        return NutritionTargets(
            bmi=round(bmi, 1),
            bmr=round(bmr, 0),
            tdee=round(tdee, 0),
            target_calories=round(target_calories, 0),
            protein_g=round(protein_g, 0),
            carbs_g=round(carbs_g, 0),
            fat_g=round(fat_g, 0),
            fiber_g=round(fiber_g, 0),
            water_ml=round(water_ml, 0),
            meal_distribution=meal_dist,
            **micros
        )
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> float:
        height_m = height_cm / 100
        if height_m <= 0:
            return 0.0
        return weight_kg / (height_m ** 2)
    
    @staticmethod
    def calculate_bmr(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
        """Mifflin-St Jeor Equation (most accurate for general population)."""
        base = 10 * weight_kg + 6.25 * height_cm - 5 * age
        if sex in ('male', 'm'):
            return base + 5
        else:
            return base - 161
    
    @staticmethod
    def calculate_tdee(bmr: float, activity_level: str) -> float:
        multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.55)
        return bmr * multiplier
    
    @staticmethod
    def adjust_calories_for_goal(tdee: float, fitness_goal: str) -> float:
        if fitness_goal == 'WEIGHT_LOSS':
            deficit = min(500, tdee * 0.20)  # Max 20% deficit
            return max(1200, tdee - deficit)  # Never below 1200
        elif fitness_goal == 'WEIGHT_GAIN':
            return tdee + 400
        elif fitness_goal == 'MUSCLE_GAIN':
            return tdee + 300
        else:  # WEIGHT_MAINTENANCE, GENERAL_HEALTH
            return tdee
    
    @staticmethod
    def calculate_protein_target(weight_kg: float, fitness_goal: str) -> float:
        multipliers = {
            'WEIGHT_LOSS': 1.2,
            'WEIGHT_MAINTENANCE': 1.0,
            'WEIGHT_GAIN': 1.4,
            'MUSCLE_GAIN': 1.8,
            'GENERAL_HEALTH': 1.0
        }
        mult = multipliers.get(fitness_goal, 1.0)
        return weight_kg * mult
    
    @staticmethod
    def calculate_fat_target(target_calories: float) -> float:
        return (target_calories * 0.25) / 9  # 25% of calories from fat
    
    @staticmethod
    def calculate_carbs_target(target_calories: float, protein_g: float, fat_g: float) -> float:
        remaining_calories = target_calories - (protein_g * 4) - (fat_g * 9)
        return max(100, remaining_calories / 4)  # At least 100g carbs
    
    @staticmethod
    def calculate_fiber_target(sex: str, age: int) -> float:
        if sex in ('male', 'm'):
            return 38.0 if age <= 50 else 30.0
        else:
            return 25.0 if age <= 50 else 21.0
    
    @staticmethod
    def calculate_water_target(weight_kg: float) -> float:
        return weight_kg * 35  # 35 ml per kg body weight
    
    @staticmethod
    def calculate_micronutrient_targets(sex: str, age: int) -> dict:
        """ICMR RDA-based micronutrient targets."""
        if sex in ('male', 'm'):
            return {
                'calcium_mg': 1000.0,
                'iron_mg': 17.0,
                'vitamin_c_mg': 80.0,
                'vitamin_d_mcg': 10.0,
                'vitamin_b12_mcg': 2.2,
                'folate_mcg': 300.0
            }
        else:
            return {
                'calcium_mg': 1000.0,
                'iron_mg': 21.0,
                'vitamin_c_mg': 65.0,
                'vitamin_d_mcg': 10.0,
                'vitamin_b12_mcg': 2.2,
                'folate_mcg': 400.0
            }
    
    @staticmethod
    def get_meal_distribution() -> Dict[str, float]:
        return {
            'BREAKFAST': 0.25,
            'LUNCH': 0.35,
            'DINNER': 0.30,
            'SNACK': 0.10
        }
    
    def get_meal_calorie_target(self, targets: NutritionTargets, meal_type: str) -> float:
        distribution = targets.meal_distribution.get(meal_type.upper(), 0.30)
        return targets.target_calories * distribution
    
    def get_meal_protein_target(self, targets: NutritionTargets, meal_type: str) -> float:
        distribution = targets.meal_distribution.get(meal_type.upper(), 0.30)
        return targets.protein_g * distribution
