import httpx

from dateno_cmd.utils.errors import (
    EXIT_API,
    EXIT_INTERNAL,
    EXIT_NETWORK,
    EXIT_USER,
    UserInputError,
    print_sdk_error,
)


class DummyResponse:
    def __init__(self, status_code):
        self.status_code = status_code


class DummyApiError(Exception):
    def __init__(self, status_code):
        self.response = DummyResponse(status_code)
        self.body = {"detail": "not found"}
        self.message = "Not Found"


def test_print_sdk_error_http_4xx_is_user(capsys):
    code = print_sdk_error(DummyApiError(404))
    captured = capsys.readouterr()
    assert code == EXIT_USER
    assert "User error" in captured.err
    assert "Status: 404" in captured.err


def test_print_sdk_error_http_5xx_is_api(capsys):
    code = print_sdk_error(DummyApiError(503))
    captured = capsys.readouterr()
    assert code == EXIT_API
    assert "API error" in captured.err
    assert "Status: 503" in captured.err


def test_print_sdk_error_network(capsys):
    request = httpx.Request("GET", "https://example.com")
    err = httpx.ConnectError("boom", request=request)
    code = print_sdk_error(err)
    captured = capsys.readouterr()
    assert code == EXIT_NETWORK
    assert "Network error" in captured.err


def test_print_sdk_error_user(capsys):
    code = print_sdk_error(UserInputError("bad input"))
    captured = capsys.readouterr()
    assert code == EXIT_USER
    assert "User error" in captured.err


def test_print_sdk_error_internal(capsys):
    code = print_sdk_error(RuntimeError("oops"))
    captured = capsys.readouterr()
    assert code == EXIT_INTERNAL
    assert "Internal error" in captured.err
