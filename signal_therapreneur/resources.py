"""API resource classes."""

from typing import Optional, List, Dict, Any


class ClientsResource:
    """Manage therapy clients."""

    def __init__(self, client):
        self._client = client

    def list(self, status: str = None, search: str = None, limit: int = 50, offset: int = 0) -> Dict:
        """List clients with optional filters.

        Args:
            status: Filter by status (e.g., 'active', 'inactive')
            search: Search by name or email
            limit: Max results per page (default: 50)
            offset: Pagination offset
        """
        return self._client.request("GET", "/clients", params={
            "status": status, "search": search, "limit": limit, "offset": offset,
        })

    def get(self, client_id: str) -> Dict:
        """Get a single client by ID."""
        return self._client.request("GET", f"/clients/{client_id}")

    def create(
        self,
        name: str,
        email: str = None,
        phone: str = None,
        date_of_birth: str = None,
        diagnosis: List[str] = None,
        insurance: Dict = None,
    ) -> Dict:
        """Create a new client.

        Args:
            name: Client full name (required)
            email: Email address
            phone: Phone number
            date_of_birth: Date of birth (YYYY-MM-DD)
            diagnosis: List of ICD-10 diagnosis codes
            insurance: Insurance info dict with 'payer' and 'member_id'
        """
        return self._client.request("POST", "/clients", json={
            "name": name, "email": email, "phone": phone,
            "date_of_birth": date_of_birth, "diagnosis": diagnosis, "insurance": insurance,
        })

    def update(self, client_id: str, **kwargs) -> Dict:
        """Update a client. Pass any fields to update as keyword arguments."""
        return self._client.request("PUT", f"/clients/{client_id}", json=kwargs)

    def delete(self, client_id: str) -> Dict:
        """Delete a client by ID."""
        return self._client.request("DELETE", f"/clients/{client_id}")


class AppointmentsResource:
    """Manage appointments and scheduling."""

    def __init__(self, client):
        self._client = client

    def list(
        self,
        start_date: str = None,
        end_date: str = None,
        client_id: str = None,
        status: str = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict:
        """List appointments with optional filters.

        Args:
            start_date: Filter from date (YYYY-MM-DD)
            end_date: Filter to date (YYYY-MM-DD)
            client_id: Filter by client
            status: Filter by status (scheduled, completed, cancelled)
            limit: Max results per page
            offset: Pagination offset
        """
        return self._client.request("GET", "/appointments", params={
            "start_date": start_date, "end_date": end_date, "client_id": client_id,
            "status": status, "limit": limit, "offset": offset,
        })

    def get(self, appointment_id: str) -> Dict:
        """Get a single appointment by ID."""
        return self._client.request("GET", f"/appointments/{appointment_id}")

    def create(
        self,
        client_id: str,
        scheduled_at: str,
        duration_minutes: int = 50,
        session_type: str = "individual",
        session_format: str = "telehealth",
        practitioner_id: str = None,
        notes: str = None,
    ) -> Dict:
        """Create a new appointment.

        Args:
            client_id: Client ID (required)
            scheduled_at: ISO 8601 datetime (required)
            duration_minutes: Session duration in minutes (default: 50)
            session_type: Type of session (individual, couple, group)
            session_format: Format (telehealth, in_person)
            practitioner_id: Practitioner to assign
            notes: Appointment notes
        """
        return self._client.request("POST", "/appointments", json={
            "client_id": client_id, "scheduled_at": scheduled_at,
            "duration_minutes": duration_minutes, "session_type": session_type,
            "session_format": session_format, "practitioner_id": practitioner_id, "notes": notes,
        })

    def update(self, appointment_id: str, **kwargs) -> Dict:
        """Update an appointment. Pass any fields to update as keyword arguments."""
        return self._client.request("PUT", f"/appointments/{appointment_id}", json=kwargs)

    def cancel(self, appointment_id: str, reason: str = None) -> Dict:
        """Cancel an appointment.

        Args:
            appointment_id: Appointment to cancel
            reason: Cancellation reason
        """
        return self._client.request("POST", f"/appointments/{appointment_id}/cancel", json={"reason": reason})


class SessionsResource:
    """Access completed therapy sessions and clinical notes (read-only)."""

    def __init__(self, client):
        self._client = client

    def list(
        self,
        client_id: str = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict:
        """List therapy sessions."""
        return self._client.request("GET", "/sessions", params={
            "client_id": client_id, "start_date": start_date, "end_date": end_date,
            "limit": limit, "offset": offset,
        })

    def get(self, session_id: str) -> Dict:
        """Get session details."""
        return self._client.request("GET", f"/sessions/{session_id}")

    def get_note(self, session_id: str) -> Dict:
        """Get the clinical note for a session."""
        return self._client.request("GET", f"/sessions/{session_id}/note")


class ClaimsResource:
    """Manage insurance claims."""

    def __init__(self, client):
        self._client = client

    def list(self, status: str = None, client_id: str = None, limit: int = 50) -> Dict:
        """List insurance claims."""
        return self._client.request("GET", "/claims", params={
            "status": status, "client_id": client_id, "limit": limit,
        })

    def get(self, claim_id: str) -> Dict:
        """Get claim details."""
        return self._client.request("GET", f"/claims/{claim_id}")

    def create(self, **kwargs) -> Dict:
        """Create an insurance claim."""
        return self._client.request("POST", "/claims", json=kwargs)


class InsuranceResource:
    """Insurance eligibility verification."""

    def __init__(self, client):
        self._client = client

    def check_eligibility(self, client_id: str) -> Dict:
        """Check insurance eligibility for a client.

        Args:
            client_id: Client ID to check eligibility for
        """
        return self._client.request("GET", f"/eligibility/{client_id}")


class PractitionersResource:
    """Manage practitioners and availability."""

    def __init__(self, client):
        self._client = client

    def list(self) -> Dict:
        """List all practitioners in the practice."""
        return self._client.request("GET", "/practitioners")

    def get(self, practitioner_id: str) -> Dict:
        """Get practitioner details."""
        return self._client.request("GET", f"/practitioners/{practitioner_id}")

    def get_availability(self, practitioner_id: str, date: str = None) -> Dict:
        """Get practitioner availability.

        Args:
            practitioner_id: Practitioner ID
            date: Date to check (YYYY-MM-DD), defaults to today
        """
        return self._client.request("GET", f"/practitioners/{practitioner_id}/availability", params={"date": date})


class WebhooksResource:
    """Manage webhook subscriptions."""

    def __init__(self, client):
        self._client = client

    def list(self) -> Dict:
        """List all webhook subscriptions."""
        return self._client.request("GET", "/webhooks")

    def create(self, url: str, events: List[str], secret: str = None) -> Dict:
        """Create a webhook subscription.

        Args:
            url: Endpoint URL to receive events
            events: List of event types to subscribe to
            secret: Signing secret for verifying payloads
        """
        return self._client.request("POST", "/webhooks", json={
            "url": url, "events": events, "secret": secret,
        })

    def delete(self, webhook_id: str) -> Dict:
        """Delete a webhook subscription."""
        return self._client.request("DELETE", f"/webhooks/{webhook_id}")

    def list_events(self) -> Dict:
        """List all available webhook event types."""
        return self._client.request("GET", "/webhooks/events")
