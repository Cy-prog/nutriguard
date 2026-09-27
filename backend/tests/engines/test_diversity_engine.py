import pytest
from unittest.mock import MagicMock
from engines.diversity_engine import DiversityEngine

@pytest.fixture
def diversity_engine():
    return DiversityEngine()

def create_mock_meal(name="Dal", protein_src="LENTIL", grain="WHEAT", cuisine="NORTH"):
    m = MagicMock()
    m.name = name
    m.primary_protein_source = protein_src
    m.primary_grain = grain
    m.cuisine_region = cuisine
    m.cooking_method = "BOILING"
    return m

def test_no_repetition(diversity_engine):
    m1 = create_mock_meal("Dal")
    m2 = create_mock_meal("Dal")
    assert not diversity_engine.is_diverse_from(m2, [m1])

def test_different_meals_diverse(diversity_engine):
    m1 = create_mock_meal("Dal", "LENTIL", "WHEAT")
    m2 = create_mock_meal("Paneer", "PANEER", "RICE")
    assert diversity_engine.is_diverse_from(m2, [m1])

def test_same_protein_and_grain_not_diverse(diversity_engine):
    m1 = create_mock_meal("Dal Roti", "LENTIL", "WHEAT")
    m2 = create_mock_meal("Dal Paratha", "LENTIL", "WHEAT")
    assert not diversity_engine.is_diverse_from(m2, [m1])

def test_diversity_score_empty(diversity_engine):
    score = diversity_engine.calculate_diversity_score([])
    assert score.total == 0

def test_diversity_score_varied(diversity_engine):
    meals = [
        create_mock_meal("A", "P1", "G1", "C1"),
        create_mock_meal("B", "P2", "G2", "C2")
    ]
    score = diversity_engine.calculate_diversity_score(meals)
    assert score.total > 50

def test_filter_diverse_candidates(diversity_engine):
    m1 = create_mock_meal("Dal Roti", "LENTIL", "WHEAT")
    m2 = create_mock_meal("Dal Paratha", "LENTIL", "WHEAT")
    m3 = create_mock_meal("Chicken Rice", "CHICKEN", "RICE")
    
    candidates = [m2, m3]
    filtered = diversity_engine.filter_diverse_candidates(candidates, [m1])
    assert len(filtered) == 1
    assert filtered[0].name == "Chicken Rice"
