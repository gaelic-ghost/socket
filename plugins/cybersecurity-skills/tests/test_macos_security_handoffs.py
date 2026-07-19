from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_macos_threat_workflows_route_app_and_private_control_questions() -> None:
    assess = read("skills/assess-macos-threat/SKILL.md")
    runtime = read("skills/inspect-macos-runtime-activity/SKILL.md")
    layers = read("skills/assess-macos-threat/references/macos-security-layers.md")
    for text in (assess, runtime, layers):
        assert "macos-privacy-permissions-workflow" in text
        assert "research-macos-security-control" in text
    assert "not automatically proof of prior execution" in layers
    assert "telemetry gap, not evidence" in runtime


def test_hardening_recovery_and_isolation_preserve_platform_controls() -> None:
    harden = read("skills/harden-macos/SKILL.md")
    recover = read("skills/contain-and-recover-macos/SKILL.md")
    select = read("skills/select-analysis-isolation/SKILL.md")
    lab = read("skills/prepare-isolated-analysis-lab/SKILL.md")
    assert "developer prompt/request implementation" in harden
    assert "Do not reset, disable, or weaken TCC" in recover
    assert "research-macos-security-control" in select
    assert "research-macos-security-control" in lab
