"""Signal API client."""

import httpx
from typing import Optional, Any, Dict


class SignalAPIError(Exception):
    """Raised when the Signal API returns an error response."""

    def __init__(self, status: int, message: str, body: Any = None):
        self.status = status
        self.body = body
        super().__init__(message)


class Signal:
    """Signal by TheraPreneur API client.

    Args:
        api_key: Your API key (starts with sk_live_ or sk_test_)
        base_url: API base URL (default: production)
        timeout: Request timeout in seconds (default: 30)

    Example::

        from signal_therapreneur import Signal

        signal = Signal(api_key="sk_live_xxx")
        clients = signal.clients.list(status="active")
    """

    DEFAULT_BASE_URL = "https://calpay-backend-626763732019.us-central1.run.app/api/v1"

    def __init__(self, api_key: str, base_url: str = None, timeout: int = 30):
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self._http = httpx.Client(
            base_url=self.base_url,
            headers={
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "User-Agent": f"signal-sdk-python/{__import__('signal_therapreneur').__version__}",
            },
            timeout=self.timeout,
        )

        from .resources import (
            ClientsResource,
            AppointmentsResource,
            SessionsResource,
            ClaimsResource,
            PractitionersResource,
            WebhooksResource,
            InsuranceResource,
        )

        self.clients = ClientsResource(self)
        self.appointments = AppointmentsResource(self)
        self.sessions = SessionsResource(self)
        self.claims = ClaimsResource(self)
        self.practitioners = PractitionersResource(self)
        self.webhooks = WebhooksResource(self)
        self.insurance = InsuranceResource(self)

    def request(self, method: str, path: str, json: Dict = None, params: Dict = None) -> Any:
        """Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            json: Request body as dict
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            SignalAPIError: If the API returns a non-success status
        """
        # Filter None params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        response = self._http.request(method, path, json=json, params=params)

        if not response.is_success:
            try:
                body = response.json()
                message = body.get("detail", response.text)
            except Exception:
                message = response.text
                body = None
            raise SignalAPIError(response.status_code, message, body)

        return response.json()

    def close(self):
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
