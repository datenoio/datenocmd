import json
import os

import pytest
from typer.testing import CliRunner

from dateno.sdk import SDK

from dateno_cmd.cli import app
from dateno_cmd.utils.search import extract_hits_list
from dateno_cmd.utils.serialization import to_plain


runner = CliRunner()


def _require_env(*names: str) -> None:
    missing = [name for name in names if not os.getenv(name)]
    if missing:
        pytest.skip(f"Missing env vars: {', '.join(missing)}")


def _runner_env() -> dict[str, str]:
    _require_env("DATENO_APIKEY")
    env = {"DATENO_APIKEY": os.getenv("DATENO_APIKEY", "")}
    if os.getenv("DATENO_SERVER_URL"):
        env["DATENO_SERVER_URL"] = os.getenv("DATENO_SERVER_URL", "")
    return env


def _sdk() -> SDK:
    _require_env("DATENO_APIKEY")
    return SDK(
        api_key_query=os.getenv("DATENO_APIKEY", ""),
        server_url=os.getenv("DATENO_SERVER_URL", "https://api.dateno.io"),
    )


@pytest.mark.contract
def test_contract_search_query_hits_match():
    query = os.getenv("DATENO_TEST_QUERY", "environment")
    sdk = _sdk()

    sdk_result = sdk.search_api.search_datasets(q=query, limit=1)
    sdk_payload = to_plain(sdk_result)

    cli_result = runner.invoke(
        app,
        ["search", "query", query, "--limit", "1", "--mode", "raw", "--format", "json"],
        env=_runner_env(),
    )
    assert cli_result.exit_code == 0
    cli_payload = json.loads(cli_result.output)

    sdk_hits = extract_hits_list(sdk_payload)
    cli_hits = extract_hits_list(cli_payload)
    assert len(sdk_hits) == len(cli_hits)


@pytest.mark.contract
def test_contract_catalogs_get_id_match():
    _require_env("DATENO_TEST_CATALOG_ID")
    catalog_id = os.getenv("DATENO_TEST_CATALOG_ID", "")

    sdk = _sdk()
    sdk_result = sdk.data_catalogs_api.get_catalog_by_id(catalog_id=catalog_id)
    sdk_payload = to_plain(sdk_result)

    cli_result = runner.invoke(
        app,
        ["catalogs", "get", catalog_id, "--format", "json"],
        env=_runner_env(),
    )
    assert cli_result.exit_code == 0
    cli_payload = json.loads(cli_result.output)

    sdk_id = sdk_payload.get("id") or sdk_payload.get("_id")
    cli_id = cli_payload.get("id") or cli_payload.get("_id")
    assert sdk_id == cli_id
