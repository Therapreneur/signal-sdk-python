"""
Signal by TheraPreneur — Official Python SDK

AI Clinical Intelligence & Practice Management API

Example:
    from signal_therapreneur import Signal

    signal = Signal(api_key="sk_live_xxx")
    clients = signal.clients.list(status="active")
"""

from .client import Signal, SignalAPIError
from .resources import *

__version__ = "1.0.0"
__all__ = ["Signal", "SignalAPIError"]
