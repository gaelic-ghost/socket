from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"


def test_root_agents_stays_bounded_and_routes_to_live_owners() -> None:
    guidance = AGENTS.read_text()

    assert len(guidance.split()) <= 1_100

    required_owners = (
        "CONTRIBUTING.md",
        "subtree-workflow.md",
        "release-workflow.md",
        "codex-plugin-install-surfaces.md",
        "deferred-work-wakeup-policy.md",
        "spi-add-package-automation-plan.md",
    )
    for owner in required_owners:
        assert owner in guidance


def test_root_agents_keeps_high_risk_guards_directly_visible() -> None:
    guidance = " ".join(AGENTS.read_text().split())

    required_guards = (
        "do not subtree-push",
        "no local `plugins/SpeakSwiftlyServer` mirror",
        "not an aggregate plugin",
        "Do not hold a terminal open or create a polling loop",
        "Never substitute `gh issue create`",
        "Do not delete a branch, worktree, remote branch, archive ref, rescue ref",
        "Ask before adding or reintroducing a subtree-managed child repository",
        "Ask before broadening Socket",
    )
    for guard in required_guards:
        assert guard in guidance


def test_root_agents_does_not_reabsorb_domain_or_command_detail() -> None:
    guidance = AGENTS.read_text()

    prohibited_details = (
        "@Query",
        "AWSClient",
        "uv sync --dev",
        "git subtree pull",
        "deferred-work-wakeup-policy-plan.md",
    )
    for detail in prohibited_details:
        assert detail not in guidance


def test_live_docs_agree_that_speak_swiftly_has_no_local_mirror() -> None:
    contributing = (ROOT / "CONTRIBUTING.md").read_text()
    roadmap = (ROOT / "ROADMAP.md").read_text()
    subtree_workflow = (
        ROOT / "docs" / "maintainers" / "subtree-workflow.md"
    ).read_text()

    assert "does not keep a local `plugins/SpeakSwiftlyServer` mirror" in contributing
    assert "retiring the local `plugins/SpeakSwiftlyServer/` mirror" in roadmap
    assert "no longer imports the standalone source tree" in subtree_workflow
    assert not (ROOT / "plugins" / "SpeakSwiftlyServer").exists()
