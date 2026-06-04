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


def test_skill_metadata_names_eval_scope() -> None:
    metadata = frontmatter(read(SKILL_ROOT / "SKILL.md"))

    assert metadata["name"] == "design-agent-eval-workflow"
    description = metadata["description"]
    for required in [
        "agent",
        "skill",
        "prompt",
        "automation",
        "full-auto",
        "OpenAI Agents SDK",
        "LangGraph",
    ]:
        assert required in description


def test_skill_body_prefers_safe_full_automation() -> None:
    body = read(SKILL_ROOT / "SKILL.md")

    assert "Prefer full automation" in body
    assert "Use human-in-the-loop only for the exact decision" in body
    assert "auto-with-escalation" in body
    assert "manual-only-for-now" in body


def test_openai_interface_metadata_matches_skill() -> None:
    metadata = yaml.safe_load(read(SKILL_ROOT / "agents" / "openai.yaml"))
    interface = metadata["interface"]

    assert interface["display_name"] == "Design Agent Eval Workflow"
    assert "agent, skill, prompt, and automation behavior" in interface["short_description"]
    assert "$design-agent-eval-workflow" in interface["default_prompt"]
    assert "full-auto" in interface["default_prompt"]


def test_eval_surface_reference_covers_runtime_choices() -> None:
    reference = read(SKILL_ROOT / "references" / "eval-surface-selection.md")

    for required in [
        "Local script or pytest",
        "`codex exec` or Codex GitHub Action",
        "Codex app automation",
        "OpenAI Agents SDK eval/tracing",
        "LangGraph or LangSmith eval",
        "Stack-owned runner",
    ]:
        assert required in reference

    for official_link in [
        "https://developers.openai.com/codex/noninteractive",
        "https://developers.openai.com/codex/github-action",
        "https://developers.openai.com/api/docs/guides/evals",
        "https://docs.langchain.com/oss/python/langgraph/overview",
        "https://docs.smith.langchain.com/evaluation",
    ]:
        assert official_link in reference


def test_eval_plan_template_has_required_output_sections() -> None:
    template = read(SKILL_ROOT / "references" / "eval-plan-template.md")

    for heading in [
        "## Recommendation",
        "## Behavior Under Test",
        "## Case Set",
        "## Graders",
        "## Safety Gates",
        "## Run Cadence",
        "## Scaffold",
        "## Handoff",
        "## Sources",
    ]:
        assert heading in template
