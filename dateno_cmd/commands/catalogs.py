"""Catalogs commands."""

from __future__ import annotations

import typer

from dateno_cmd.services.context import build_context
from dateno_cmd.utils.command import run_and_render


app = typer.Typer(no_args_is_help=True)


@app.command("get")
def catalogs_get(
    catalog_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get a single data catalog by id (SDK-backed)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.data_catalogs_api.get_catalog_by_id(catalog_id=catalog_id),
        output,
    )


@app.command("list")
def catalogs_list(
    query: str = typer.Option("", "--query", "-q", help="Search query text (e.g. environment)"),
    limit: int = 10,
    offset: int = 0,
    software: str | None = None,
    owner_type: str | None = None,
    catalog_type: str | None = None,
    owner_country: str = typer.Option("", "--owner-country", help="Comma-separated country codes"),
    coverage_country: str = typer.Option("", "--coverage-country", help="Comma-separated country codes"),
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """List catalogs (SDK-backed)."""
    ctx = build_context(format, debug)
    owner_country_list = [c.strip() for c in owner_country.split(",") if c.strip()] or None
    coverage_country_list = [c.strip() for c in coverage_country.split(",") if c.strip()] or None
    run_and_render(
        ctx,
        lambda: ctx.sdk.data_catalogs_api.list_catalogs(
            q=query or "",
            limit=limit,
            offset=offset,
            software=software,
            owner_type=owner_type,
            catalog_type=catalog_type,
            owner_country=owner_country_list,
            coverage_country=coverage_country_list,
        ),
        output,
    )
