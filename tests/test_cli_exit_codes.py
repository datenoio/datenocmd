from types import SimpleNamespace

import httpx
from typer.testing import CliRunner

from dateno_cmd.cli import app
from dateno_cmd.commands import search as search_cmd
from dateno_cmd.commands import stats as stats_cmd
from dateno_cmd.utils.errors import EXIT_API, EXIT_NETWORK, EXIT_USER, UserInputError


runner = CliRunner()


def _ctx_with_sdk(sdk):
    settings = SimpleNamespace(debug=False)
    return SimpleNamespace(sdk=sdk, settings=settings, out_format="yaml")


def test_cli_exit_code_user_error(monkeypatch):
    class SearchAPI:
        def get_dataset_by_entry_id(self, entry_id):
            raise UserInputError("bad input")

    sdk = SimpleNamespace(search_api=SearchAPI())
    monkeypatch.setattr(search_cmd, "build_context", lambda *_a, **_k: _ctx_with_sdk(sdk))

    result = runner.invoke(app, ["search", "get", "id"])
    assert result.exit_code == EXIT_USER
    assert "User error" in result.output


def test_cli_exit_code_network_error(monkeypatch):
    class SearchAPI:
        def get_dataset_by_entry_id(self, entry_id):
            request = httpx.Request("GET", "https://example.com")
            raise httpx.ConnectError("boom", request=request)

    sdk = SimpleNamespace(search_api=SearchAPI())
    monkeypatch.setattr(search_cmd, "build_context", lambda *_a, **_k: _ctx_with_sdk(sdk))

    result = runner.invoke(app, ["search", "get", "id"])
    assert result.exit_code == EXIT_NETWORK
    assert "Network error" in result.output


def test_cli_exit_code_api_error(monkeypatch, tmp_path):
    class DummyResponse:
        status_code = 503

    class DummyApiError(Exception):
        def __init__(self):
            self.response = DummyResponse()
            self.body = {"detail": "fail"}
            self.message = "Service Unavailable"

    class StatsAPI:
        def export_timeseries_file(self, **_kwargs):
            raise DummyApiError()

    sdk = SimpleNamespace(statistics_api=StatsAPI())
    monkeypatch.setattr(stats_cmd, "build_context", lambda *_a, **_k: _ctx_with_sdk(sdk))

    out = tmp_path / "export.csv"
    result = runner.invoke(
        app,
        ["stats", "export", "ilostat", "CCF_XOXR_CUR_RT.ABW", "--format", "csv", "-o", str(out)],
    )
    assert result.exit_code == EXIT_API
    assert "API error" in result.output
