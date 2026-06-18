from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_bootstrap_and_sync_skills_route_github_settings_to_repo_maintenance() -> None:
    skill_paths = (
        "skills/bootstrap-swift-package/SKILL.md",
        "skills/sync-swift-package-guidance/SKILL.md",
        "skills/bootstrap-xcode-app-project/SKILL.md",
        "skills/sync-xcode-project-guidance/SKILL.md",
    )

    for relative_path in skill_paths:
        skill_text = (ROOT / relative_path).read_text(encoding="utf-8")
        assert "productivity-skills:maintain-project-repo" in skill_text
        assert "repository features" in skill_text
        assert "branch protection" in skill_text
