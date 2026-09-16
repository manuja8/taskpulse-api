from fastapi.testclient import TestClient

from app.main import app
from app.service import classify_task_priority, completion_percentage

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_completion_percentage():
    assert completion_percentage(3, 4) == 75.0


def test_zero_total_is_safe():
    assert completion_percentage(0, 0) == 0.0


def test_normal_priority():
    assert classify_task_priority(1) == "NORMAL"


def test_high_priority():
    assert classify_task_priority(3) == "HIGH"


def test_task_status_endpoint():
    response = client.post(
        "/task/status",
        json={
            "task_name": "Release API",
            "completed_steps": 4,
            "total_steps": 5,
            "open_dependencies": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completion_percentage"] == 80.0
    assert data["priority"] == "NORMAL"
