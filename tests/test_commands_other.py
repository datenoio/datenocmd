from types import SimpleNamespace

from dateno_cmd.commands import catalogs as catalogs_cmd
from dateno_cmd.commands import raw as raw_cmd
from dateno_cmd.commands import service as service_cmd
from dateno_cmd.commands import stats as stats_cmd


def _ctx_with_sdk(sdk):
    return SimpleNamespace(sdk=sdk, out_format="yaml")


def test_raw_get_calls_run_and_render(monkeypatch):
    called = {"ok": False}

    monkeypatch.setattr(raw_cmd, "build_context", lambda *_args, **_kwargs: _ctx_with_sdk(object()))
    monkeypatch.setattr(raw_cmd, "run_and_render", lambda *_args, **_kwargs: called.update({"ok": True}))

    raw_cmd.raw_get("id")
    assert called["ok"] is True


def test_catalogs_get_calls_run_and_render(monkeypatch):
    called = {"ok": False}

    monkeypatch.setattr(catalogs_cmd, "build_context", lambda *_args, **_kwargs: _ctx_with_sdk(object()))
    monkeypatch.setattr(catalogs_cmd, "run_and_render", lambda *_args, **_kwargs: called.update({"ok": True}))

    catalogs_cmd.catalogs_get("cdi00001616")
    assert called["ok"] is True


def test_service_health_calls_run_and_render(monkeypatch):
    called = {"ok": False}

    sdk = SimpleNamespace(service=SimpleNamespace(get_healthz=lambda: {"ok": True}))
    monkeypatch.setattr(service_cmd, "build_context", lambda *_args, **_kwargs: _ctx_with_sdk(sdk))
    monkeypatch.setattr(service_cmd, "run_and_render", lambda *_args, **_kwargs: called.update({"ok": True}))

    service_cmd.service_health()
    assert called["ok"] is True


def test_stats_export_writes_file(tmp_path, monkeypatch):
    class DummyResult:
        def __init__(self):
            self.content = b"data"
            self.read_called = False

        def read(self):
            self.read_called = True

    class DummyResp:
        def __init__(self):
            self.result = DummyResult()

    stats_api = SimpleNamespace(export_timeseries_file=lambda **_kwargs: DummyResp())
    sdk = SimpleNamespace(statistics_api=stats_api)
    monkeypatch.setattr(stats_cmd, "build_context", lambda *_args, **_kwargs: _ctx_with_sdk(sdk))

    out = tmp_path / "export.csv"
    stats_cmd.stats_export_timeseries(
        "ilostat",
        "CCF_XOXR_CUR_RT.ABW",
        fileext="csv",
        output=str(out),
    )
    assert out.read_bytes() == b"data"
