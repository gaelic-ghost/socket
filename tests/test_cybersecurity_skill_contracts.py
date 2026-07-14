from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "plugins" / "cybersecurity-skills" / "skills"


def skill_text(name: str) -> str:
    return (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8").lower()


def assert_contract(name: str, *required_phrases: str) -> None:
    contents = skill_text(name)
    missing = [phrase for phrase in required_phrases if phrase.lower() not in contents]
    assert not missing, f"{name} is missing required contract phrases: {missing}"


def test_benign_lookalikes_do_not_become_binary_verdicts() -> None:
    assert_contract(
        "assess-and-explain-threat",
        "binary safe/malicious verdict",
        "contradicting evidence",
        "state confidence separately",
    )


def test_remote_reputation_requires_egress_approval() -> None:
    assert_contract(
        "check-artifact-reputation",
        "explicit approval",
        "upload",
        "privacy",
    )


def test_isolation_rejects_linux_container_for_macos_payload() -> None:
    assert_contract(
        "select-analysis-isolation",
        "use a macos vm or spare mac for macos payload behavior",
        "do not substitute a linux container",
        "no host share or forwarded port remains",
    )


def test_authorized_testing_has_scope_and_stop_conditions() -> None:
    assert_contract(
        "scope-authorized-security-test",
        "access to a target or a public address is not permission",
        "establish stop conditions",
        "update the scope record before expanding work",
    )


def test_vulnerability_validation_keeps_negative_results() -> None:
    assert_contract(
        "validate-vulnerability",
        "smallest safe proof",
        "not reachable",
        "false positive",
        "stop before destructive impact",
    )


def test_macos_assessment_separates_platform_controls() -> None:
    assert_contract(
        "assess-macos-threat",
        "gatekeeper",
        "notarization",
        "xprotect",
        "tcc",
        "sip",
    )


def test_macos_recovery_preserves_evidence_and_verifies_outcome() -> None:
    assert_contract(
        "contain-and-recover-macos",
        "preserve decisive evidence",
        "prefer reversible",
        "residual uncertainty",
        "return-to-service decision",
    )


def test_incident_containment_records_operational_impact() -> None:
    assert_contract(
        "contain-security-incident",
        "business impact",
        "volatile evidence",
        "rollback",
    )


def test_detection_content_requires_positive_and_negative_fixtures() -> None:
    assert_contract(
        "author-detection-content",
        "test fixtures",
        "benign negatives",
        "false positives",
        "telemetry contract",
    )


def test_non_specialist_advice_is_immediate_and_calm() -> None:
    assert_contract(
        "assess-and-explain-threat",
        "plain-language",
        "what to do now",
        "avoid fear",
    )


def test_repository_scanning_routes_to_codex_security() -> None:
    assert_contract(
        "route-security-work",
        "codex security",
        "repository-wide",
        "reverse-engineering-skills",
    )
