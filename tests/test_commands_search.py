from types import SimpleNamespace

from dateno_cmd.commands import search as search_cmd


def _make_ctx(result):
    sdk = SimpleNamespace(
        search_api=SimpleNamespace(
            search_datasets=lambda **_kwargs: result,
            search_datasets_dsl=lambda **_kwargs: result,
            get_similar_datasets=lambda **_kwargs: result,
            get_dataset_by_entry_id=lambda **_kwargs: result,
        )
    )
    return SimpleNamespace(sdk=sdk, out_format="yaml")


def test_search_query_results_writes_csv(tmp_path, monkeypatch):
    result = {"hits": {"hits": [{"_source": {"id": "1"}}]}}
    ctx = _make_ctx(result)
    monkeypatch.setattr(search_cmd, "build_context", lambda *_args, **_kwargs: ctx)

    out = tmp_path / "out.csv"
    search_cmd.search_query(
        query="env",
        mode="results",
        headers="id",
        output=str(out),
    )
    content = out.read_text(encoding="utf-8").splitlines()
    assert content[0] == "id"
    assert content[1] == "1"


def test_search_query_totals_prints_value(capsys, monkeypatch):
    result = {"hits": {"total": {"value": 5}}}
    ctx = _make_ctx(result)
    monkeypatch.setattr(search_cmd, "build_context", lambda *_args, **_kwargs: ctx)

    search_cmd.search_query(query="env", mode="totals")
    captured = capsys.readouterr()
    assert "5" in captured.out


def test_search_dsl_raw_output(capsys, monkeypatch):
    result = {"ok": True}
    ctx = _make_ctx(result)
    monkeypatch.setattr(search_cmd, "build_context", lambda *_args, **_kwargs: ctx)

    search_cmd.search_dsl(body='{"query":{"match_all":{}}}', mode="raw")
    captured = capsys.readouterr()
    assert "ok" in captured.out


def test_search_similar_results_writes_csv(tmp_path, monkeypatch):
    result = {"hits": {"hits": [{"_source": {"id": "x"}}]}}
    ctx = _make_ctx(result)
    monkeypatch.setattr(search_cmd, "build_context", lambda *_args, **_kwargs: ctx)

    out = tmp_path / "out.csv"
    search_cmd.search_similar(
        entry_id="id",
        mode="results",
        fields="dataset.title",
        headers="id",
        output=str(out),
    )
    content = out.read_text(encoding="utf-8").splitlines()
    assert content[0] == "id"
    assert content[1] == "x"
