import logging
import requests
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class APIClient: 
    """
    HTTP client to interact with User Management API
    """

    def __init__(self, base_url:str, token: str = None, timeout: int = 5):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()
        self.timeout = timeout
        self.token = token

        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _build_url(self, endpoint:str) -> str:
        return urljoin(self.base_url, endpoint.rstrip("/"))

    def delete(self, endpoint: str, token:str = None, headers: dict = None):
            url = self._build_url(endpoint)
            request_headers = headers or {}

            request_token = token if token is not None else self.token
            if request_token:
                 request_headers["Authentication"] = request_token

            response = self.session.delete(url, headers=request_headers, timeout=self.timeout)
            logger.info(f"HTTP DELETE {url} -> Status: {response.status_code}")
            return response

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        url = self._build_url(endpoint)
        response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        logger.info(f"HTTP GET {url} -> Status: {response.status_code}")
        return response

    def post(self, endpoint: str, json_data: dict = None, headers: dict = None):
        url = self._build_url(endpoint)
        response = self.session.post(url, json=json_data, headers=headers, timeout=self.timeout)
        logger.info(f"HTTP POST {url} -> Status: {response.status_code}")
        return response

    def put(self, endpoint: str, json_data: dict = None, headers: dict = None):
        url = self._build_url(endpoint)
        response = self.session.put(url, json=json_data, headers=headers, timeout=self.timeout)
        logger.info(f"HTTP PUT {url} -> Status: {response.status_code}")
        return response

    