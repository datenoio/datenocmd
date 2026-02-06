"""Service commands."""

from __future__ import annotations

import typer

from dateno_cmd.services.context import build_context
from dateno_cmd.utils.command import run_and_render


app = typer.Typer(no_args_is_help=True)


@app.command("health")
def service_health(
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Health check endpoint (SDK-backed)."""
    ctx = build_context(format, debug)
    run_and_render(ctx, ctx.sdk.service.get_healthz, output)
