from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_metadata_and_interface_name_the_settings_scope() -> None:
    skill_text = read(SKILL_ROOT / "SKILL.md")
    frontmatter = skill_text.split("---", 2)[1]
    metadata = yaml.safe_load(frontmatter)
    interface = yaml.safe_load(read(SKILL_ROOT / "agents" / "openai.yaml"))["interface"]

    assert metadata["name"] == "maintain-github-repository"
    assert "GitHub repository's server-side settings" in metadata["description"]
    assert "ordinary local Git commits" in metadata["description"]
    assert interface["display_name"] == "Maintain GitHub Repository"
    assert "$maintain-github-repository" in interface["default_prompt"]


def test_settings_reference_covers_recommended_baseline_and_guards() -> None:
    reference = read(SKILL_ROOT / "references" / "github-repository-settings.md")

    for expected in (
        "Dependabot alerts and security updates enabled",
        "private vulnerability reporting enabled for public repositories",
        "web commit sign-off required when the repository uses DCO",
        "preserve documented owner or maintainer direct pushes",
        "visibility changes",
        "gh repo edit",
        "gh api",
    ):
        assert expected in reference


def test_trigger_eval_routes_settings_and_release_requests_separately() -> None:
    trigger_eval = read(SKILL_ROOT / "references" / "trigger-eval.md")

    for expected in (
        "Apply my normal GitHub repository settings.",
        "Audit this repo's branch protection and Dependabot settings.",
        "Release version 1.4.0.",
        "Tag this commit and create the GitHub release.",
        "route to `maintain-project-repo`",
    ):
        assert expected in trigger_eval
