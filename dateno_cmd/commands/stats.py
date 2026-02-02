"""Statistics (statsdb) commands."""

from __future__ import annotations

from pathlib import Path

import typer

from dateno_cmd.services.context import build_context
from dateno_cmd.utils.command import run_and_render
from dateno_cmd.utils.errors import print_sdk_error


app = typer.Typer(no_args_is_help=True)


@app.command("ns")
def stats_list_namespaces(
    start: int = 0,
    limit: int = 100,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """List namespaces / databases (SDK: list_namespaces)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.list_namespaces(start=start, limit=limit),
        output,
    )


@app.command("ns-get")
def stats_get_namespace(
    ns_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get namespace metadata (SDK: get_namespace)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.get_namespace(ns_id=ns_id),
        output,
    )


@app.command("tables")
def stats_list_tables(
    ns_id: str,
    start: int = 0,
    limit: int = 100,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """List tables in a namespace (SDK: list_namespace_tables)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.list_namespace_tables(
            ns_id=ns_id, start=start, limit=limit
        ),
        output,
    )


@app.command("table")
def stats_get_table(
    ns_id: str,
    table_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get table metadata (SDK: get_namespace_table)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.get_namespace_table(
            ns_id=ns_id, table_id=table_id
        ),
        output,
    )


@app.command("indicators")
def stats_list_indicators(
    ns_id: str,
    start: int = 0,
    limit: int = 100,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """List indicators (SDK: list_indicators)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.list_indicators(
            ns_id=ns_id, start=start, limit=limit
        ),
        output,
    )


@app.command("indicator")
def stats_get_indicator(
    ns_id: str,
    ind_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get indicator metadata (SDK: get_namespace_indicator)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.get_namespace_indicator(
            ns_id=ns_id, ind_id=ind_id
        ),
        output,
    )


@app.command("ts")
def stats_list_timeseries(
    ns_id: str,
    start: int = 0,
    limit: int = 100,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """List timeseries (SDK: list_timeseries)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.list_timeseries(
            ns_id=ns_id, start=start, limit=limit
        ),
        output,
    )


@app.command("ts-get")
def stats_get_timeseries(
    ns_id: str,
    ts_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get timeseries metadata (SDK: get_timeseries)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.statistics_api.get_timeseries(ns_id=ns_id, ts_id=ts_id),
        output,
    )


@app.command("export-formats")
def stats_list_export_formats(
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """List exportable formats (SDK: list_export_formats)."""
    ctx = build_context(format, debug)
    run_and_render(ctx, ctx.sdk.statistics_api.list_export_formats, output)


@app.command("export")
def stats_export_timeseries(
    ns_id: str,
    ts_id: str,
    fileext: str = typer.Option(..., "--format", help="e.g. csv, xlsx, json"),
    output: str = typer.Option(..., "--output", "-o", help="Output file path"),
    debug: bool = False,
):
    """
    Export timeseries data to file (SDK: export_timeseries_file).
    """
    ctx = build_context(None, debug)
    try:
        resp = ctx.sdk.statistics_api.export_timeseries_file(
            ns_id=ns_id,
            ts_id=ts_id,
            fileext=fileext,
        )
    except Exception as e:
        print_sdk_error(e)
        return
    r = getattr(resp, "result", resp)
    if hasattr(r, "read"):
        r.read()
    content = getattr(r, "content", b"")
    if not isinstance(content, bytes):
        content = b""
    Path(output).write_bytes(content)
    print(f"Exported to {output}")
