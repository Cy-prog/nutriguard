from typing import Dict, Any

def score_meal(meal, target_calories: float, target_protein: float, user_context: dict) -> float:
    score = 100.0
    
    meal_cal = float(meal.calories or 0)
    meal_prot = float(meal.protein_g or 0)
    
    if meal_cal > 0 and target_calories > 0:
        cal_diff = abs(meal_cal - target_calories) / target_calories
        score -= min(30, cal_diff * 100)
        
    if meal_prot > 0 and target_protein > 0:
        prot_diff = abs(meal_prot - target_protein) / target_protein
        score -= min(20, prot_diff * 100)
        
    if meal.name.lower() in [f.lower() for f in user_context.get('favorite_foods', [])]:
        score += 15
        
    return max(0.0, min(100.0, score))
