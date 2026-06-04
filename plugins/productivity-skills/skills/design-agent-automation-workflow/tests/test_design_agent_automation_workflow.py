from __future__ import annotations

from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def frontmatter(text: str) -> dict[str, str]:
    assert text.startswith("---\n")
    _empty, raw_yaml, _body = text.split("---", 2)
    return yaml.safe_load(raw_yaml)


def test_skill_metadata_names_framework_neutral_scope() -> None:
    metadata = frontmatter(read(SKILL_ROOT / "SKILL.md"))

    assert metadata["name"] == "design-agent-automation-workflow"
    description = metadata["description"]
    for required in [
        "Codex app automations",
        "codex exec",
        "Codex subagents",
        "OpenAI Agents SDK",
        "LangGraph",
        "Hermes",
        "full-auto",
        "auto-with-escalation",
        "no automation yet",
    ]:
        assert required in description


def test_skill_body_preserves_planning_not_runtime_boundary() -> None:
    body = read(SKILL_ROOT / "SKILL.md")

    assert "framework-neutral planning surface" in body
    assert "Do not implement framework runtime code" in body
    assert "Do not wrap OpenAI Agents SDK, LangGraph, Hermes, or Codex runtimes" in body
    assert "Prefer safe full automation" in body
    assert "Use human review only for the exact" in body
    assert "Return a concise plan with these sections" in body


def test_openai_interface_metadata_matches_skill() -> None:
    metadata = yaml.safe_load(read(SKILL_ROOT / "agents" / "openai.yaml"))
    interface = metadata["interface"]

    assert interface["display_name"] == "Design Agent Automation Workflow"
    assert "agent or automation surface" in interface["short_description"]
    assert "$design-agent-automation-workflow" in interface["default_prompt"]
    assert "safe full automation" in interface["default_prompt"]
    assert "auto-with-escalation" in interface["default_prompt"]
    assert "implementation handoff" in interface["default_prompt"]


def test_framework_reference_covers_all_selection_surfaces() -> None:
    reference = read(SKILL_ROOT / "references" / "framework-selection.md")

    for required in [
        "Codex app automation",
        "`codex exec` or Codex GitHub Action",
        "Codex subagents",
        "OpenAI Agents SDK service",
        "LangGraph graph",
        "Hermes-specific workflow",
        "Full-auto execution",
        "Auto-with-escalation",
        "No automation yet",
    ]:
        assert required in reference

    for official_link in [
        "https://developers.openai.com/codex/app/automations",
        "https://developers.openai.com/codex/noninteractive",
        "https://developers.openai.com/codex/subagents",
        "https://developers.openai.com/api/docs/guides/agents",
        "https://docs.langchain.com/oss/python/langgraph/overview",
        "https://hermes-agent.nousresearch.com/docs",
    ]:
        assert official_link in reference


def test_plan_template_has_required_output_sections() -> None:
    template = read(SKILL_ROOT / "references" / "automation-plan-template.md")

    for heading in [
        "## Recommendation",
        "## Not Chosen",
        "## State And Safety",
        "## Scaffold",
        "## Validation",
        "## Handoff",
        "## Sources",
    ]:
        assert heading in template
