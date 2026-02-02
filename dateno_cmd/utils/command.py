"""Shared command helpers for DRY output handling."""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from dateno_cmd.services.context import CommandContext
from dateno_cmd.utils.errors import print_sdk_error
from dateno_cmd.utils.io import write_or_print
from dateno_cmd.utils.serialization import render_output


def run_and_render(
    ctx: CommandContext,
    call: Callable[[], object],
    output: Optional[str],
) -> object | None:
    """
    Execute SDK call, print errors, and render output.
    Returns the result or None on error.
    """
    try:
        result = call()
    except Exception as e:
        print_sdk_error(e)
        return None
    rendered = render_output(result, ctx.out_format)
    write_or_print(rendered, output)
    return result
