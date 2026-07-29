from __future__ import annotations

from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1] / "skills" / "build-python-agent-service"


def test_agent_service_skill_has_local_first_framework_and_safety_contract() -> None:
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    for required in [
        "OpenAI Agents SDK",
        "LangGraph",
        "LlamaIndex",
        "Pydantic AI",
        "Google ADK Python",
        "AutoGen",
        "CrewAI",
        "capability gate",
        "read-only",
        "auto-with-escalation",
        "attempted versus executed side effects",
    ]:
        assert required in skill


def test_agent_service_interface_mentions_exact_model_and_approval() -> None:
    metadata = yaml.safe_load((SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8"))
    interface = metadata["interface"]

    assert interface["display_name"] == "Build Python Agent Service"
    assert "exact model" in interface["default_prompt"]
    assert "approval gate" in interface["default_prompt"]
