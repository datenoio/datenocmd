"""Config commands."""

from __future__ import annotations

from pathlib import Path

import typer

from dateno_cmd.services.context import load_settings_with_overrides
from dateno_cmd.settings import DEFAULT_CONFIGFILE
from dateno_cmd.utils.io import write_or_print
from dateno_cmd.utils.serialization import render_output


app = typer.Typer(no_args_is_help=True)


def _mask_apikey(value: str | None) -> str | None:
    if not value:
        return None
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


@app.command("init")
def config_init(
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing config file."
    ),
):
    """
    Create a default .dateno_cmd.yaml in the current directory.
    """
    path = Path.cwd() / DEFAULT_CONFIGFILE
    if path.exists() and not force:
        typer.echo(f"Config file already exists: {path}")
        if not typer.confirm("Overwrite it?", default=False):
            return

    template = (
        "# Dateno CLI config\n"
        'apikey: ""\n'
        '# server_url: "https://apiv2.dateno.io"\n'
        "# timeout_ms: 30000\n"
        "# retries: 2\n"
        '# output_format: "yaml"\n'
        "# debug: false\n"
    )
    path.write_text(template, encoding="utf-8")
    typer.echo(f"Created {path}")


@app.command("show")
def config_show(
    format: str = typer.Option("yaml", "--format", help="yaml|json"),
    output: str | None = None,
):
    """
    Show effective config (with masked API key).
    """
    settings = load_settings_with_overrides()
    payload = {
        "apikey": _mask_apikey(settings.apikey),
        "server_url": settings.server_url,
        "timeout_ms": settings.timeout_ms,
        "retries": settings.retries,
        "output_format": settings.output_format,
        "debug": settings.debug,
    }
    rendered = render_output(payload, format)
    write_or_print(rendered, output)
