"""
SDK factory for Dateno CLI.

Responsible for:
- Creating and configuring a singleton SDK client
- Wiring SDK configuration with CLI settings
- Centralizing authentication and transport configuration

This module MUST NOT perform any I/O or CLI parsing.
"""

from __future__ import annotations

from typing import Optional
import inspect

import httpx

from dateno.sdk import SDK
from dateno.utils import RetryConfig

from dateno_cmd.settings import Settings


_sdk_instance: Optional[SDK] = None


def _build_retry_config(retries: int) -> Optional[RetryConfig]:
    """
    Build RetryConfig in a version-tolerant way.

    Speakeasy-generated SDKs may change RetryConfig constructor parameter names.
    We therefore inspect the signature and map CLI "retries" to the supported arg.
    """
    if not retries or retries <= 0:
        return None

    sig = inspect.signature(RetryConfig)
    params = sig.parameters

    candidates = [
        "max_retries",
        "retries",
        "max_attempts",
        "max_retry_count",
        "retry_count",
        "attempts",
    ]

    for name in candidates:
        if name in params:
            return RetryConfig(**{name: retries})

    non_self = [p for p in params.values()]
    if len(non_self) == 1:
        return RetryConfig(retries)  # type: ignore[misc]

    return None


def _build_http_clients(apikey: str, timeout_ms: int) -> tuple[httpx.Client, httpx.AsyncClient]:
    """
    Build preconfigured HTTPX clients for the SDK.

    The API supports API key auth via:
    - Authorization: Bearer <key>
    - Query param ?apikey=<key>

    The generated SDK currently injects the key via query param (api_key_query).
    Some endpoints may require the Authorization header, so we proactively set it here.

    :param apikey: API key string
    :param timeout_ms: Timeout in milliseconds
    :return: (sync_client, async_client)
    """
    timeout_s = max(1.0, float(timeout_ms or 30000) / 1000.0)

    headers = {
        "Authorization": f"Bearer {apikey}",
    }

    client = httpx.Client(
        follow_redirects=True,
        headers=headers,
        timeout=timeout_s,
    )
    async_client = httpx.AsyncClient(
        follow_redirects=True,
        headers=headers,
        timeout=timeout_s,
    )
    return client, async_client


def get_sdk(settings: Settings) -> SDK:
    """
    Create (or return cached) SDK instance configured from CLI settings.

    The SDK instance is cached for the lifetime of the process to avoid:
    - recreating HTTP clients
    - losing connection pools
    - inconsistent retry / timeout behavior

    :param settings: Loaded CLI settings
    :return: Configured SDK instance
    """
    global _sdk_instance

    if _sdk_instance is not None:
        return _sdk_instance

    if not settings.apikey:
        raise RuntimeError(
            "API key is not configured. "
            "Please provide it via .dateno_cmd.yaml (apikey: ...) or DATENO_APIKEY env var."
        )

    retry_config = _build_retry_config(settings.retries or 0)

    client, async_client = _build_http_clients(
        apikey=settings.apikey,
        timeout_ms=settings.timeout_ms or 30000,
    )

    _sdk_instance = SDK(
        api_key_query=settings.apikey,  # used by SDK to inject ?apikey=
        server_url=settings.server_url,
        client=client,
        async_client=async_client,
        timeout_ms=settings.timeout_ms,
        retry_config=retry_config,
    )
    return _sdk_instance
