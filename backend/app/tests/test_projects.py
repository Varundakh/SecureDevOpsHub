from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_project_creation_and_listing() -> None:
    registration = client.post(
        "/api/auth/register",
        json={"email": "project@example.com", "password": "P@ssword123", "role": "Developer"},
    )
    token = registration.json()["access_token"]

    create_response = client.post(
        "/api/projects",
        json={"name": "demo-project", "description": "Example project", "repository_url": "https://github.com/example/demo"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    project_id = create_response.json()["id"]

    list_response = client.get("/api/projects")
    assert list_response.status_code == 200
    assert any(item["id"] == project_id for item in list_response.json())

    scan_response = client.post(
        f"/api/projects/{project_id}/scan",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert scan_response.status_code == 200
