"""HTTP clients scoped to hosted model calls, not other application traffic."""

import logging

import httpx

logger = logging.getLogger(__name__)


def create_model_client(*, timeout: float, tls_verify: bool = True) -> httpx.Client:
    if not tls_verify:
        logger.warning(
            "DEVELOPMENT ONLY: model gateway TLS certificate verification is disabled. "
            "Use synthetic data and a restricted test key; restore MODEL_TLS_VERIFY=true."
        )
    return httpx.Client(timeout=timeout, verify=tls_verify)
