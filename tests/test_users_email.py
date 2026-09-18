import pytest
import time

class TestUsersEmail:
    """
    Tests for the following operations:
    - [GET] /users/{email} - Get specific user
    - [PUT] /users/{email} - Update an specific user
    """
    # --- GET /users/{email} ---
    def test_get_user_by_email(self, api_client, generate_email):
        email = generate_email()
        payload = {"name": "Alice Smith", "email": email, "age": 25}
        
        create_res = api_client.post("users", json_data=payload)
        assert create_res.status_code == 201

        response = api_client.get(f"users/{email}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        
        assert "name" in data
        assert "email" in data
        assert "age" in data

        assert isinstance(data["name"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["age"], int)

        assert data["email"] == email
        assert data["name"] == payload["name"]
        assert data["age"] == payload["age"]

    def test_get_user_by_email_not_found(self, api_client):
        non_existent_email = "nonexistent_user_9999@example.com"
        response = api_client.get(f"users/{non_existent_email}")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)

    # --- PUT /users/{email} ---
    def test_update_user(self, api_client, generate_email):
        email = generate_email()
        initial_payload = {"name": "Old Name", "email": email, "age": 20}
        
        create_res = api_client.post("users", json_data=initial_payload)
        assert create_res.status_code == 201

        update_payload = {"name": "New Name", "email": email, "age": 21}
        response = api_client.put(f"users/{email}", json_data=update_payload)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        
        assert data["name"] == "New Name"
        assert data["age"] == 21
        assert data["email"] == email

    def test_update_user_not_found(self, api_client):
        non_existent_email = "ghost_user_8888@example.com"
        update_payload = {"name": "Ghost", "email": non_existent_email, "age": 30}
        
        response = api_client.put(f"users/{non_existent_email}", json_data=update_payload)
        
        assert response.status_code == 404
        assert "error" in response.json()

    @pytest.mark.parametrize("missing_field", ["name", "email", "age"])
    def test_update_user_missing_required_fields(self, api_client, generate_email, missing_field):
        email = generate_email()
        api_client.post("users", json_data={"name": "Alice", "email": email, "age": 25})

        payload = {"name": "Alice Updated", "email": email, "age": 26}
        payload.pop(missing_field)

        response = api_client.put(f"users/{email}", json_data=payload)
        assert response.status_code == 400
        assert "error" in response.json()

    def test_update_user_duplicate_email(self, api_client, generate_email):
        email_user_a = generate_email()
        email_user_b = generate_email()

        api_client.post("users", json_data={"name": "User A", "email": email_user_a, "age": 25})
        api_client.post("users", json_data={"name": "User B", "email": email_user_b, "age": 33})

        update_payload = {"name": "User A Modified", "email": email_user_b, "age": 25}
        response = api_client.put(f"users/{email_user_a}", json_data=update_payload)

        assert response.status_code == 409
        assert "error" in response.json()
    

