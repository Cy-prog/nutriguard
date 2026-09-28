import pytest
from core.security import verify_password, get_password_hash

def test_password_hashing():
    pwd = "supersecret"
    hashed = get_password_hash(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong", hashed)

def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user@nutriguard.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user@nutriguard.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400

def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@nutriguard.com", "password": "securepassword123", "name": "New User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client):
    # user@nutriguard.com already exists in test seeds
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user@nutriguard.com", "password": "securepassword123"}
    )
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()

def test_register_short_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "shortpwd@nutriguard.com", "password": "short"}
    )
    assert response.status_code == 422
