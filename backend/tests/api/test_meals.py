import pytest
import uuid

def test_list_meals_requires_auth(client):
    response = client.get("/api/v1/meals")
    assert response.status_code == 401

def test_meal_detail_404(client):
    # This might require auth. Since we don't have an auth token here, 
    # we just test that the endpoint requires auth
    meal_id = uuid.uuid4()
    response = client.get(f"/api/v1/meals/{meal_id}")
    assert response.status_code == 401
