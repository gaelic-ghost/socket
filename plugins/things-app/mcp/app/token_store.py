from __future__ import annotations

import subprocess


SERVICE_NAME = "things-mcp"
ACCOUNT_NAME = "things-auth-token"


class TokenStoreError(RuntimeError):
    """Raised when keychain token operations fail."""


class TokenNotFoundError(TokenStoreError):
    """Raised when no token exists in keychain for this service/account."""


def set_token(token: str) -> None:
    try:
        subprocess.run(
            [
                "security",
                "add-generic-password",
                "-a",
                ACCOUNT_NAME,
                "-s",
                SERVICE_NAME,
                "-w",
                token,
                "-U",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or exc.stdout or str(exc)).strip()
        raise TokenStoreError(
            f"THINGS_AUTH_KEYCHAIN_WRITE_FAILED: Failed to save token to keychain: {message}"
        ) from exc


def get_token() -> str:
    try:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                ACCOUNT_NAME,
                "-s",
                SERVICE_NAME,
                "-w",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or exc.stdout or str(exc)).strip()
        lowered = message.lower()
        if "could not be found" in lowered or "item could not be found" in lowered:
            raise TokenNotFoundError("THINGS_AUTH_TOKEN_NOT_FOUND: No token stored in keychain") from exc
        raise TokenStoreError(
            f"THINGS_AUTH_KEYCHAIN_READ_FAILED: Failed to read token from keychain: {message}"
        ) from exc

    return result.stdout.strip()


def clear_token() -> None:
    try:
        subprocess.run(
            [
                "security",
                "delete-generic-password",
                "-a",
                ACCOUNT_NAME,
                "-s",
                SERVICE_NAME,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        message = (exc.stderr or exc.stdout or str(exc)).strip()
        lowered = message.lower()
        if "could not be found" in lowered or "item could not be found" in lowered:
            return
        raise TokenStoreError(
            f"THINGS_AUTH_KEYCHAIN_CLEAR_FAILED: Failed to clear token from keychain: {message}"
        ) from exc


def has_token() -> bool:
    try:
        token = get_token()
        return bool(token)
    except TokenNotFoundError:
        return False
