from types import SimpleNamespace

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

    monkeypatch.setattr(cmd, "print_sdk_error", lambda e: calls.update({"error": True}))

    result = cmd.run_and_render(ctx, boom, None)
    assert result is None
    assert calls["error"] is True
