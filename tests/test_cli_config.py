from pathlib import Path

from typer.testing import CliRunner

from dateno_cmd.cli import app


runner = CliRunner()


def test_config_init_creates_file():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["config", "init"])
        assert result.exit_code == 0
        assert Path(".dateno_cmd.yaml").exists()


def test_config_init_prompt_no_overwrite():
    with runner.isolated_filesystem():
        path = Path(".dateno_cmd.yaml")
        path.write_text("apikey: old", encoding="utf-8")
        result = runner.invoke(app, ["config", "init"], input="n\n")
        assert result.exit_code == 0
        assert path.read_text(encoding="utf-8") == "apikey: old"


def test_config_show_masks_apikey(monkeypatch):
    with runner.isolated_filesystem():
        monkeypatch.delenv("DATENO_APIKEY", raising=False)
        Path(".dateno_cmd.yaml").write_text(
            "apikey: abcd1234wxyz5678\n", encoding="utf-8"
        )
        result = runner.invoke(app, ["config", "show", "--format", "json"])
        assert result.exit_code == 0
        assert "abcd...5678" in result.output


def test_config_show_respects_overrides():
    with runner.isolated_filesystem():
        result = runner.invoke(
            app,
            ["--server-url", "https://override.example", "config", "show"],
        )
        assert result.exit_code == 0
        assert "https://override.example" in result.output
