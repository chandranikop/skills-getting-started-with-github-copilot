import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", json={"email": email})

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]

    # Check participant is added
    resp_activities = client.get("/activities")
    assert email in resp_activities.json()[activity]["participants"]

    # Unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert resp_unreg.status_code == 200
    assert f"Unregistered {email}" in resp_unreg.json()["message"]

    # Check participant is removed
    resp_activities2 = client.get("/activities")
    assert email not in resp_activities2.json()[activity]["participants"]
