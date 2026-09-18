import pytest

class TestUsersDelete:
    """
    Tests for the following operations:
    - [DELETE] /users/{email} - Delete specific user
    """
    def test_delete_user_unauthorized(self, api_client, generate_email):
        email = generate_email()
        
        response = api_client.delete(f"users/{email}", token=None)
        
        assert response.status_code == 401
        data = response.json()
        assert "error" in data

    def test_delete_user_invalid_token(self, api_client, generate_email):
        email = generate_email()
        
        response = api_client.delete(f"users/{email}", token="invalid_token_xyz")
        
        assert response.status_code == 401
        data = response.json()
        assert "error" in data

    def test_delete_user(self, authenticated_client, generate_email):
        email = generate_email()
        payload = {"name": "To Delete", "email": email, "age": 40}
        
        create_res = authenticated_client.post("users", json_data=payload)
        assert create_res.status_code == 201

        response = authenticated_client.delete(f"users/{email}")
        
        assert response.status_code == 204

        get_response = authenticated_client.get(f"users/{email}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, authenticated_client):
        non_existent_email = "nonexistent_delete_7777@example.com"
        
        response = authenticated_client.delete(f"users/{non_existent_email}")
        
        assert response.status_code == 404
        assert "error" in response.json()