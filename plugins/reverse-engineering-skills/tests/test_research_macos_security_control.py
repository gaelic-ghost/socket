from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_research_workflow_separates_public_private_and_runtime_evidence() -> None:
    skill = read("skills/research-macos-security-control/SKILL.md")
    hierarchy = read("skills/research-macos-security-control/references/source-and-evidence-hierarchy.md")
    matrix = read("skills/research-macos-security-control/references/control-research-matrix.md")
    note = read("skills/research-macos-security-control/references/technical-note-contract.md")

    assert "Do not present private symbols" in skill
    assert "exact macOS version/build" in skill
    assert "A private symbol or schema proves only" in hierarchy
    for control in ("TCC/privacy", "App Sandbox/files", "Execution/distribution", "Malware protection", "System integrity"):
        assert control in matrix
    for heading in ("Public Contract", "Direct Observations", "Private Implementation Evidence", "Hypotheses And Tests"):
        assert heading in note


def test_research_workflow_requires_bounded_probe_and_handoffs() -> None:
    probe = read("skills/research-macos-security-control/references/exact-build-probe-design.md")
    skill = read("skills/research-macos-security-control/SKILL.md")
    assert "Disposable SIP-enabled macOS guest" in probe
    assert "Do not prompt or mutate Gale's active Mac" in probe
    for owner in ("macos-privacy-permissions-workflow", "diagnose-apple-entitlements", "assess-macos-threat"):
        assert owner in skill
    assert "$research-macos-security-control" in read("skills/research-macos-security-control/agents/openai.yaml")
