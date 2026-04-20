import subprocess

from app import tools


def test_cardhop_parse_invalid_input() -> None:
    payload = tools.cardhop_parse(sentence="   ", dry_run=True)
    assert payload["ok"] is False
    assert payload["error_code"] == "INVALID_INPUT"


def test_cardhop_parse_applescript_dry_run(monkeypatch) -> None:
    monkeypatch.setattr(tools, "_is_cardhop_installed", lambda: True)
    monkeypatch.setattr(tools, "_which", lambda command: command == "osascript")

    payload = tools.cardhop_parse(
        sentence='Jane Doe email "jane@example.com"',
        transport="applescript",
        add_immediately=True,
        dry_run=True,
    )
    assert payload["ok"] is True
    assert payload["dispatched"] is False
    assert payload["transport_used"] == "applescript"
    command_preview = payload["command_preview"]
    assert isinstance(command_preview, str)
    assert "with add immediately" in command_preview


def test_cardhop_parse_url_scheme_dispatch(monkeypatch) -> None:
    monkeypatch.setattr(tools, "_is_cardhop_installed", lambda: True)
    monkeypatch.setattr(tools, "_which", lambda command: command == "open")
    monkeypatch.setattr(
        tools,
        "_run",
        lambda cmd: subprocess.CompletedProcess(cmd, 0, stdout="", stderr=""),
    )

    payload = tools.cardhop_parse(
        sentence="Jane Doe new email jane@example.com",
        transport="url_scheme",
        dry_run=False,
    )
    assert payload["ok"] is True
    assert payload["dispatched"] is True
    assert payload["transport_used"] == "url_scheme"
    command_preview = payload["command_preview"]
    assert isinstance(command_preview, str)
    assert command_preview.startswith("x-cardhop://parse?s=")


def test_cardhop_update_forwards_to_parse(monkeypatch) -> None:
    captured: dict[str, object] = {}

    def fake_parse(
        sentence: str,
        transport: tools.Transport = "auto",
        add_immediately: bool = False,
        dry_run: bool = False,
    ) -> dict[str, object]:
        captured["sentence"] = sentence
        captured["transport"] = transport
        captured["add_immediately"] = add_immediately
        captured["dry_run"] = dry_run
        return {
            "ok": True,
            "dispatched": False,
            "command_preview": "preview",
            "dry_run": True,
            "error_code": None,
            "error_message": None,
            "transport_used": "applescript",
        }

    monkeypatch.setattr(tools, "cardhop_parse", fake_parse)
    payload = tools.cardhop_update(
        instruction="Jane Doe new mobile 555-111-2222",
        transport="auto",
        add_immediately=False,
        dry_run=True,
    )

    assert payload["ok"] is True
    assert captured["sentence"] == "Jane Doe new mobile 555-111-2222"
    assert captured["transport"] == "auto"
    assert captured["add_immediately"] is False
    assert captured["dry_run"] is True


def test_cardhop_healthcheck(monkeypatch) -> None:
    monkeypatch.setattr(tools, "_is_cardhop_installed", lambda: True)
    monkeypatch.setattr(tools, "_which", lambda _command: True)

    payload = tools.cardhop_healthcheck()
    assert payload["ok"] is True
    assert payload["cardhop_installed"] is True
    assert payload["applescript_available"] is True
    assert payload["url_scheme_available"] is True
