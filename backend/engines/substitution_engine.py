from typing import List, Optional
from uuid import UUID
import math

class SubstitutionEngine:
    def __init__(self, db_session):
        self.db = db_session
    
    def find_alternatives(self, meal, user_context: dict, all_safe_meals: list, count: int = 5) -> list:
        same_type = [m for m in all_safe_meals 
                     if m.meal_type == meal.meal_type and m.meal_id != meal.meal_id]
        
        scored = []
        for candidate in same_type:
            similarity = self._nutrition_similarity(meal, candidate)
            scored.append((candidate, similarity))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored[:count]]
    
    def _nutrition_similarity(self, original, candidate) -> float:
        """Score 0-100 based on how nutritionally similar two meals are."""
        score = 100.0
        
        orig_cal = float(original.calories or 0)
        cand_cal = float(candidate.calories or 0)
        if orig_cal > 0:
            cal_diff_pct = abs(orig_cal - cand_cal) / orig_cal
            score -= min(40, cal_diff_pct * 100)
        
        orig_prot = float(original.protein_g or 0)
        cand_prot = float(candidate.protein_g or 0)
        if orig_prot > 0:
            prot_diff_pct = abs(orig_prot - cand_prot) / orig_prot
            score -= min(30, prot_diff_pct * 75)
        
        if original.cuisine_region and candidate.cuisine_region:
            if original.cuisine_region == candidate.cuisine_region:
                score += 5
        
        if original.is_vegetarian == candidate.is_vegetarian:
            score += 5
        
        return max(0, min(100, score))
