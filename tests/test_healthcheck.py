
def test_healthcheck_endpoint(api_client):
    response = api_client.get("users")
    assert response.status_code == 200

def test_healthcheck_auth(authenticated_client):
    response = authenticated_client.get("users")
    assert response.status_code == 200
