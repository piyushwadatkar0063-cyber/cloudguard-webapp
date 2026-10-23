
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["project"] == "CloudGuard"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "connected"


def test_create_deployment():
    response = client.post(
        "/deployments",
        json={
            "application_name": "test-payment-service",
            "environment": "testing",
            "status": "success",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["application_name"] == "test-payment-service"
    assert data["environment"] == "testing"
    assert data["status"] == "success"
    assert "id" in data


def test_list_deployments():
    response = client.get("/deployments")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_deployments_by_status():
    response = client.get("/deployments?status=success")

    assert response.status_code == 200
    assert all(
        deployment["status"] == "success"
        for deployment in response.json()
    )


def test_deployment_pagination():
    response = client.get("/deployments?limit=1&offset=0")

    assert response.status_code == 200
    assert len(response.json()) <= 1


def test_deployment_not_found():
    response = client.get("/deployments/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Deployment not found"


def test_invalid_deployment_status():
    response = client.post(
        "/deployments",
        json={
            "application_name": "invalid-status-service",
            "environment": "testing",
            "status": "unknown",
        },
    )

    assert response.status_code == 422
