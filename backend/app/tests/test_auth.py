from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_and_login() -> None:
    register_response = client.post(
        "/api/auth/register",
        json={"email": "demo@example.com", "password": "P@ssword123", "role": "Developer"},
    )
    assert register_response.status_code == 200
    assert "access_token" in register_response.json()

    login_response = client.post(
        "/api/auth/login",
        json={"email": "demo@example.com", "password": "P@ssword123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_invalid_login() -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "missing@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
