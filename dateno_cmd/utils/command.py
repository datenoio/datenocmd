"""Shared command helpers for DRY output handling."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

import typer

from dateno_cmd.services.context import CommandContext
from dateno_cmd.utils.errors import print_sdk_error
from dateno_cmd.utils.io import write_or_print
from dateno_cmd.utils.serialization import render_output, to_plain


def call_sdk(ctx: CommandContext, call: Callable[[], object]) -> object:
    """
    Execute SDK call and raise typer.Exit on error.
    """
    try:
        return call()
    except typer.Exit:
        raise
    except Exception as e:
        settings = getattr(ctx, "settings", None)
        debug = bool(getattr(settings, "debug", False)) if settings is not None else False
        code = print_sdk_error(e, debug=debug)
        raise typer.Exit(code=code)


def run_and_render(
    ctx: CommandContext,
    call: Callable[[], object],
    output: Optional[str],
) -> object:
    """
    Execute SDK call, render output, and write to file/stdout.
    """
    result = call_sdk(ctx, call)
    rendered = render_output(result, ctx.out_format)
    write_or_print(rendered, output)
    return result


def run_and_render_with_mode(
    ctx: CommandContext,
    call: Callable[[], object],
    mode: str,
    output: Optional[str],
    raw_mode: str = "raw",
) -> dict | None:
    """
    Execute SDK call and handle raw output. Returns a dict for further processing.
    """
    result = call_sdk(ctx, call)
    if mode == raw_mode:
        rendered = render_output(result, ctx.out_format)
        write_or_print(rendered, output)
        return None
    data_dict = to_plain(result)
    if not isinstance(data_dict, dict):
        rendered = render_output(data_dict, ctx.out_format)
        write_or_print(rendered, output)
        return None
    return data_dict
