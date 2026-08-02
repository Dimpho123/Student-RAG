from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_empty_question():
    response = client.post(
        "/ask",
        json={"question": ""}
    )

    assert response.status_code == 200
    assert "error" in response.json()


def test_unknown_question():
    response = client.post(
        "/ask",
        json={"question": "Who won FIFA 2022?"}
    )

    assert response.status_code == 200


def test_valid_question():
    response = client.post(
        "/ask",
        json={"question": "What are the hardware requirements?"}
    )

    assert response.status_code == 200