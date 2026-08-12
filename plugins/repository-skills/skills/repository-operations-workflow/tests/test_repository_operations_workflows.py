from pathlib import Path

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_SKILLS_ROOT = SKILL_ROOT.parent


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def metadata(path: Path) -> dict:
    return yaml.safe_load(read(path).split("---", 2)[1])


def test_router_names_each_repository_owner_and_its_mutation_boundaries() -> None:
    router = read(SKILL_ROOT / "SKILL.md")
    router_metadata = metadata(SKILL_ROOT / "SKILL.md")
    agent = yaml.safe_load(read(SKILL_ROOT / "agents" / "openai.yaml"))["interface"]

    assert router_metadata["name"] == "repository-operations-workflow"
    for expected in (
        "`git-workflow`",
        "`github-collaboration-workflow`",
        "`codex-gui-worktree-workflow`",
        "`coordinate-worktrees-and-threads`",
        "`maintain-github-repository`",
        "`maintain-project-repo`",
        "machine-level defaults",
        "Do not infer permission to push, merge, tag, delete, publish, or change",
    ):
        assert expected in router
    assert "$repository-operations-workflow" in agent["default_prompt"]


def test_git_and_github_workflows_keep_local_collaboration_and_release_owners_separate() -> None:
    git_skill = REPOSITORY_SKILLS_ROOT / "git-workflow" / "SKILL.md"
    github_skill = REPOSITORY_SKILLS_ROOT / "github-collaboration-workflow" / "SKILL.md"

    assert metadata(git_skill)["name"] == "git-workflow"
    assert metadata(github_skill)["name"] == "github-collaboration-workflow"

    git_text = read(git_skill)
    github_text = read(github_skill)
    for expected in (
        "`git worktree list`",
        "reflog",
        "Push, force push, merge, tag, and destructive recovery actions require clear",
        "`github-collaboration-workflow`",
        "`maintain-project-repo`",
        "fetch.prune=true",
        "pull.ff=only",
        "branch.autoSetupRebase=always",
        "repository-local config",
    ):
        assert expected in git_text
    for expected in (
        "`gh` authentication",
        "one bounded snapshot",
        "`cronjob`",
        "`maintain-github-repository`",
        "`maintain-project-repo`",
    ):
        assert expected in github_text


def test_git_baseline_is_shared_machine_policy_without_local_template_writes() -> None:
    baseline = read(REPOSITORY_SKILLS_ROOT / "git-workflow" / "references" / "gale-git-baseline.md")
    repo_maintenance = read(REPOSITORY_SKILLS_ROOT / "maintain-project-repo" / "SKILL.md")

    for expected in (
        "fetch.prune = true",
        "pull.ff = only",
        "branch.autoSetupRebase = always",
        "git config --show-origin --get-regexp",
        "git config --local",
    ):
        assert expected in baseline
    assert "not write `git config --local`" in repo_maintenance
