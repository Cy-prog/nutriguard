import pytest
from unittest.mock import MagicMock
from engines.nutrition_engine import NutritionEngine

@pytest.fixture
def nutrition_engine():
    return NutritionEngine()

def test_bmi_calculation(nutrition_engine):
    bmi = nutrition_engine.calculate_bmi(70, 170)
    assert round(bmi, 1) == 24.2

def test_bmi_edge_case_zero_height(nutrition_engine):
    bmi = nutrition_engine.calculate_bmi(70, 0)
    assert bmi == 0.0

def test_bmr_male(nutrition_engine):
    bmr = nutrition_engine.calculate_bmr(70, 175, 30, 'male')
    assert bmr == 1648.75

def test_bmr_female(nutrition_engine):
    bmr = nutrition_engine.calculate_bmr(60, 160, 25, 'female')
    assert bmr == 1314.0

def test_tdee_sedentary(nutrition_engine):
    bmr = nutrition_engine.calculate_bmr(70, 175, 30, 'male')
    tdee = nutrition_engine.calculate_tdee(bmr, 'SEDENTARY')
    assert round(tdee, 1) == round(bmr * 1.2, 1)

def test_tdee_very_active(nutrition_engine):
    bmr = nutrition_engine.calculate_bmr(70, 175, 30, 'male')
    tdee = nutrition_engine.calculate_tdee(bmr, 'VERY_ACTIVE')
    assert round(tdee, 1) == round(bmr * 1.725, 1)

def test_calories_weight_loss(nutrition_engine):
    cals = nutrition_engine.adjust_calories_for_goal(2000, 'WEIGHT_LOSS')
    assert cals == 1600.0

def test_calories_weight_gain(nutrition_engine):
    cals = nutrition_engine.adjust_calories_for_goal(2000, 'WEIGHT_GAIN')
    assert cals == 2400.0

def test_calories_muscle_gain(nutrition_engine):
    cals = nutrition_engine.adjust_calories_for_goal(2000, 'MUSCLE_GAIN')
    assert cals == 2300.0

def test_protein_weight_loss(nutrition_engine):
    protein = nutrition_engine.calculate_protein_target(70, 'WEIGHT_LOSS')
    assert round(protein, 1) == 84.0

def test_protein_muscle_gain(nutrition_engine):
    protein = nutrition_engine.calculate_protein_target(70, 'MUSCLE_GAIN')
    assert round(protein, 1) == 126.0

def test_fiber_male_young(nutrition_engine):
    fiber = nutrition_engine.calculate_fiber_target('male', 30)
    assert fiber == 38.0

def test_fiber_female_young(nutrition_engine):
    fiber = nutrition_engine.calculate_fiber_target('female', 25)
    assert fiber == 25.0

def test_calculate_targets_full(nutrition_engine):
    profile = MagicMock()
    profile.weight_kg = 70
    profile.height_cm = 175
    profile.age = 30
    profile.sex = 'male'
    profile.activity_level = 'MODERATELY_ACTIVE'
    profile.fitness_goal = 'GENERAL_HEALTH'
    
    targets = nutrition_engine.calculate_targets(profile)
    assert targets.bmi > 0
    assert targets.target_calories > 0
    assert targets.protein_g > 0
    assert targets.fat_g > 0
    assert targets.carbs_g > 0
    assert targets.fiber_g > 0

def test_meal_distribution_sums_to_one(nutrition_engine):
    dist = nutrition_engine.get_meal_distribution()
    assert round(sum(dist.values()), 5) == 1.0

def test_minimum_calories_never_below_1200(nutrition_engine):
    cals = nutrition_engine.adjust_calories_for_goal(1300, 'WEIGHT_LOSS')
    assert cals >= 1200
