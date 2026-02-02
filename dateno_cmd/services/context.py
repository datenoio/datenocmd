"""Context helpers for CLI commands."""

from __future__ import annotations

from dataclasses import dataclass
import logging

import click

from dateno_cmd.settings import Settings, get_settings
from dateno_cmd.sdk_factory import get_sdk


@dataclass
class CommandContext:
    settings: Settings
    sdk: object
    out_format: str


def _get_global_debug() -> bool:
    ctx = click.get_current_context(silent=True)
    if ctx and isinstance(ctx.obj, dict):
        return bool(ctx.obj.get("debug"))
    return False


def configure_logging(cli_debug: bool, settings_debug: bool) -> None:
    """
    Enable debug logging if explicitly requested via CLI or config.
    """
    if cli_debug or settings_debug:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=logging.DEBUG,
        )


def build_context(format_override: str | None, debug: bool) -> CommandContext:
    settings = get_settings().load_user_yaml_if_needed()
    effective_debug = debug or _get_global_debug()
    configure_logging(effective_debug, settings.debug)
    out_format = (format_override or settings.output_format or "yaml").strip().lower()
    sdk = get_sdk(settings)
    return CommandContext(settings=settings, sdk=sdk, out_format=out_format)
