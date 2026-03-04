import requests
from flask import current_app
from requests.exceptions import RequestException

class AuthClient:
    """
    Example client if you want to validate tokens by calling the Auth Service.
    Left as optional — default implementation decodes JWT locally.
    """
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.timeout = current_app.config.get("REQUESTS_TIMEOUT", 5)

    def me(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            resp = requests.get(f"{self.base_url}/api/auth/me", headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except RequestException as e:
            current_app.logger.error("Auth service /me error: %s", e)
            raise
