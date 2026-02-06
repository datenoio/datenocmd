from dateno_cmd.utils.serialization import render_output, to_plain


class DummyModelDump:
    def model_dump(self, mode="python", exclude_none=True):
        payload = {"a": 1, "b": None}
        if exclude_none:
            return {"a": 1}
        return payload


class DummyDict:
    def dict(self, exclude_none=True):
        return {"x": 2}


def test_to_plain_model_dump():
    assert to_plain(DummyModelDump()) == {"a": 1}


def test_to_plain_dict_fallback():
    assert to_plain(DummyDict()) == {"x": 2}


def test_to_plain_nested_list():
    assert to_plain([{"k": 1}, 2]) == [{"k": 1}, 2]


def test_render_output_json():
    rendered = render_output({"a": 1}, "json")
    assert '"a": 1' in rendered


def test_render_output_yaml():
    rendered = render_output({"a": 1}, "yaml")
    assert "a: 1" in rendered
