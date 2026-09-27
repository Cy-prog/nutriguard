import pytest
from unittest.mock import MagicMock
from engines.substitution_engine import SubstitutionEngine

@pytest.fixture
def substitution_engine():
    db_session_mock = MagicMock()
    return SubstitutionEngine(db_session_mock)

def create_mock_meal(meal_id=1, meal_type="LUNCH", calories=500, protein_g=20):
    m = MagicMock()
    m.meal_id = meal_id
    m.meal_type = meal_type
    m.calories = calories
    m.protein_g = protein_g
    m.cuisine_region = "NORTH"
    m.is_vegetarian = True
    return m

def test_finds_same_type_alternatives(substitution_engine):
    meal = create_mock_meal(1, "LUNCH", 500, 20)
    candidates = [
        create_mock_meal(2, "LUNCH", 480, 18),
        create_mock_meal(3, "DINNER", 500, 20)
    ]
    alts = substitution_engine.find_alternatives(meal, {}, candidates)
    assert len(alts) == 1
    assert alts[0].meal_id == 2

def test_excludes_original_meal(substitution_engine):
    meal = create_mock_meal(1, "LUNCH", 500, 20)
    candidates = [
        create_mock_meal(1, "LUNCH", 500, 20),
        create_mock_meal(2, "LUNCH", 480, 18)
    ]
    alts = substitution_engine.find_alternatives(meal, {}, candidates)
    assert len(alts) == 1
    assert alts[0].meal_id == 2

def test_ranks_by_similarity(substitution_engine):
    meal = create_mock_meal(1, "LUNCH", 500, 20)
    candidates = [
        create_mock_meal(2, "LUNCH", 200, 5),
        create_mock_meal(3, "LUNCH", 490, 19)
    ]
    alts = substitution_engine.find_alternatives(meal, {}, candidates)
    assert len(alts) == 2
    assert alts[0].meal_id == 3
    assert alts[1].meal_id == 2

def test_empty_pool(substitution_engine):
    meal = create_mock_meal(1, "LUNCH")
    alts = substitution_engine.find_alternatives(meal, {}, [])
    assert len(alts) == 0

def test_count_limits_results(substitution_engine):
    meal = create_mock_meal(1, "LUNCH")
    candidates = [create_mock_meal(i, "LUNCH") for i in range(2, 10)]
    alts = substitution_engine.find_alternatives(meal, {}, candidates, count=3)
    assert len(alts) == 3
