import requests
from requests.exceptions import RequestException
from flask import current_app
from .errors import APIError

class AuthClient:
    """
    Interacts with the Authentication Service for user creation.
    Assumes the Auth Service exposes:
      - POST /api/auth/admin/register  (librarian JWT required)
        Body: {username, email, password, role}
        Response: {id, username, email, role, created_at}
    """
    def __init__(self):
        self.base_url = current_app.config.get("AUTH_SERVICE_URL", "").rstrip("/")
        self.timeout = current_app.config.get("REQUESTS_TIMEOUT", 5)

    def admin_register(self, token: str, username: str, email: str, password: str, role: str):
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"username": username, "email": email, "password": password, "role": role}
        try:
            resp = requests.post(
                f"{self.base_url}/api/auth/admin/register",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            if resp.status_code == 201:
                return resp.json()
            elif resp.status_code in (400, 409):
                raise APIError(resp.json().get("error", "Auth service error"), status_code=resp.status_code)
            elif resp.status_code == 401:
                raise APIError("Unauthorized to call Auth service", status_code=401)
            else:
                raise APIError("Auth service failed to create user", status_code=resp.status_code)
        except RequestException as e:
            current_app.logger.error("Auth service register error: %s", e)
            raise APIError("Authentication service unavailable", status_code=502)
