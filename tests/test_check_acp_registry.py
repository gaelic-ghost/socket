from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "agent-portability-skills"
    / "skills"
    / "operate-acp-agent-integration"
    / "scripts"
    / "check_acp_registry.py"
)
SPEC = importlib.util.spec_from_file_location("check_acp_registry", MODULE_PATH)
assert SPEC and SPEC.loader
registry_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registry_check)


def test_find_agents_requires_exact_id_or_name() -> None:
    payload = {
        "agents": [
            {"id": "hermes-agent", "name": "Hermes Agent", "version": "0.18.2"}
        ]
    }

    assert registry_check.find_agents(payload, "hermes-agent") == payload["agents"]
    assert registry_check.find_agents(payload, "HERMES AGENT") == payload["agents"]
    assert registry_check.find_agents(payload, "hermes") == []


def test_load_registry_accepts_a_valid_registry_document(tmp_path: Path) -> None:
    registry_path = tmp_path / "registry.json"
    expected = {"version": "1.0.0", "agents": []}
    registry_path.write_text(json.dumps(expected), encoding="utf-8")

    assert registry_check.load_registry(registry_path.as_uri()) == expected


def test_main_reports_a_missing_agent_without_treating_it_as_an_error(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        registry_check,
        "load_registry",
        lambda _url: {"version": "1.0.0", "agents": []},
    )
    monkeypatch.setattr(sys, "argv", [str(MODULE_PATH), "hermes-agent"])

    assert registry_check.main() == 1
    assert "does not currently contain" in capsys.readouterr().out
