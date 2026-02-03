"""Error handling helpers for SDK calls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import click
import httpx
import yaml

from dateno_cmd.utils.serialization import to_plain


EXIT_OK = 0
EXIT_INTERNAL = 1
EXIT_USER = 2
EXIT_NETWORK = 3
EXIT_API = 4


class UserInputError(RuntimeError):
    """Raised for user-caused errors (bad input / missing config)."""


@dataclass(frozen=True)
class ErrorInfo:
    code: int
    kind: str
    message: str | None = None
    status_code: int | None = None
    details: Any | None = None


def _get_status_code(e: Exception) -> int | None:
    resp = getattr(e, "response", None)
    if resp is not None:
        status_code = getattr(resp, "status_code", None)
        if status_code is not None:
            return status_code
    return getattr(e, "status_code", None)


def classify_error(e: Exception) -> ErrorInfo:
    if isinstance(e, UserInputError) or isinstance(e, click.BadParameter):
        return ErrorInfo(code=EXIT_USER, kind="User error", message=str(e))

    if isinstance(e, httpx.RequestError):
        return ErrorInfo(code=EXIT_NETWORK, kind="Network error", message=str(e))

    status_code = _get_status_code(e)
    body = getattr(e, "body", None)
    message = getattr(e, "message", None) or str(e)
    if status_code is not None:
        if 400 <= status_code < 500:
            return ErrorInfo(
                code=EXIT_USER,
                kind="User error",
                message=message,
                status_code=status_code,
                details=body,
            )
        return ErrorInfo(
            code=EXIT_API,
            kind="API error",
            message=message,
            status_code=status_code,
            details=body,
        )

    if body is not None:
        return ErrorInfo(
            code=EXIT_INTERNAL,
            kind="Internal error",
            message=message,
            details=body,
        )

    return ErrorInfo(code=EXIT_INTERNAL, kind="Internal error", message=message)


def print_sdk_error(e: Exception, debug: bool = False) -> int:
    """
    Универсальный печатник ошибок Speakeasy SDK:
    - ErrorResponse (400/422 с телом)
    - SDKDefaultError (401/500 с текстом)
    - ResponseValidationError (когда схема ответа не совпала)
    """
    info = classify_error(e)
    click.echo(f"Error: {info.kind}", err=True)
    if info.status_code is not None:
        click.echo(f"Status: {info.status_code}", err=True)
    if info.message:
        click.echo(f"Message: {info.message}", err=True)
    if info.details is not None:
        rendered = yaml.safe_dump(
            to_plain(info.details), sort_keys=False, allow_unicode=True
        ).rstrip()
        click.echo("Details:", err=True)
        click.echo(rendered, err=True)
    if debug:
        click.echo(f"Exception: {type(e).__name__}", err=True)
    return info.code
