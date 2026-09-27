import pytest
from unittest.mock import MagicMock
from engines.portion_engine import PortionEngine

@pytest.fixture
def portion_engine():
    return PortionEngine()

def create_mock_meal(calories=500, protein_g=20):
    m = MagicMock()
    m.calories = calories
    m.protein_g = protein_g
    m.carbohydrates_g = 50
    m.fat_g = 15
    m.fiber_g = 10
    m.serving_description = "1 bowl"
    return m

def test_exact_match_portion(portion_engine):
    meal = create_mock_meal(500, 20)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.portion_multiplier == 1.0

def test_double_portion(portion_engine):
    meal = create_mock_meal(250, 10)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.portion_multiplier == 2.0

def test_half_portion(portion_engine):
    meal = create_mock_meal(1000, 40)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.portion_multiplier == 0.5

def test_min_portion_clamped(portion_engine):
    meal = create_mock_meal(2000, 80)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.portion_multiplier == 0.5

def test_max_portion_clamped(portion_engine):
    meal = create_mock_meal(100, 4)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.portion_multiplier == 2.5

def test_zero_calorie_meal(portion_engine):
    meal = create_mock_meal(0, 0)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.portion_multiplier == 1.0

def test_portion_scales_protein(portion_engine):
    meal = create_mock_meal(250, 10)
    portioned = portion_engine.calculate_portion(meal, 500, 20)
    assert portioned.protein_g == 20.0
