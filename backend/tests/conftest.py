import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from data.seed import (
    seed_foods, seed_medications, seed_conditions, seed_users,
    seed_drug_nutrient_depletions, seed_drug_food_interactions, seed_meals
)
import json

from sqlalchemy.pool import StaticPool

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="session")
def seeded_db(engine):
    Session = sessionmaker(bind=engine)
    db = Session()
    
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    with open(os.path.join(base_dir, 'seeds', 'foods_indian.json'), 'r') as f:
        foods_data = json.load(f)
    with open(os.path.join(base_dir, 'seeds', 'medications.json'), 'r') as f:
        meds_data = json.load(f)
    with open(os.path.join(base_dir, 'seeds', 'conditions.json'), 'r') as f:
        conds_data = json.load(f)
        
    seed_users(db)
    seed_foods(db, foods_data)
    seed_medications(db, meds_data)
    seed_conditions(db, conds_data)
    seed_drug_nutrient_depletions(db)
    seed_drug_food_interactions(db)

    meals_path = os.path.join(base_dir, 'seeds', 'meals_indian.json')
    if os.path.exists(meals_path):
        with open(meals_path, 'r', encoding='utf-8') as f:
            meals_data = json.load(f)
        seed_meals(db, meals_data)
    
    db.commit()
    
    yield db
    
    db.close()

@pytest.fixture
def db_session(seeded_db):
    yield seeded_db

from fastapi.testclient import TestClient
from main import app
from api.deps import get_db

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

