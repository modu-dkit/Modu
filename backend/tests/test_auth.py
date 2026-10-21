from fastapi.testclient import TestClient

from app.main import app


def test_logged_out_user_cannot_reach_private_page() -> None:
    with TestClient(app) as client:
        response = client.get("/private")

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"
