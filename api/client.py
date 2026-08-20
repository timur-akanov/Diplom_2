"""Base HTTP client for API requests."""

import requests


class APIClient:
    """Low-level HTTP client for making requests to the API."""

    def __init__(self, timeout=10):
        self.timeout = timeout

    def get(self, url, headers=None):
        """Perform GET request."""
        response = requests.get(url, headers=headers, timeout=self.timeout)
        return response

    def post(self, url, json=None, headers=None):
        """Perform POST request."""
        response = requests.post(url, json=json, headers=headers, timeout=self.timeout)
        return response

    def patch(self, url, json=None, headers=None):
        """Perform PATCH request."""
        response = requests.patch(url, json=json, headers=headers, timeout=self.timeout)
        return response

    def delete(self, url, headers=None):
        """Perform DELETE request."""
        response = requests.delete(url, headers=headers, timeout=self.timeout)
        return response
