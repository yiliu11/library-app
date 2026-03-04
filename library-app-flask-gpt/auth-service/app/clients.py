import requests
from flask import current_app
from requests.exceptions import RequestException

class BookCatalogClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.timeout = current_app.config.get("REQUESTS_TIMEOUT", 5)

    def get_book(self, book_id):
        try:
            resp = requests.get(f"{self.base_url}/api/catalog/books/{book_id}", timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except RequestException as e:
            current_app.logger.error("Catalog service error: %s", e)
            raise

# Add other clients similarly; instantiate in endpoints when needed.
