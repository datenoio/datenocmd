"""Raw data access commands."""

from __future__ import annotations

import typer

from dateno_cmd.services.context import build_context
from dateno_cmd.utils.command import run_and_render


app = typer.Typer(no_args_is_help=True)


@app.command("get")
def raw_get(
    entry_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get a single raw entry by id (SDK-backed)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.raw_data_access.get_raw_entry_by_id(entry_id=entry_id),
        output,
    )
