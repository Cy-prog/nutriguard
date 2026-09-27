import pytest

def test_list_foods_endpoint(client):
    response = client.get("/api/v1/foods?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "foods" in data
    assert "total" in data
    assert isinstance(data["foods"], list)

def test_get_food_substitutions(client):
    response = client.get("/api/v1/foods/substitutions?food=paneer")
    assert response.status_code == 200
    data = response.json()
    assert data["target_food"].lower() == "paneer"
    assert len(data["substitutions"]) > 0
    assert any("tofu" in s["name"].lower() for s in data["substitutions"])

def test_get_rice_substitutions(client):
    response = client.get("/api/v1/foods/substitutions?food=white%20rice")
    assert response.status_code == 200
    data = response.json()
    assert len(data["substitutions"]) > 0
    assert any("millet" in s["name"].lower() or "brown rice" in s["name"].lower() for s in data["substitutions"])

def test_recipes_alias_requires_auth(client):
    response = client.get("/api/v1/recipes")
    assert response.status_code == 401

def test_recipes_alias_with_token(client):
    login_res = client.post("/api/v1/auth/login", data={"username": "user@nutriguard.com", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    res = client.get("/api/v1/recipes/?page=1&page_size=5", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "meals" in data
