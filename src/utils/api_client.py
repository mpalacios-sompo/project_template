import requests
from typing import Optional, Any


class APIClient:
    """
    A reusable API client for making HTTP GET and POST requests with built-in
    error handling and response validation.

    Attributes:
        base_url (str): The base URL of the API.
        headers (dict): Default headers for all requests.
    """

    def __init__(self, base_url: str, headers: Optional[dict] = None):
        """
        Initialize the APIClient instance.

        Args:
            base_url (str): Base URL of the API service.
            headers (dict, optional): Default headers for all requests.
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def _full_url(self, path: str) -> str:
        """
        Construct a full URL from a relative path.

        Args:
            path (str): The API path relative to the base URL.

        Returns:
            str: The full URL.
        """
        return f"{self.base_url}/{path.lstrip('/')}"

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle an HTTP response by checking for errors and returning parsed content.

        Args:
            response (requests.Response): The response object.

        Returns:
            Any: Parsed response content (JSON or raw bytes).

        Raises:
            requests.HTTPError: If the response has a bad status code.
            ValueError: If response is not valid JSON (for JSON requests).
        """
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(
                f"HTTP error: {response.status_code} - {response.text}"
            ) from e

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                return response.json()
            except ValueError as e:
                raise ValueError("Invalid JSON response") from e
        return response.content

    def get(self, path: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> Any:
        """
        Send a GET request to the API.

        Args:
            path (str): API endpoint path.
            params (dict, optional): Query parameters.
            headers (dict, optional): Additional headers.

        Returns:
            Any: Parsed JSON or raw content from the response.
        """
        try:
            response = requests.get(
                self._full_url(path),
                params=params,
                headers={**self.headers, **(headers or {})}
            )
            return self._handle_response(response)
        except requests.ConnectionError as e:
            raise requests.ConnectionError("Connection error during GET request") from e
        except requests.Timeout as e:
            raise requests.Timeout("Timeout during GET request") from e

    def post(self, path: str, data: Optional[dict] = None, json: Optional[dict] = None,
             files: Optional[dict] = None, headers: Optional[dict] = None) -> Any:
        """
        Send a POST request to the API.

        Args:
            path (str): API endpoint path.
            data (dict, optional): Form data.
            json (dict, optional): JSON payload.
            files (dict, optional): Files to upload.
            headers (dict, optional): Additional headers.

        Returns:
            Any: Parsed JSON or raw content from the response.
        """
        try:
            response = requests.post(
                self._full_url(path),
                data=data,
                json=json,
                files=files,
                headers={**self.headers, **(headers or {})}
            )
            return self._handle_response(response)
        except requests.ConnectionError as e:
            raise requests.ConnectionError("Connection error during POST request") from e
        except requests.Timeout as e:
            raise requests.Timeout("Timeout during POST request") from e
