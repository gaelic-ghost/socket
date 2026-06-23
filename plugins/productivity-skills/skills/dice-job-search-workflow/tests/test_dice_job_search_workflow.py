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


def test_skill_metadata_targets_dice_job_search() -> None:
    metadata = frontmatter(read(SKILL_ROOT / "SKILL.md"))

    assert metadata["name"] == "dice-job-search-workflow"
    description = metadata["description"]
    for required in [
        "Dice.com job search",
        "MCP setup guidance",
        "resume-to-listing comparison",
        "search_jobs",
    ]:
        assert required in description


def test_skill_body_preserves_read_only_external_mcp_boundary() -> None:
    body = read(SKILL_ROOT / "SKILL.md")

    assert "https://mcp.dice.com/mcp" in body
    assert "plugins/productivity-skills/.mcp.json" in body
    assert "read-only job-search data source" in body
    assert "Do not apply to jobs" in body
    assert "Do not build a local MCP server" in body
    assert "Respect rate limits" in body
    assert "Keep personal job-search preferences" in body


def test_skill_lists_documented_search_parameters() -> None:
    body = read(SKILL_ROOT / "SKILL.md")

    for parameter in [
        "`keyword`",
        "`location`",
        "`radius`",
        "`radius_unit`",
        "`workplace_types`",
        "`employment_types`",
        "`employer_types`",
        "`posted_date`",
        "`willing_to_sponsor`",
        "`easy_apply`",
        "`jobs_per_page`",
        "`page_number`",
        "`fields`",
    ]:
        assert parameter in body


def test_openai_interface_metadata_matches_skill() -> None:
    metadata = yaml.safe_load(read(SKILL_ROOT / "agents" / "openai.yaml"))
    interface = metadata["interface"]

    assert interface["display_name"] == "Dice Job Search Workflow"
    assert "remote MCP server" in interface["short_description"]
    assert "$dice-job-search-workflow" in interface["default_prompt"]
    assert "search_jobs" in interface["default_prompt"]
    assert "ask before applying" in interface["default_prompt"]


def test_reference_records_official_dice_surfaces() -> None:
    reference = read(SKILL_ROOT / "references" / "dice-mcp-source-notes.md")

    for official_link in [
        "https://www.dice.com/about/mcp",
        "https://www.dice.com/career-advice/how-to-connect-the-dice-mcp-server-to-your-ai-assistant",
        "https://www.dice.com/career-advice/dice-launches-mcp-server-for-ai-powered-job-search",
    ]:
        assert official_link in reference

    assert "The documented MCP tool is `search_jobs`" in reference
    assert '"mcpServers": "./.mcp.json"' in reference
    assert '"url": "https://mcp.dice.com/mcp"' in reference
    assert "should bundle only the remote MCP config" in reference
