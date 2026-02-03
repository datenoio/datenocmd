import json
import os

import pytest
from typer.testing import CliRunner

from dateno_cmd.cli import app


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


@pytest.mark.integration
def test_service_health():
    result = runner.invoke(
        app,
        ["service", "health", "--format", "json"],
        env=_runner_env(),
    )
    assert result.exit_code == 0
    assert json.loads(result.output)


@pytest.mark.integration
def test_search_query():
    result = runner.invoke(
        app,
        ["search", "query", "environment", "--limit", "1", "--mode", "raw", "--format", "json"],
        env=_runner_env(),
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert "hits" in payload


@pytest.mark.integration
def test_search_get():
    _require_env("DATENO_TEST_ENTRY_ID")
    result = runner.invoke(
        app,
        ["search", "get", os.getenv("DATENO_TEST_ENTRY_ID", ""), "--format", "json"],
        env=_runner_env(),
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload


@pytest.mark.integration
def test_raw_get():
    _require_env("DATENO_TEST_ENTRY_ID")
    result = runner.invoke(
        app,
        ["raw", "get", os.getenv("DATENO_TEST_ENTRY_ID", ""), "--format", "json"],
        env=_runner_env(),
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload


@pytest.mark.integration
def test_catalogs_get():
    _require_env("DATENO_TEST_CATALOG_ID")
    result = runner.invoke(
        app,
        ["catalogs", "get", os.getenv("DATENO_TEST_CATALOG_ID", ""), "--format", "json"],
        env=_runner_env(),
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload


@pytest.mark.integration
def test_stats_namespaces():
    result = runner.invoke(
        app,
        ["stats", "ns", "--limit", "1", "--format", "json"],
        env=_runner_env(),
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload is not None
