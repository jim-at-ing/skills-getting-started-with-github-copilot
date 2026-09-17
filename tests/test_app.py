from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_activities_include_participants():
    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    chess = activities["Chess Club"]
    assert "participants" in chess
    assert chess["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]
