"""Search commands."""

from __future__ import annotations

from typing import Any

import typer
from flatdict import FlatDict
from tabulate import tabulate

from dateno_cmd.services.context import build_context
from dateno_cmd.utils.command import run_and_render
from dateno_cmd.utils.errors import print_sdk_error
from dateno_cmd.utils.io import load_json_arg, write_csv, write_or_print
from dateno_cmd.utils.search import extract_doc_from_item, extract_hits_list
from dateno_cmd.utils.sdk import call_sdk_flexible
from dateno_cmd.utils.serialization import render_output, to_plain


app = typer.Typer(no_args_is_help=True)


@app.command("get")
def search_get(
    entry_id: str,
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """Get a single search entry by id (SDK-backed)."""
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.search_api.get_dataset_by_entry_id(entry_id=entry_id),
        output,
    )


@app.command("query")
def search_query(
    query: str,
    filters: str = "",
    mode: str = "results",
    format: str | None = None,
    headers: str = "id,dataset.title,source.name,source.uid",
    output: str | None = None,
    limit: int = 10,
    offset: int = 0,
    facets: bool = typer.Option(
        False,
        "--facets/--no-facets",
        help="Request facets/aggregations from API.",
    ),
    sort_by: str | None = None,
    debug: bool = False,
):
    """
    Search datasets via SDK.

    Modes:
      - results: tabular output (default)
      - raw: full response as yaml/json
      - facets: only aggregations/facets part (yaml/json)
      - totals: only total hits number
    """
    ctx = build_context(format, debug)
    sdk_filters = [f.strip() for f in (filters.split(";") if filters else []) if f.strip()]

    try:
        result = ctx.sdk.search_api.search_datasets(
            q=query,
            filters=sdk_filters or None,
            limit=limit,
            offset=offset,
            facets=facets,
            sort_by=sort_by,
        )
    except Exception as e:
        print_sdk_error(e)
        return

    if mode == "raw":
        rendered = render_output(result, ctx.out_format)
        write_or_print(rendered, output)
        return

    data_dict = to_plain(result)
    if not isinstance(data_dict, dict):
        rendered = render_output(data_dict, ctx.out_format)
        write_or_print(rendered, output)
        return

    if mode == "totals":
        total = ""
        hits = data_dict.get("hits")
        if isinstance(hits, dict):
            total_obj = hits.get("total")
            if isinstance(total_obj, dict):
                total = total_obj.get("value", "")
            else:
                total = hits.get("total", "") or data_dict.get("total", "") or data_dict.get(
                    "estimated_total", ""
                )
        else:
            total = data_dict.get("total", "") or data_dict.get("estimated_total", "") or data_dict.get(
                "total_hits", ""
            )
        write_or_print(str(total if total is not None else ""), output)
        return

    if mode == "facets":
        aggs = data_dict.get("aggregations") or data_dict.get("facets") or {}
        rendered = render_output(aggs, ctx.out_format)
        write_or_print(rendered, output)
        return

    header_list = [h.strip() for h in headers.split(",") if h.strip()]
    items = extract_hits_list(data_dict)

    rows: list[list[Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        doc = extract_doc_from_item(item)
        flat = FlatDict(doc, delimiter=".")
        rows.append([flat.get(h, "") for h in header_list])

    if output:
        write_csv(header_list, rows, output)
    else:
        print(tabulate(rows, headers=header_list))


@app.command("dsl")
def search_dsl(
    body: str = typer.Option(..., "--body", help="JSON string or @file.json"),
    mode: str = typer.Option("raw", "--mode", help="raw|results|facets|totals"),
    headers: str = "id,dataset.title,source.name,source.uid",
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """
    POST /search/0.2/query_dsl -> sdk.search_api.search_datasets_dsl

    Examples:
      dateno search dsl --body @query.json --mode raw
      dateno search dsl --body '{"query":{"match_all":{}}}' --mode results
    """
    ctx = build_context(format, debug)
    payload = load_json_arg(body)

    try:
        result = call_sdk_flexible(ctx.sdk.search_api.search_datasets_dsl, body=payload)
    except Exception as e:
        print_sdk_error(e)
        return

    if mode == "raw":
        rendered = render_output(result, ctx.out_format)
        write_or_print(rendered, output)
        return

    data_dict = to_plain(result)
    if not isinstance(data_dict, dict):
        rendered = render_output(data_dict, ctx.out_format)
        write_or_print(rendered, output)
        return

    if mode == "totals":
        total = ""
        hits = data_dict.get("hits")
        if isinstance(hits, dict):
            total_obj = hits.get("total")
            if isinstance(total_obj, dict):
                total = total_obj.get("value", "")
        write_or_print(str(total), output)
        return

    if mode == "facets":
        aggs = data_dict.get("aggregations") or data_dict.get("facets") or {}
        rendered = render_output(aggs, ctx.out_format)
        write_or_print(rendered, output)
        return

    header_list = [h.strip() for h in headers.split(",") if h.strip()]
    hit_list = extract_hits_list(data_dict)

    rows: list[list[Any]] = []
    for hit in hit_list:
        if not isinstance(hit, dict):
            continue
        src = hit.get("_source", hit)
        flat = FlatDict(src, delimiter=".")
        rows.append([flat.get(h, "") for h in header_list])

    if output:
        write_csv(header_list, rows, output)
    else:
        print(tabulate(rows, headers=header_list))


@app.command("similar")
def search_similar(
    entry_id: str = typer.Option(..., "--entry-id", help="Search entry id (_id)"),
    limit: int = 10,
    mode: str = typer.Option("raw", "--mode", help="raw|results"),
    fields: str = typer.Option(
        "dataset.title,source.topics",
        "--fields",
        help="Comma-separated fields for more_like_this",
    ),
    headers: str = "id,dataset.title,source.name,source.uid",
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """
    GET /search/0.2/similar -> sdk.search_api.get_similar_datasets
    """
    ctx = build_context(format, debug)
    fields_list = [f.strip() for f in fields.split(",") if f.strip()] or None

    try:
        result = ctx.sdk.search_api.get_similar_datasets(
            entry_id=entry_id,
            limit=limit,
            fields=fields_list,
        )
    except Exception as e:
        print_sdk_error(e)
        return

    if mode == "raw":
        rendered = render_output(result, ctx.out_format)
        write_or_print(rendered, output)
        return

    data_dict = to_plain(result)
    if not isinstance(data_dict, dict):
        rendered = render_output(data_dict, ctx.out_format)
        write_or_print(rendered, output)
        return

    header_list = [h.strip() for h in headers.split(",") if h.strip()]
    hit_list = extract_hits_list(data_dict)

    rows: list[list[Any]] = []
    for hit in hit_list:
        if not isinstance(hit, dict):
            continue
        src = hit.get("_source", hit)
        flat = FlatDict(src, delimiter=".")
        rows.append([flat.get(h, "") for h in header_list])

    if output:
        write_csv(header_list, rows, output)
    else:
        print(tabulate(rows, headers=header_list))


@app.command("facets")
def search_facets_list(
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """
    List available search facets (SDK: list_search_facets).
    GET /search/0.2/list_facets
    """
    ctx = build_context(format, debug)
    run_and_render(ctx, ctx.sdk.search_api.list_search_facets, output)


@app.command("facet")
def search_facet_values(
    key: str = typer.Option(
        "source.catalog_type",
        "--key",
        help="Facet key from dateno search facets",
    ),
    format: str | None = None,
    output: str | None = None,
    debug: bool = False,
):
    """
    Get values for a single facet (SDK: get_search_facet_values).
    GET /search/0.2/get_facet
    """
    ctx = build_context(format, debug)
    run_and_render(
        ctx,
        lambda: ctx.sdk.search_api.get_search_facet_values(key=key),
        output,
    )
