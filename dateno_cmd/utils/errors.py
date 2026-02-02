"""Error handling helpers for SDK calls."""

from __future__ import annotations

import yaml

from dateno_cmd.utils.serialization import to_plain


def print_sdk_error(e: Exception) -> None:
    """
    Универсальный печатник ошибок Speakeasy SDK:
    - ErrorResponse (400/422 с телом)
    - SDKDefaultError (401/500 с текстом)
    - ResponseValidationError (когда схема ответа не совпала)
    """
    body = getattr(e, "body", None)
    message = getattr(e, "message", None)

    status_code = None
    resp = getattr(e, "response", None)
    if resp is not None:
        status_code = getattr(resp, "status_code", None)

    if status_code:
        print(f"SDK error (HTTP {status_code})")
    if message:
        print(message)

    if body is not None:
        print(yaml.safe_dump(to_plain(body), sort_keys=False, allow_unicode=True))
        return

    print(str(e))
