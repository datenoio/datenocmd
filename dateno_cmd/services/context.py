"""Context helpers for CLI commands."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

import click

from dateno_cmd.settings import Settings, get_settings
from dateno_cmd.sdk_factory import get_sdk


@dataclass
class CommandContext:
    settings: Settings
    sdk: object
    out_format: str


def _get_cli_overrides() -> dict[str, Any]:
    ctx = click.get_current_context(silent=True)
    if ctx and isinstance(ctx.obj, dict):
        return ctx.obj
    return {}


def _apply_overrides(settings: Settings, overrides: dict[str, Any]) -> None:
    if overrides.get("apikey") is not None:
        settings.apikey = overrides["apikey"]
    if overrides.get("server_url") is not None:
        settings.server_url = overrides["server_url"]
    if overrides.get("timeout_ms") is not None:
        settings.timeout_ms = overrides["timeout_ms"]
    if overrides.get("retries") is not None:
        settings.retries = overrides["retries"]
    if overrides.get("debug") is not None:
        settings.debug = bool(overrides["debug"])


def configure_logging(cli_debug: bool, settings_debug: bool) -> None:
    """
    Enable debug logging if explicitly requested via CLI or config.
    """
    if cli_debug or settings_debug:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )


def load_settings_with_overrides() -> Settings:
    settings = get_settings().load_user_yaml_if_needed()
    overrides = _get_cli_overrides()
    _apply_overrides(settings, overrides)
    return settings


def build_context(format_override: str | None, debug: bool) -> CommandContext:
    settings = load_settings_with_overrides()
    if debug:
        settings.debug = True
    configure_logging(settings.debug, settings.debug)
    out_format = (format_override or settings.output_format or "yaml").strip().lower()
    sdk = get_sdk(settings)
    return CommandContext(settings=settings, sdk=sdk, out_format=out_format)
