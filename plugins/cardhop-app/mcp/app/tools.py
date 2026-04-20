from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Sequence
from typing import Annotated, Literal
from urllib.parse import quote

from pydantic import BaseModel, ConfigDict, Field

Transport = Literal["auto", "applescript", "url_scheme"]
ResolvedTransport = Literal["applescript", "url_scheme"]
ErrorCode = Literal[
    "CARDHOP_NOT_FOUND",
    "AUTOMATION_DENIED",
    "INVALID_INPUT",
    "LAUNCH_FAILED",
    "EXEC_FAILED",
]

MAX_SENTENCE_LENGTH = 2000
CARDHOP_APP_PATHS = (
    "/Applications/Cardhop.app",
    os.path.expanduser("~/Applications/Cardhop.app"),
)


class DispatchResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool
    dispatched: bool
    command_preview: str
    dry_run: bool
    error_code: ErrorCode | None = None
    error_message: str | None = None
    transport_used: ResolvedTransport | None = None


class HealthcheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: bool
    cardhop_installed: bool
    applescript_available: bool
    url_scheme_available: bool
    notes: list[str]


CARDHOP_SCHEMA_BUNDLE: dict[str, object] = {
    "$id": "cardhop.mcp.tools.v1",
    "version": "1.0.0",
    "constraints": {
        "documented_macos_routes_only": True,
        "allowed_transports": ["applescript.parse_sentence", "url_scheme.parse"],
    },
    "tools": ["cardhop_parse", "cardhop_add", "cardhop_update", "cardhop_healthcheck"],
}


def _is_cardhop_installed() -> bool:
    return any(os.path.isdir(path) for path in CARDHOP_APP_PATHS)


def _which(command: str) -> bool:
    return shutil.which(command) is not None


def _escape_applescript(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _applescript_preview(sentence: str, add_immediately: bool) -> str:
    escaped_sentence = _escape_applescript(sentence)
    tail = " with add immediately" if add_immediately else ""
    return f'tell application "Cardhop" to parse sentence "{escaped_sentence}"{tail}'


def _url_preview(sentence: str) -> str:
    return f"x-cardhop://parse?s={quote(sentence, safe='')}"


def _run(cmd: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=False, capture_output=True, text=True)


def _validate_sentence(raw_sentence: str) -> str:
    sentence = raw_sentence.strip()
    if not sentence:
        raise ValueError("sentence must not be empty")
    if len(sentence) > MAX_SENTENCE_LENGTH:
        raise ValueError(f"sentence must be <= {MAX_SENTENCE_LENGTH} characters")
    return sentence


def _resolve_transport(
    requested: Transport,
) -> tuple[ResolvedTransport | None, DispatchResult | None]:
    if not _is_cardhop_installed():
        return None, DispatchResult(
            ok=False,
            dispatched=False,
            dry_run=False,
            command_preview="",
            error_code="CARDHOP_NOT_FOUND",
            error_message="Cardhop.app not found in /Applications or ~/Applications.",
        )

    has_osascript = _which("osascript")
    has_open = _which("open")

    if requested == "applescript":
        if not has_osascript:
            return None, DispatchResult(
                ok=False,
                dispatched=False,
                dry_run=False,
                command_preview="",
                error_code="EXEC_FAILED",
                error_message="osascript is not available on PATH.",
            )
        return "applescript", None

    if requested == "url_scheme":
        if not has_open:
            return None, DispatchResult(
                ok=False,
                dispatched=False,
                dry_run=False,
                command_preview="",
                error_code="EXEC_FAILED",
                error_message="open is not available on PATH.",
            )
        return "url_scheme", None

    if has_osascript:
        return "applescript", None
    if has_open:
        return "url_scheme", None
    return None, DispatchResult(
        ok=False,
        dispatched=False,
        dry_run=False,
        command_preview="",
        error_code="EXEC_FAILED",
        error_message="Neither osascript nor open is available on PATH.",
    )


def _dispatch_applescript(sentence: str, add_immediately: bool, dry_run: bool) -> DispatchResult:
    preview = _applescript_preview(sentence, add_immediately)
    if dry_run:
        return DispatchResult(
            ok=True,
            dispatched=False,
            dry_run=True,
            command_preview=preview,
            transport_used="applescript",
        )

    completed = _run(["osascript", "-e", preview])
    if completed.returncode == 0:
        return DispatchResult(
            ok=True,
            dispatched=True,
            dry_run=False,
            command_preview=preview,
            transport_used="applescript",
        )

    stderr = (completed.stderr or "").strip()
    denied_hint = "not authorized" in stderr.lower() or "not permitted" in stderr.lower()
    return DispatchResult(
        ok=False,
        dispatched=False,
        dry_run=False,
        command_preview=preview,
        transport_used="applescript",
        error_code="AUTOMATION_DENIED" if denied_hint else "EXEC_FAILED",
        error_message=stderr or "osascript execution failed.",
    )


def _dispatch_url_scheme(sentence: str, dry_run: bool) -> DispatchResult:
    url = _url_preview(sentence)
    if dry_run:
        return DispatchResult(
            ok=True,
            dispatched=False,
            dry_run=True,
            command_preview=url,
            transport_used="url_scheme",
        )

    completed = _run(["open", url])
    if completed.returncode == 0:
        return DispatchResult(
            ok=True,
            dispatched=True,
            dry_run=False,
            command_preview=url,
            transport_used="url_scheme",
        )

    stderr = (completed.stderr or "").strip()
    return DispatchResult(
        ok=False,
        dispatched=False,
        dry_run=False,
        command_preview=url,
        transport_used="url_scheme",
        error_code="LAUNCH_FAILED",
        error_message=stderr or "open command failed for Cardhop URL scheme.",
    )


def cardhop_parse(
    sentence: Annotated[str, Field(min_length=1, max_length=MAX_SENTENCE_LENGTH)],
    transport: Transport = "auto",
    add_immediately: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    """Send a natural-language sentence to Cardhop via documented macOS parse routes.

    Uses only:
    - AppleScript: tell application "Cardhop" to parse sentence "..."
    - URL scheme: x-cardhop://parse?s=...
    """
    try:
        clean_sentence = _validate_sentence(sentence)
    except ValueError as exc:
        return DispatchResult(
            ok=False,
            dispatched=False,
            dry_run=dry_run,
            command_preview="",
            error_code="INVALID_INPUT",
            error_message=str(exc),
        ).model_dump()

    resolved_transport, error = _resolve_transport(transport)
    if error is not None:
        error.dry_run = dry_run
        return error.model_dump()

    assert resolved_transport is not None
    if resolved_transport == "applescript":
        return _dispatch_applescript(
            clean_sentence,
            add_immediately=add_immediately,
            dry_run=dry_run,
        ).model_dump()
    return _dispatch_url_scheme(clean_sentence, dry_run=dry_run).model_dump()


def cardhop_add(
    sentence: Annotated[str, Field(min_length=1, max_length=MAX_SENTENCE_LENGTH)],
    transport: Transport = "auto",
    dry_run: bool = False,
) -> dict[str, object]:
    """Convenience wrapper for add/create flows using Cardhop parse.

    This always maps to parse with add_immediately=true.
    """
    return cardhop_parse(
        sentence=sentence,
        transport=transport,
        add_immediately=True,
        dry_run=dry_run,
    )


def cardhop_update(
    instruction: Annotated[str, Field(min_length=1, max_length=MAX_SENTENCE_LENGTH)],
    transport: Transport = "auto",
    add_immediately: bool = False,
    dry_run: bool = False,
) -> dict[str, object]:
    """Freeform update/edit command over Cardhop parse.

    Guidance for LLMs:
    - Use natural language updates in the form '<existing name> <changed fields>'.
    - Example: 'Jane Doe new email jane@acme.com mobile 555-123-4567'.
    - Do not rely on undocumented Cardhop routes or identifiers.
    """
    return cardhop_parse(
        sentence=instruction,
        transport=transport,
        add_immediately=add_immediately,
        dry_run=dry_run,
    )


def cardhop_healthcheck() -> dict[str, object]:
    """Check Cardhop and local transport readiness for macOS."""
    cardhop_installed = _is_cardhop_installed()
    applescript_available = _which("osascript")
    url_scheme_available = _which("open")

    notes = []
    if not cardhop_installed:
        notes.append("Install Cardhop.app in /Applications or ~/Applications.")
    if applescript_available:
        notes.append(
            "AppleScript transport available; first run may prompt for Automation permission."
        )
    if url_scheme_available:
        notes.append("URL scheme transport available via open x-cardhop://parse.")
    if not applescript_available and not url_scheme_available:
        notes.append("No supported transport command available on PATH.")

    payload = HealthcheckResult(
        ok=cardhop_installed and (applescript_available or url_scheme_available),
        cardhop_installed=cardhop_installed,
        applescript_available=applescript_available,
        url_scheme_available=url_scheme_available,
        notes=notes,
    )
    return payload.model_dump()
