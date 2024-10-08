from starlette.testclient import TestClient

from tests.types import SideEffect


def test_if_can_get_health_report_when_healthy(
    test_client: TestClient, healthy_probe: SideEffect
) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "uptime": "1:00:00",
        "cpu": 8,
        "ram": 32,
    }


def test_if_can_get_health_report_when_unhealthy(
    test_client: TestClient, faulty_probe: SideEffect
) -> None:
    response = test_client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "unhealthy",
        "error_type": "OSError",
        "error": "Foo",
    }
