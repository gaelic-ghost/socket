from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_a2a_skill_keeps_protocol_roles_and_security_distinct() -> None:
    skill = read("skills/operate-a2a-agent-integration/SKILL.md")
    reference = read(
        "skills/operate-a2a-agent-integration/references/a2a-operations-map.md"
    )

    for term in ("Agent Card", "contextId", "taskId", "input-required"):
        assert term in skill
    assert "editor-to-agent hosting (ACP)" in skill
    assert "agent-to-tool calls (MCP)" in skill
    assert "SSRF controls" in skill
    assert "Hermes 0.20 Surface" in reference


def test_protocol_chooser_routes_peer_agents_to_a2a() -> None:
    skill = read("skills/choose-agent-integration-protocol/SKILL.md")
    reference = read(
        "skills/choose-agent-integration-protocol/references/protocol-decision-map.md"
    )

    assert "Use A2A when independently operated agents" in skill
    assert "operate-a2a-agent-integration" in skill
    assert "three distinct trust, lifecycle, and permission boundaries" in reference


def test_acp_guidance_separates_latest_v1_from_draft_work() -> None:
    operator = read("skills/operate-acp-agent-integration/SKILL.md")
    builder = read("skills/build-acp-agent/SKILL.md")
    implementation = read("skills/build-acp-agent/references/acp-implementation-map.md")

    for text in (operator, builder, implementation):
        assert "ACP v1" in text
        assert "v2" in text
    assert "draft RFD" in operator
    assert "session/close" in implementation
    assert "additional directories" in implementation
