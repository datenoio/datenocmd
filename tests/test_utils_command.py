from types import SimpleNamespace

import pytest
import typer

from dateno_cmd.utils import command as cmd


def test_run_and_render_success(monkeypatch):
    ctx = SimpleNamespace(out_format="yaml")
    calls = {"rendered": None}

    monkeypatch.setattr(cmd, "render_output", lambda data, fmt: f"{fmt}:{data}")
    monkeypatch.setattr(cmd, "write_or_print", lambda rendered, output: calls.update({"rendered": rendered}))

    result = cmd.run_and_render(ctx, lambda: {"a": 1}, None)
    assert result == {"a": 1}
    assert calls["rendered"] == "yaml:{'a': 1}"


def test_run_and_render_error(monkeypatch):
    ctx = SimpleNamespace(out_format="yaml")
    calls = {"error": False}

    def boom():
        raise RuntimeError("bad")

    monkeypatch.setattr(
        cmd, "print_sdk_error", lambda e, debug=False: calls.update({"error": True}) or 4
    )

    with pytest.raises(typer.Exit) as exc:
        cmd.run_and_render(ctx, boom, None)
    assert exc.value.exit_code == 4
    assert calls["error"] is True


def test_run_and_render_with_mode_raw(monkeypatch):
    ctx = SimpleNamespace(out_format="yaml")
    calls = {"rendered": None}

    monkeypatch.setattr(cmd, "render_output", lambda data, fmt: f"{fmt}:{data}")
    monkeypatch.setattr(cmd, "write_or_print", lambda rendered, output: calls.update({"rendered": rendered}))

    result = cmd.run_and_render_with_mode(ctx, lambda: {"a": 1}, "raw", None)
    assert result is None
    assert calls["rendered"] == "yaml:{'a': 1}"


def test_run_and_render_with_mode_dict():
    ctx = SimpleNamespace(out_format="yaml")
    result = cmd.run_and_render_with_mode(ctx, lambda: {"a": 1}, "results", None)
    assert result == {"a": 1}
