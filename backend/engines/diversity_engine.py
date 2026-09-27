from typing import List, Dict, Set, Optional
from dataclasses import dataclass

@dataclass
class DiversityScore:
    cuisine_diversity: float
    protein_source_diversity: float
    grain_diversity: float
    vegetable_diversity: float
    cooking_method_diversity: float
    total: float

class DiversityEngine:
    def calculate_diversity_score(self, meals: list) -> DiversityScore:
        if not meals:
            return DiversityScore(0, 0, 0, 0, 0, 0)
        
        cuisine_set = set()
        protein_set = set()
        grain_set = set()
        cooking_set = set()
        
        for meal in meals:
            if meal.cuisine_region:
                cuisine_set.add(meal.cuisine_region)
            if meal.primary_protein_source:
                protein_set.add(meal.primary_protein_source)
            if meal.primary_grain:
                grain_set.add(meal.primary_grain)
            if meal.cooking_method:
                cooking_set.add(meal.cooking_method)
        
        n = len(meals)
        cuisine_div = min(100, (len(cuisine_set) / max(n, 1)) * 100)
        protein_div = min(100, (len(protein_set) / max(n, 1)) * 100)
        grain_div = min(100, (len(grain_set) / max(n, 1)) * 100)
        cooking_div = min(100, (len(cooking_set) / max(n, 1)) * 100)
        
        total = (
            cuisine_div * 0.20 +
            protein_div * 0.30 +
            grain_div * 0.20 +
            cooking_div * 0.15 +
            50.0 * 0.15  # vegetable diversity placeholder
        )
        
        return DiversityScore(
            cuisine_diversity=round(cuisine_div, 1),
            protein_source_diversity=round(protein_div, 1),
            grain_diversity=round(grain_div, 1),
            vegetable_diversity=50.0,
            cooking_method_diversity=round(cooking_div, 1),
            total=round(total, 1)
        )
    
    def is_diverse_from(self, candidate, already_selected: list) -> bool:
        if not already_selected:
            return True
        for selected in already_selected:
            if candidate.name == selected.name:
                return False
            if (candidate.primary_protein_source and selected.primary_protein_source and 
                candidate.primary_protein_source == selected.primary_protein_source and
                candidate.primary_grain and selected.primary_grain and
                candidate.primary_grain == selected.primary_grain):
                return False
        return True
    
    def filter_diverse_candidates(self, candidates: list, already_selected: list) -> list:
        return [c for c in candidates if self.is_diverse_from(c, already_selected)]
