from __future__ import annotations

from urllib.request import urlopen

import pytest

from app.things_client import CallbackResult, CallbackServer, ThingsClientError, ThingsUrlClient


class FakeCallbackServer:
    def __init__(self, result: CallbackResult) -> None:
        self.result = result
        self.success_url = "http://127.0.0.1:4000/success"
        self.error_url = "http://127.0.0.1:4000/error"

    def __enter__(self) -> "FakeCallbackServer":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def wait(self) -> CallbackResult:
        return self.result


def test_build_url_encodes_params() -> None:
    client = ThingsUrlClient(opener=lambda _: None)

    url = client.build_url("add", {"title": "Ship release", "tags": ["a", "b"], "reveal": True})

    assert url.startswith("things:///add?")
    assert "title=Ship+release" in url
    assert "tags=a%0Ab" in url
    assert "reveal=true" in url


def test_execute_with_callback_returns_callback_params() -> None:
    opened: list[str] = []

    client = ThingsUrlClient(
        opener=lambda url: opened.append(url),
        callback_server_factory=lambda: FakeCallbackServer(
            CallbackResult(status="success", params={"version": "3.21.8", "build": "1234"})
        ),
    )

    response = client.execute("version", capture_callback=True)

    assert response["ok"] is True
    assert response["callback"]["version"] == "3.21.8"
    assert opened and "x-success=" in opened[0]


def test_execute_raises_on_error_callback() -> None:
    client = ThingsUrlClient(
        opener=lambda _: None,
        callback_server_factory=lambda: FakeCallbackServer(
            CallbackResult(status="error", params={"errorMessage": "bad command"})
        ),
    )

    with pytest.raises(ThingsClientError, match="bad command"):
        client.execute("version", capture_callback=True)


def test_execute_dry_run_skips_open(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("THINGS_MCP_DRY_RUN", "1")
    opened: list[str] = []
    client = ThingsUrlClient(opener=lambda url: opened.append(url))

    response = client.execute("add", {"title": "Dry run"})

    assert response["ok"] is True
    assert response["dry_run"] is True
    assert opened == []


def test_execute_dry_run_rejects_callback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("THINGS_MCP_DRY_RUN", "true")
    client = ThingsUrlClient(opener=lambda _: None)

    with pytest.raises(ThingsClientError, match="not supported"):
        client.execute("version", capture_callback=True)


def test_execute_redacts_auth_token_in_returned_url() -> None:
    client = ThingsUrlClient(opener=lambda _: None)

    response = client.execute("update", {"id": "abc", "auth-token": "secret-token", "title": "X"})

    assert response["ok"] is True
    assert response["url"].startswith("things:///update?")
    assert "auth-token=%2A%2A%2AREDACTED%2A%2A%2A" in response["url"]
    assert "secret-token" not in response["url"]


def test_callback_server_parses_success_query_params() -> None:
    with CallbackServer(timeout_seconds=1.0) as callback_server:
        with urlopen(f"{callback_server.success_url}?version=3.21.8&build=1234") as response:
            assert response.status == 200

        result = callback_server.wait()

    assert result.status == "success"
    assert result.params == {"version": "3.21.8", "build": "1234"}


def test_callback_server_parses_error_query_params() -> None:
    with CallbackServer(timeout_seconds=1.0) as callback_server:
        with urlopen(f"{callback_server.error_url}?errorMessage=bad+command") as response:
            assert response.status == 200

        result = callback_server.wait()

    assert result.status == "error"
    assert result.params == {"errorMessage": "bad command"}
