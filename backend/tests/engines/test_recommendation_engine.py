import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import date
from engines.recommendation_engine import RecommendationEngine

def create_mock_meal(meal_id=1, name="Dal", meal_type="LUNCH", cals=500, prot=20, veg=True):
    m = MagicMock()
    m.meal_id = meal_id
    m.name = name
    m.meal_type = meal_type
    m.calories = cals
    m.protein_g = prot
    m.is_vegetarian = veg
    m.is_active = True
    m.cuisine_region = "NORTH_INDIAN"
    m.primary_protein_source = "LENTIL"
    m.primary_grain = "WHEAT"
    m.cooking_method = "BOILING"
    m.is_vegan = veg
    m.is_jain_friendly = False
    return m

@pytest.fixture
def db_session_mock():
    return MagicMock()

@pytest.fixture
def recommendation_engine(db_session_mock):
    return RecommendationEngine(db_session_mock)

def test_generate_plan_returns_plan(recommendation_engine, db_session_mock):
    user_id = uuid4()
    profile_mock = MagicMock()
    profile_mock.user_id = user_id
    profile_mock.weight_kg = 70
    profile_mock.height_cm = 175
    profile_mock.age = 30
    profile_mock.sex = 'male'
    profile_mock.activity_level = 'SEDENTARY'
    profile_mock.fitness_goal = 'GENERAL_HEALTH'
    profile_mock.diet_type = 'VEGETARIAN'
    profile_mock.disliked_foods = []
    profile_mock.favorite_foods = []
    
    meals = [
        create_mock_meal(1, "Oats", "BREAKFAST", 300, 10, True),
        create_mock_meal(2, "Dal Rice", "LUNCH", 600, 20, True),
        create_mock_meal(3, "Roti Sabzi", "DINNER", 500, 15, True),
        create_mock_meal(4, "Fruit", "SNACK", 150, 2, True),
    ]
    db_session_mock.query().filter().first.side_effect = [profile_mock]
    db_session_mock.query().filter().all.side_effect = [[], [], [], meals]
    
    with patch('engines.meal_safety_engine.MealSafetyEngine.filter_safe_meals', return_value=meals):
        plan = recommendation_engine.generate_daily_plan(user_id, date.today())
        
    assert plan is not None
    assert plan.user_id == user_id
    assert db_session_mock.add.called

def test_generate_plan_no_profile(recommendation_engine, db_session_mock):
    db_session_mock.query().filter().first.return_value = None
    plan = recommendation_engine.generate_daily_plan(uuid4(), date.today())
    assert plan is None

def test_generate_plan_no_meals(recommendation_engine, db_session_mock):
    user_id = uuid4()
    profile_mock = MagicMock()
    db_session_mock.query().filter().first.return_value = profile_mock
    db_session_mock.query().filter().all.return_value = []
    
    plan = recommendation_engine.generate_daily_plan(user_id, date.today())
    assert plan is None

def test_vegetarian_filter(recommendation_engine, db_session_mock):
    pass

def test_meal_types_correct(recommendation_engine, db_session_mock):
    pass

def test_three_different_meals(recommendation_engine, db_session_mock):
    pass

def test_weekly_plan_generates_7_days(recommendation_engine, db_session_mock):
    with patch.object(recommendation_engine, 'generate_daily_plan', return_value=MagicMock()):
        plans = recommendation_engine.generate_weekly_plan(uuid4(), date.today())
        assert len(plans) == 7
