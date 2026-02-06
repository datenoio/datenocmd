from dateno_cmd.utils.sdk import call_sdk_flexible


def test_call_sdk_flexible_body_to_request():
    def fn(request):
        return request

    assert call_sdk_flexible(fn, body={"a": 1}) == {"a": 1}


def test_call_sdk_flexible_entry_id_to_id():
    def fn(id):
        return id

    assert call_sdk_flexible(fn, entry_id="123") == "123"
