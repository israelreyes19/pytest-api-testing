import pytest
import time
from config.settings import get_base_url, AUTH_TOKEN
from client.api_client import APIClient

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Execution enviroment: dev or prod"
    )

@pytest.fixture
def generate_email():
    counter = 0
    def _create():
        nonlocal counter
        counter += 1
        timestamp = int(time.time() * 1000)
        return f"user_{timestamp}_{counter}@example.com"
    return _create

@pytest.fixture(scope="session")
def base_url(request):
    env = request.config.getoption("--env").lower()
    return get_base_url(env)

@pytest.fixture(scope="session")
def api_client(base_url) -> APIClient:
    """Shared instance of HTTP APIClient for testing session"""
    return APIClient(base_url=base_url)

@pytest.fixture(scope="session")
def authenticated_client(base_url) -> APIClient: 
    """Shared instance of Authenticaded HTTP APIClient for testing session"""
    return APIClient(base_url=base_url, token=AUTH_TOKEN)
