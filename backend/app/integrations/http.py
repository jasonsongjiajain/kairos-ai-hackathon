"""Shared HTTPS and retry behavior for hosted provider calls.

Internal model endpoints often use a private CA that is not in the system trust
store. ``MODEL_CA_BUNDLE`` points at that CA file; ``MODEL_TLS_VERIFY=false`` is
available for a trusted internal dev endpoint only and must never be used for
public traffic.

The provider endpoints can be flaky on internal networks, so transient transport
errors (connect/read/timeout) are retried a small number of times. HTTP status
errors are never retried.
"""

import time

import httpx

from app.config import Settings

RETRYABLE_TRANSPORT_ERRORS = (httpx.TransportError,)
DEFAULT_ATTEMPTS = 3


def verify_setting(settings: Settings) -> bool | str:
    if settings.model_ca_bundle:
        return settings.model_ca_bundle
    return settings.model_tls_verify


def post_json(
    client: httpx.Client,
    url: str,
    *,
    headers: dict[str, str],
    payload: dict,
    attempts: int = DEFAULT_ATTEMPTS,
) -> httpx.Response:
    """POST JSON, retrying transient transport failures with a short backoff."""
    last_error: httpx.TransportError | None = None
    for attempt in range(attempts):
        try:
            return client.post(url, headers=headers, json=payload)
        except RETRYABLE_TRANSPORT_ERRORS as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(0.5 * (attempt + 1))
    assert last_error is not None
    raise last_error
