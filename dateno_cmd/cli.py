"""
Dateno CLI application.

Commands:
- dateno search ...   (get, query, dsl, similar, facets, facet)
- dateno raw ...     (get)
- dateno catalogs ... (get, list)
- dateno service ... (health)
- dateno stats ...   (ns, ns-get, tables, table, indicators, indicator, ts, ts-get, export-formats, export)
- dateno config ...  (init, show)
"""

from __future__ import annotations

import typer

from dateno_cmd import __version__

from dateno_cmd.commands import catalogs, config, raw, search, service, stats


app = typer.Typer(no_args_is_help=True)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def _main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug logging.",
    ),
    apikey: str | None = typer.Option(
        None,
        "--apikey",
        "--api-key",
        help="Override API key for this command only (may be stored in shell history).",
    ),
    server_url: str | None = typer.Option(
        None,
        "--server-url",
        help="Override API base URL for this command only.",
    ),
    timeout_ms: int | None = typer.Option(
        None,
        "--timeout-ms",
        help="Override request timeout in milliseconds for this command only.",
    ),
    retries: int | None = typer.Option(
        None,
        "--retries",
        help="Override retry count for this command only.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        help="Show CLI version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug
    ctx.obj["apikey"] = apikey
    ctx.obj["server_url"] = server_url
    ctx.obj["timeout_ms"] = timeout_ms
    ctx.obj["retries"] = retries
app.add_typer(search.app, name="search")
app.add_typer(raw.app, name="raw")
app.add_typer(catalogs.app, name="catalogs")
app.add_typer(service.app, name="service")
app.add_typer(stats.app, name="stats")
app.add_typer(config.app, name="config")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
