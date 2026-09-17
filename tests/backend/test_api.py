from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


def test_get_activities_returns_activity_catalog():
    # Arrange
    # no setup beyond the fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_for_duplicate_student_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Missing Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity_name)}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
