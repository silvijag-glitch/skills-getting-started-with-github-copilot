from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # make sure known activity exists
    assert "Chess Club" in data


def test_signup_and_duplicate():
    activity = "Soccer Team"
    email = "teststudent@example.com"

    # Ensure participant not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Cleanup
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)


def test_remove_participant():
    activity = "Programming Class"
    email = "removeme@example.com"

    # Add test participant
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Delete participant
    resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
