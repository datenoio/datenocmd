"""
Dateno CLI application.

Commands:
- dateno search ...   (get, query, dsl, similar, facets, facet)
- dateno raw ...     (get)
- dateno catalogs ... (get, list)
- dateno service ... (health)
- dateno stats ...   (ns, ns-get, tables, table, indicators, indicator, ts, ts-get, export-formats, export)
"""

from __future__ import annotations

import typer

from dateno_cmd import __version__

from dateno_cmd.commands import catalogs, raw, search, service, stats


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
app.add_typer(search.app, name="search")
app.add_typer(raw.app, name="raw")
app.add_typer(catalogs.app, name="catalogs")
app.add_typer(service.app, name="service")
app.add_typer(stats.app, name="stats")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
