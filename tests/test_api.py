"""
API endpoint tests for Mergington High School Activities

All tests follow the AAA (Arrange-Act-Assert) pattern for clarity and maintainability.
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_success(self, client):
        """Test retrieving all activities returns status 200"""
        # ARRANGE
        # (no setup needed, endpoint returns existing data)

        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client, activities_state):
        """Test successful signup adds participant to activity"""
        # ARRANGE
        activity_name = "Soccer Team"
        email = "new_student@mergington.edu"
        initial_count = len(activities_state[activity_name]["participants"])

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        assert email in activities_state[activity_name]["participants"]
        assert len(activities_state[activity_name]["participants"]) == initial_count + 1

    def test_signup_already_registered(self, client):
        """Test signup fails when student is already registered"""
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in Chess Club

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_activity_full(self, client, activities_state):
        """Test signup fails when activity has reached max participants"""
        # ARRANGE
        activity_name = "Track and Field"
        # Fill the activity to capacity
        activity = activities_state[activity_name]
        while len(activity["participants"]) < activity["max_participants"]:
            activity["participants"].append(f"student{len(activity['participants'])}@mergington.edu")
        
        new_email = "another_student@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "full" in response.json()["detail"]

    def test_signup_activity_not_found(self, client):
        """Test signup fails when activity does not exist"""
        # ARRANGE
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Tests for POST /activities/{activity_name}/unregister endpoint"""

    def test_unregister_success(self, client, activities_state):
        """Test successful unregister removes participant from activity"""
        # ARRANGE
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        initial_count = len(activities_state[activity_name]["participants"])

        # ACT
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in activities_state[activity_name]["participants"]
        assert len(activities_state[activity_name]["participants"]) == initial_count - 1

    def test_unregister_student_not_registered(self, client):
        """Test unregister fails when student is not registered"""
        # ARRANGE
        activity_name = "Art Club"
        email = "not_registered@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_activity_not_found(self, client):
        """Test unregister fails when activity does not exist"""
        # ARRANGE
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestRootRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """Test root path redirects to static index.html"""
        # ARRANGE
        # (no setup needed)

        # ACT
        response = client.get("/", follow_redirects=False)

        # ASSERT
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
