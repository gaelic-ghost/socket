from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_privacy_workflow_preserves_permission_boundaries() -> None:
    skill = read("skills/macos-privacy-permissions-workflow/SKILL.md")
    matrix = read("skills/macos-privacy-permissions-workflow/references/permission-class-matrix.md")
    reset = read("skills/macos-privacy-permissions-workflow/references/prompting-settings-reset-and-mdm.md")
    attribution = read("skills/macos-privacy-permissions-workflow/references/responsible-code-and-attribution.md")

    for term in (
        "AXIsProcessTrustedWithOptions",
        "AEDeterminePermissionToAutomateTarget",
        "EPDeveloperTool.authorizationStatus",
        "CGPreflightScreenCaptureAccess",
        "Full Disk Access",
    ):
        assert term in matrix
    assert "reset surface, not a general grant or status tool" in reset
    assert "Terminal, an IDE, or an agent host" in attribution
    assert "Do not edit, replace, copy back, or directly query a live TCC database" in skill
    assert "explicit approval immediately before" in skill


def test_privacy_workflow_has_discovery_metadata() -> None:
    name = "macos-privacy-permissions-workflow"
    assert f"./skills/{name}/SKILL.md" in read(".github/scripts/validate_repo_docs.sh")
    assert f"${name}" in read(f"skills/{name}/agents/openai.yaml")


def test_sandbox_file_workflow_preserves_authorization_lifetime() -> None:
    skill = read("skills/macos-sandbox-file-access-workflow/SKILL.md")
    lifecycle = read("skills/macos-sandbox-file-access-workflow/references/security-scoped-bookmark-lifecycle.md")
    controls = read("skills/macos-sandbox-file-access-workflow/references/sandbox-and-filesystem-control-map.md")
    boundaries = read("skills/macos-sandbox-file-access-workflow/references/helpers-groups-and-process-boundaries.md")
    assert "startAccessingSecurityScopedResource()" in lifecycle
    assert "stopAccessingSecurityScopedResource()" in lifecycle
    assert "If stale" in lifecycle
    for layer in ("POSIX and ACL", "App Sandbox", "TCC", "Data Vault/SIP"):
        assert layer in controls
    assert "Do not pass a path across IPC and assume authorization follows" in boundaries
    assert "Do not claim a bookmark bypasses TCC" in skill


def test_entitlement_workflow_requires_five_state_evidence() -> None:
    skill = read("skills/diagnose-apple-entitlements/SKILL.md")
    comparison = read("skills/diagnose-apple-entitlements/references/five-state-entitlement-comparison.md")
    classification = read("skills/diagnose-apple-entitlements/references/restricted-and-private-entitlements.md")
    artifact = read("skills/diagnose-apple-entitlements/references/artifact-and-nested-code-inspection.md")
    for state in ("Desired behavior", "Tracked source", "Account authorization", "Signed result", "Runtime result"):
        assert state in comparison
    assert "do not recommend them for an ordinary third-party product" in classification
    assert "`codesign --deep` verification is not a substitute" in artifact
    assert "Do not call an entitlement effective" in skill


def test_slice_two_skills_have_discovery_metadata() -> None:
    validator = read(".github/scripts/validate_repo_docs.sh")
    for name in ("macos-sandbox-file-access-workflow", "diagnose-apple-entitlements"):
        assert f"./skills/{name}/SKILL.md" in validator
        assert f"${name}" in read(f"skills/{name}/agents/openai.yaml")
