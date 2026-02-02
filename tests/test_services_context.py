import click

from dateno_cmd.services import context as ctx_mod


class DummySettings:
    def __init__(self, output_format="json", debug=False):
        self.output_format = output_format
        self.debug = debug

    def load_user_yaml_if_needed(self):
        return self


def test_build_context_uses_settings_and_sdk(monkeypatch):
    settings = DummySettings(output_format="json")
    sdk = object()

    monkeypatch.setattr(ctx_mod, "get_settings", lambda: settings)
    monkeypatch.setattr(ctx_mod, "get_sdk", lambda _s: sdk)
    monkeypatch.setattr(ctx_mod, "configure_logging", lambda *_args, **_kwargs: None)

    ctx = ctx_mod.build_context(None, False)
    assert ctx.out_format == "json"
    assert ctx.sdk is sdk


def test_build_context_respects_global_debug(monkeypatch):
    settings = DummySettings(output_format="yaml")
    sdk = object()
    calls = {}

    monkeypatch.setattr(ctx_mod, "get_settings", lambda: settings)
    monkeypatch.setattr(ctx_mod, "get_sdk", lambda _s: sdk)
    monkeypatch.setattr(ctx_mod, "configure_logging", lambda debug, _sd: calls.setdefault("debug", debug))

    class DummyCtx:
        obj = {"debug": True}

    monkeypatch.setattr(click, "get_current_context", lambda silent=True: DummyCtx())

    ctx = ctx_mod.build_context(None, False)
    assert ctx.out_format == "yaml"
    assert calls.get("debug") is True
