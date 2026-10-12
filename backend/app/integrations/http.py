"""TLS trust settings for hosted provider calls.

Internal model endpoints often use a private CA that is not in the system trust
store. ``MODEL_CA_BUNDLE`` points at that CA file; ``MODEL_TLS_VERIFY=false`` is
available for a trusted internal dev endpoint only and must never be used for
public traffic.
"""

from app.config import Settings


def verify_setting(settings: Settings) -> bool | str:
    if settings.model_ca_bundle:
        return settings.model_ca_bundle
    return settings.model_tls_verify
