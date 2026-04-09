from __future__ import annotations

import os
import subprocess
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable
from urllib.parse import parse_qs, parse_qsl, urlencode, urlparse


THINGS_URL_PREFIX = "things:///"


class ThingsClientError(RuntimeError):
    """Raised when a Things URL command cannot be executed successfully."""


class ThingsValidationError(ValueError):
    """Raised when invalid command parameters are supplied."""


@dataclass
class CallbackResult:
    status: str
    params: dict[str, str]


class CallbackServer:
    def __init__(self, timeout_seconds: float = 5.0) -> None:
        self._timeout_seconds = timeout_seconds
        self._result: CallbackResult | None = None
        self._event = threading.Event()
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    @property
    def success_url(self) -> str:
        if self._server is None:
            raise RuntimeError("callback server has not started")
        return f"http://127.0.0.1:{self._server.server_port}/success"

    @property
    def error_url(self) -> str:
        if self._server is None:
            raise RuntimeError("callback server has not started")
        return f"http://127.0.0.1:{self._server.server_port}/error"

    def __enter__(self) -> "CallbackServer":
        parent = self

        class _Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:  # noqa: A003
                return

            def do_GET(self) -> None:  # noqa: N802
                parsed = urlparse(self.path)
                path = parsed.path.strip("/")
                query = parse_qs(parsed.query, keep_blank_values=True)
                params = {k: v[-1] if v else "" for k, v in query.items()}
                status = "error" if path == "error" else "success"
                parent._result = CallbackResult(status=status, params=params)
                parent._event.set()

                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"ok")

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self

    def wait(self) -> CallbackResult:
        if not self._event.wait(timeout=self._timeout_seconds):
            raise ThingsClientError(
                f"Timed out waiting {self._timeout_seconds}s for Things callback"
            )
        if self._result is None:
            raise ThingsClientError("Callback did not provide a result")
        return self._result

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
        if self._thread is not None:
            self._thread.join(timeout=1.0)


def _default_url_opener(url: str) -> None:
    subprocess.run(["open", url], check=True)


class ThingsUrlClient:
    def __init__(
        self,
        opener: Callable[[str], None] | None = None,
        callback_server_factory: Callable[[], CallbackServer] | None = None,
    ) -> None:
        self._opener = opener or _default_url_opener
        self._callback_server_factory = callback_server_factory or CallbackServer

    def build_url(self, command: str, params: dict[str, Any]) -> str:
        normalized = {
            key: self._normalize_value(value)
            for key, value in params.items()
            if value is not None
        }
        query = urlencode(normalized, doseq=False)
        return f"{THINGS_URL_PREFIX}{command}" + (f"?{query}" if query else "")

    def execute(
        self,
        command: str,
        params: dict[str, Any] | None = None,
        *,
        capture_callback: bool = False,
    ) -> dict[str, Any]:
        params = dict(params or {})
        dry_run = _is_truthy(os.getenv("THINGS_MCP_DRY_RUN"))

        if capture_callback:
            if dry_run:
                raise ThingsClientError("capture_callback is not supported when THINGS_MCP_DRY_RUN is enabled")
            with self._callback_server_factory() as callback_server:
                params["x-success"] = callback_server.success_url
                params["x-error"] = callback_server.error_url
                url = self.build_url(command, params)
                self._opener(url)
                callback_result = callback_server.wait()
                if callback_result.status == "error":
                    raise ThingsClientError(
                        callback_result.params.get("errorMessage", "Things returned an error")
                    )
                return {
                    "ok": True,
                    "command": command,
                    "url": _redact_sensitive_query_params(url),
                    "callback": callback_result.params,
                }

        url = self.build_url(command, params)
        if not dry_run:
            self._opener(url)
        return {
            "ok": True,
            "command": command,
            "url": _redact_sensitive_query_params(url),
            "dry_run": dry_run,
        }

    @staticmethod
    def _normalize_value(value: Any) -> str:
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (list, tuple)):
            return "\n".join(str(v) for v in value)
        return str(value)


def require_non_empty(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise ThingsValidationError(f"'{field_name}' is required")
    return value.strip()


def ensure_update_payload_has_changes(payload: dict[str, Any], *, ignored_keys: set[str]) -> None:
    for key, value in payload.items():
        if key in ignored_keys:
            continue
        if value is not None:
            return
    raise ThingsValidationError("At least one field must be provided to update")


def _is_truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _redact_sensitive_query_params(url: str) -> str:
    if "?" not in url:
        return url
    base, raw_query = url.split("?", 1)
    query_params = parse_qsl(raw_query, keep_blank_values=True)
    redacted_params: list[tuple[str, str]] = []
    for key, value in query_params:
        if key.lower() == "auth-token":
            redacted_params.append((key, "***REDACTED***"))
        else:
            redacted_params.append((key, value))
    redacted_query = urlencode(redacted_params, doseq=True)
    return f"{base}?{redacted_query}"
