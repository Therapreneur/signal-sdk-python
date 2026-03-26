# signal-therapreneur

Official Python SDK for **Signal by TheraPreneur** — AI Clinical Intelligence & Practice Management API.

## Installation

```bash
pip install signal-therapreneur
```

## Quick Start

```python
from signal_therapreneur import Signal

signal = Signal(api_key="sk_live_xxx")

# List active clients
result = signal.clients.list(status="active")
for client in result["data"]:
    print(client["name"])

# Create an appointment
appointment = signal.appointments.create(
    client_id="client-123",
    scheduled_at="2026-04-01T10:00:00Z",
    duration_minutes=50,
    session_type="individual",
)
```

## Configuration

```python
signal = Signal(
    api_key="sk_live_xxx",           # Required — your API key
    base_url="https://...",          # Optional — override API base URL
    timeout=30,                      # Optional — request timeout in seconds (default: 30)
)
```

The client also works as a context manager:

```python
with Signal(api_key="sk_live_xxx") as signal:
    clients = signal.clients.list()
```

## Resources

### Clients

```python
# List clients with optional filters
result = signal.clients.list(status="active", search="Jane", limit=20)

# Get a single client
client = signal.clients.get("client-123")

# Create a client
new_client = signal.clients.create(
    name="Jane Doe",
    email="jane@example.com",
    phone="555-0100",
    date_of_birth="1990-05-15",
    diagnosis=["F41.1"],
    insurance={"payer": "Aetna", "member_id": "AET123456"},
)

# Update a client
signal.clients.update("client-123", phone="555-0200")

# Delete a client
signal.clients.delete("client-123")
```

### Appointments

```python
# List appointments in a date range
appts = signal.appointments.list(
    start_date="2026-04-01",
    end_date="2026-04-07",
    status="scheduled",
)

# Get a single appointment
appt = signal.appointments.get("appt-456")

# Create an appointment
new_appt = signal.appointments.create(
    client_id="client-123",
    scheduled_at="2026-04-01T10:00:00Z",
    duration_minutes=50,
    session_type="individual",
    session_format="telehealth",
    practitioner_id="pract-789",
    notes="Follow-up session",
)

# Update an appointment
signal.appointments.update("appt-456", notes="Rescheduled")

# Cancel an appointment
signal.appointments.cancel("appt-456", reason="Client requested reschedule")
```

### Sessions

```python
# List sessions for a client
sessions = signal.sessions.list(client_id="client-123")

# Get session details
session = signal.sessions.get("session-789")

# Get the clinical note for a session
note = signal.sessions.get_note("session-789")
```

### Claims

```python
# List claims
claims = signal.claims.list(status="pending", client_id="client-123")

# Get claim details
claim = signal.claims.get("claim-001")

# Create a claim
new_claim = signal.claims.create(
    client_id="client-123",
    session_id="session-789",
    diagnosis_codes=["F41.1"],
    cpt_code="90837",
)
```

### Insurance

```python
# Check client eligibility
eligibility = signal.insurance.check_eligibility("client-123")
```

### Practitioners

```python
# List all practitioners
practitioners = signal.practitioners.list()

# Get practitioner details
practitioner = signal.practitioners.get("pract-789")

# Get availability for a specific date
availability = signal.practitioners.get_availability("pract-789", date="2026-04-01")
```

### Webhooks

```python
# List webhooks
webhooks = signal.webhooks.list()

# Create a webhook
webhook = signal.webhooks.create(
    url="https://your-app.com/webhooks/signal",
    events=["appointment.created", "appointment.cancelled", "session.completed"],
    secret="whsec_your_secret",
)

# List available webhook events
events = signal.webhooks.list_events()

# Delete a webhook
signal.webhooks.delete("wh-001")
```

## Error Handling

```python
from signal_therapreneur import Signal, SignalAPIError

signal = Signal(api_key="sk_live_xxx")

try:
    client = signal.clients.get("nonexistent")
except SignalAPIError as e:
    print(f"API Error {e.status}: {e}")
    print(f"Response body: {e.body}")

    if e.status == 401:
        print("Invalid API key")
    elif e.status == 403:
        print("Insufficient permissions")
    elif e.status == 404:
        print("Resource not found")
    elif e.status == 429:
        print("Rate limited — slow down")
```

## Webhook Verification

When receiving webhook events, verify the signature using the secret you provided:

```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected)
```

## Documentation

Full API documentation is available at [https://signal.therapreneur.app/api/docs](https://signal.therapreneur.app/api/docs).

## License

MIT
