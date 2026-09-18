import pytest

class TestUsers:
    """
    Tests for the following operations:
    - [GET] /users - Get all users
    - [POST] /users - Create a new user
    """
    # --- GET /users/ ---
    def test_list_users(self, api_client):
        response = api_client.get("users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        for user in users:
            assert "name" in user
            assert "email" in user
            assert "age" in user
            assert isinstance(user["name"], str)
            assert isinstance(user["email"], str)
            assert isinstance(user["age"], int)
        
    # --- POST /users/ ---
    def test_create_user(self, api_client, generate_email):
        email = generate_email()
        payload = {"name": "Jane Doe", "email": email, "age":30}
        
        response = api_client.post("users", json_data=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == email
        assert isinstance(data, dict)
    
        assert "name" in data
        assert "email" in data
        assert "age" in data
        
        assert isinstance(data["name"], str)
        assert isinstance(data["email"], str)
        assert isinstance(data["age"], int)

    def test_create_user_invalid_email_format(self, api_client, generate_email):
        invalid_email = f"invalid_email_{generate_email().split('@')[0]}"
        payload = {
            "name": "Jane Doe",
            "email": invalid_email,
            "age": 30
        }
        response = api_client.post("users", json_data=payload)
        assert response.status_code == 400
        assert "error" in response.json()

    def test_create_duplicated_email(self, api_client, generate_email):
        email = generate_email()
        payload = {"name": "Jane Doe", "email": email, "age": 30}
        
        api_client.post("users", json_data=payload)
        duplicate_response = api_client.post("users", json_data=payload)
        
        assert duplicate_response.status_code == 409, f"POST /users FAILED. Status: {duplicate_response.status_code}, Body: {duplicate_response.text}"

    @pytest.mark.parametrize("invalid_age", [0, -1, 151])
    def test_create_user_invalid_age(self, api_client, generate_email, invalid_age):
        payload = {"name": "Invalid Age", "email": generate_email(), "age": invalid_age}
        response = api_client.post("users", json_data=payload)
        assert response.status_code == 400

    @pytest.mark.parametrize("missing_field", ["name", "email", "age"])
    def test_create_user_missing_required_fields(self, api_client, generate_email, missing_field):
        payload = {
            "name": "Jane Doe",
            "email": generate_email(),
            "age": 30
        }
        
        payload.pop(missing_field)

        response = api_client.post("users", json_data=payload)
        
        assert response.status_code == 400
        assert "error" in response.json()