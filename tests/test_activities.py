from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert isinstance(payload[expected_activity], dict)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "teststudent@mergington.edu"
    initial_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
    assert new_email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) + 1


def test_signup_duplicate_student_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": duplicate_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_removes_student(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = activities[activity_name]["participants"][0]
    initial_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": participant_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {participant_email} from {activity_name}"}
    assert participant_email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) - 1


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "missingstudent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": missing_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_participant_from_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
