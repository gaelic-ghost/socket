from __future__ import annotations

import subprocess

import pytest

from app.token_store import (
    TokenNotFoundError,
    TokenStoreError,
    clear_token,
    get_token,
    has_token,
    set_token,
)


def _called_process_error(stderr: str) -> subprocess.CalledProcessError:
    return subprocess.CalledProcessError(1, ["security"], stderr=stderr)


def test_get_token_not_found_raises_specific_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail(*args, **kwargs):
        raise _called_process_error("The specified item could not be found in the keychain.")

    monkeypatch.setattr("subprocess.run", _fail)

    with pytest.raises(TokenNotFoundError, match="THINGS_AUTH_TOKEN_NOT_FOUND"):
        get_token()


def test_get_token_other_read_error_has_code(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail(*args, **kwargs):
        raise _called_process_error("User interaction is not allowed.")

    monkeypatch.setattr("subprocess.run", _fail)

    with pytest.raises(TokenStoreError, match="THINGS_AUTH_KEYCHAIN_READ_FAILED"):
        get_token()


def test_set_token_error_has_code(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail(*args, **kwargs):
        raise _called_process_error("Permission denied")

    monkeypatch.setattr("subprocess.run", _fail)

    with pytest.raises(TokenStoreError, match="THINGS_AUTH_KEYCHAIN_WRITE_FAILED"):
        set_token("abc")


def test_clear_token_not_found_is_noop(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fail(*args, **kwargs):
        raise _called_process_error("The specified item could not be found in the keychain.")

    monkeypatch.setattr("subprocess.run", _fail)

    clear_token()


def test_has_token_false_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_not_found() -> str:
        raise TokenNotFoundError("x")

    monkeypatch.setattr("app.token_store.get_token", _raise_not_found)

    assert has_token() is False
