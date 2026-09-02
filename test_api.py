from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


REFUSAL_MESSAGE = (
    "I could not find that information in the available knowledge base."
)


def test_handbook_question():
    response = client.post(
        "/ask",
        json={
            "question": "What are the live class times?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data

    assert "Student Handbook" in data["source"]

    print("\nHANDBOOK TEST")
    print("Question:", "What are the live class times?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_handbook_join_classes():
    response = client.post(
        "/ask",
        json={
            "question": "How do I join classes?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data

    assert "Student Handbook" in data["source"]

    print("\nHANDBOOK TEST")
    print("Question:", "How do I join classes?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_handbook_schedule():
    response = client.post(
        "/ask",
        json={
            "question": "What happens after the first 12 weeks?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data

    assert "Student Handbook" in data["source"]

    print("\nHANDBOOK TEST")
    print("Question:", "What happens after the first 12 weeks?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_website_courses():
    response = client.post(
        "/ask",
        json={
            "question": "What courses does ZAIO offer?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data

    assert "ZAIO Website" in data["source"]
    assert "compare-courses" in data["source"]

    print("\nWEBSITE TEST")
    print("Question:", "What courses does ZAIO offer?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_website_bootcamp():
    response = client.post(
        "/ask",
        json={
            "question": "What bootcamps does ZAIO offer?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data

    assert "ZAIO Website" in data["source"]

    print("\nWEBSITE TEST")
    print("Question:", "What bootcamps does ZAIO offer?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_website_online_learning():
    response = client.post(
        "/ask",
        json={
            "question": "Are ZAIO courses fully online?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "source" in data

    assert "ZAIO Website" in data["source"]

    print("\nWEBSITE TEST")
    print("Question:", "Are ZAIO courses fully online?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_unanswerable_population():
    response = client.post(
        "/ask",
        json={
            "question": "What is the population of South Africa?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == REFUSAL_MESSAGE
    assert data["source"] is None

    print("\nUNANSWERABLE TEST")
    print("Question:", "What is the population of South Africa?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_unanswerable_weather():
    response = client.post(
        "/ask",
        json={
            "question": "What will the weather be tomorrow?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == REFUSAL_MESSAGE
    assert data["source"] is None

    print("\nUNANSWERABLE TEST")
    print("Question:", "What will the weather be tomorrow?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])


def test_unanswerable_sports():
    response = client.post(
        "/ask",
        json={
            "question": "Who won the latest football match?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == REFUSAL_MESSAGE
    assert data["source"] is None

    print("\nUNANSWERABLE TEST")
    print("Question:", "Who won the latest football match?")
    print("Source:", data["source"])
    print("Answer:", data["answer"])