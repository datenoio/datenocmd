import json

import pytest
import typer

from dateno_cmd.utils.io import load_json_arg, write_csv, write_or_print


def test_write_or_print_stdout(capsys):
    write_or_print("hello", None)
    captured = capsys.readouterr()
    assert "hello" in captured.out


def test_write_or_print_file(tmp_path):
    out = tmp_path / "out.txt"
    write_or_print("data", str(out))
    assert out.read_text(encoding="utf-8") == "data"


def test_write_csv(tmp_path):
    out = tmp_path / "out.csv"
    write_csv(["a", "b"], [[1, 2]], str(out))
    content = out.read_text(encoding="utf-8").splitlines()
    assert content[0] == "a,b"
    assert content[1] == "1,2"


def test_load_json_arg_inline():
    value = load_json_arg('{"a": 1}')
    assert value == {"a": 1}


def test_load_json_arg_file(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"x": 2}), encoding="utf-8")
    value = load_json_arg(f"@{p}")
    assert value == {"x": 2}


def test_load_json_arg_invalid():
    with pytest.raises(typer.BadParameter):
        load_json_arg("{bad json")
