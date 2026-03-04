import requests
from flask import current_app
from requests.exceptions import RequestException
from .errors import APIError

class CatalogClient:
    def __init__(self):
        self.base_url = current_app.config.get("CATALOG_SERVICE_URL").rstrip("/")
        self.timeout = current_app.config.get("REQUESTS_TIMEOUT", 5)

    def get_book(self, book_id):
        try:
            resp = requests.get(f"{self.base_url}/api/catalog/books/{book_id}", timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except RequestException as e:
            current_app.logger.error("Catalog get_book error: %s", e)
            raise APIError("Catalog service unavailable", status_code=502)

    def reserve_book(self, book_id, user_id):
        """
        Instruct Catalog to reserve/check out a copy. Catalog should perform atomic decrement.
        Expected endpoint (catalog service must implement): POST /api/catalog/books/<book_id>/reserve
        JSON body: {"user_id": "..."}
        Returns 200 with book info if success, 409 or 400 if unavailable.
        """
        try:
            resp = requests.post(
                f"{self.base_url}/api/catalog/books/{book_id}/reserve",
                json={"user_id": user_id},
                timeout=self.timeout
            )
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 409:
                raise APIError("Book not available", status_code=409)
            else:
                raise APIError("Failed to reserve book", status_code=resp.status_code)
        except RequestException as e:
            current_app.logger.error("Catalog reserve_book error: %s", e)
            raise APIError("Catalog service unavailable", status_code=502)

    def release_book(self, book_id, user_id):
        """
        Notify Catalog that a copy has been returned; catalog should increment copies_available.
        Expected endpoint (catalog service must implement): POST /api/catalog/books/<book_id>/release
        """
        try:
            resp = requests.post(
                f"{self.base_url}/api/catalog/books/{book_id}/release",
                json={"user_id": user_id},
                timeout=self.timeout
            )
            resp.raise_for_status()
            return resp.json()
        except RequestException as e:
            current_app.logger.error("Catalog release_book error: %s", e)
            # release failures are serious but we still attempt to mark returned locally; surface error
            raise APIError("Catalog service unavailable", status_code=502)
