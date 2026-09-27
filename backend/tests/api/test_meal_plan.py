import pytest
from fastapi.testclient import TestClient

def test_generate_plan_requires_auth(client):
    response = client.post("/api/v1/me/meal-plan/generate", json={"date": "2023-01-01"})
    assert response.status_code == 401

def test_get_today_plan_requires_auth(client):
    response = client.get("/api/v1/me/meal-plan/today")
    assert response.status_code == 401
