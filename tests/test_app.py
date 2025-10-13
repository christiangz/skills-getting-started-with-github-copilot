import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # First signup should succeed
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Second signup should fail (already signed up)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_participant():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Unregister should succeed
    response = client.post("/activities/unregister", json={"activity_name": activity, "email": email})
    assert response.status_code == 200
    # Unregister again should fail (not found)
    response = client.post("/activities/unregister", json={"activity_name": activity, "email": email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_activity_not_found():
    response = client.post("/activities/unregister", json={"activity_name": "Fake Activity", "email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
