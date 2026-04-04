from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "maintain_plugin_docs.py"
    spec = importlib.util.spec_from_file_location("maintain_plugin_docs", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


VALID_PUBLIC_README = """# productivity-skills

Curated Codex skills for productivity workflows.

## Table of Contents

- [What These Agent Skills Help With](#what-these-agent-skills-help-with)
- [Skill Guide (When To Use What)](#skill-guide-when-to-use-what)
- [Quick Start (Vercel Skills CLI)](#quick-start-vercel-skills-cli)
- [Install individually by Skill or Skill Pack](#install-individually-by-skill-or-skill-pack)
- [Update Skills](#update-skills)
- [More resources for similar Skills](#more-resources-for-similar-skills)
- [Repository Layout](#repository-layout)
- [Notes](#notes)
- [Keywords](#keywords)
- [License](#license)

## What These Agent Skills Help With

This repository packages reusable Codex skills for maintainers.

## Skill Guide (When To Use What)

- `example-skill`
  - Use when you need the example workflow.

## Quick Start (Vercel Skills CLI)

```bash
npx skills add gaelic-ghost/productivity-skills
```

## Install individually by Skill or Skill Pack

```bash
npx skills add gaelic-ghost/productivity-skills --skill example-skill
```

## Update Skills

```bash
npx skills check
npx skills update
```

## More resources for similar Skills

### Find Skills like these with the `skills` CLI by Vercel — [vercel-labs/skills](https://github.com/vercel-labs/skills)

```bash
npx skills find "productivity skills"
npx skills find "codex maintenance"
npx skills find "automation workflows"
```

### Find Skills like these with the `Find Skills` Agent Skill by Vercel — [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)

```bash
# `Find Skills` is a part of Vercel's `agent-skills` repo
npx skills add vercel-labs/agent-skills --skill find-skills
```

Then ask your Agent for help finding a skill for "" or ""

### Leaderboard

- Skills catalog: [skills.sh](https://skills.sh/)

## Repository Layout

```text
.
├── README.md
└── example-skill/
```

## Notes

- Keep README commands synchronized with the active skills.

## Keywords

Codex skills, productivity workflows.

## License

See [LICENSE](./LICENSE).
"""


VALID_PLUGIN_MAINTAINER_README = """# agent-plugin-skills

Canonical repo-maintainer skills for building, aligning, and evolving agent-skills and agent-plugin repositories.

## Active Skills

- `maintain-plugin-docs`
  - Current implementation: audit and bounded fixes for `README.md`, `ROADMAP.md`, or both.
  - Intended scope: become the combined docs maintainer for plugin-development repos here.

## Repo Purpose

This repository is intentionally stack-specific.

## Packaging And Discovery

Root [`skills/`](./skills/) is the canonical authored skill surface.

## Standards And Docs

- Agent Skills Standard: [agentskills.io/home](https://agentskills.io/home)

## Maintainer Python Tooling

```bash
uv sync --dev
uv tool install ruff
uv tool install mypy
uv run --group dev pytest
```

## Install

### Codex Plugin

Use the plugin package in [`plugins/agent-plugin-skills/.codex-plugin/plugin.json`](./plugins/agent-plugin-skills/.codex-plugin/plugin.json).

### Claude Code Plugin

Use the plugin package in [`plugins/agent-plugin-skills/.claude-plugin/plugin.json`](./plugins/agent-plugin-skills/.claude-plugin/plugin.json).

### Vercel `skills` CLI

```bash
npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-plugin-docs
```

## Repository Layout

```text
.
├── skills/
└── plugins/
```

## License

See [LICENSE](./LICENSE).
"""


def test_discover_repos_and_detect_profile(tmp_path: Path) -> None:
    public_repo = tmp_path / "productivity-skills"
    bootstrap_repo = tmp_path / "a11y-skills"
    plugin_repo = tmp_path / "agent-plugin-skills"
    ignored_repo = tmp_path / "notes"
    public_repo.mkdir()
    bootstrap_repo.mkdir()
    (plugin_repo / "skills").mkdir(parents=True)
    (plugin_repo / "plugins" / "agent-plugin-skills" / ".codex-plugin").mkdir(parents=True)
    (plugin_repo / "plugins" / "agent-plugin-skills" / ".codex-plugin" / "plugin.json").write_text("{}", encoding="utf-8")
    ignored_repo.mkdir()

    repos = m.discover_repos(tmp_path, "*-skills", [])

    assert repos == [bootstrap_repo, plugin_repo, public_repo]
    assert m.detect_profile(public_repo) == "public-curated"
    assert m.detect_profile(bootstrap_repo) == "bootstrap"
    assert m.detect_profile(plugin_repo) == "plugin-maintainer"


def test_check_sections_accepts_minimal_valid_public_readme(tmp_path: Path) -> None:
    repo = tmp_path / "productivity-skills"
    repo.mkdir()

    issues = m.check_sections(repo, "public-curated", VALID_PUBLIC_README)

    assert issues == []


def test_check_sections_accepts_plugin_maintainer_readme(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    repo.mkdir()

    issues = m.check_sections(repo, "plugin-maintainer", VALID_PLUGIN_MAINTAINER_README)

    assert issues == []


def test_check_sections_flags_missing_tooling_guidance_snippets(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    repo.mkdir()
    broken = VALID_PLUGIN_MAINTAINER_README.replace("uv tool install ruff\nuv tool install mypy\n", "")

    issues = m.check_sections(repo, "plugin-maintainer", broken)

    assert any(issue.issue_id == "tooling-guidance-missing-snippet" for issue in issues)


def test_check_sections_flags_missing_required_section(tmp_path: Path) -> None:
    repo = tmp_path / "productivity-skills"
    repo.mkdir()
    broken = VALID_PUBLIC_README.replace("## Update Skills\n\n```bash\nnpx skills check\nnpx skills update\n```\n\n", "")

    issues = m.check_sections(repo, "public-curated", broken)

    assert any(issue.issue_id == "section-missing-update_skills" for issue in issues)


def test_parse_skills_add_command_line_handles_canonical_and_legacy_forms() -> None:
    canonical = m.parse_skills_add_command_line(
        "npx skills add gaelic-ghost/productivity-skills --skill example-skill"
    )
    legacy = m.parse_skills_add_command_line(
        "npx skills add gaelic-ghost/productivity-skills@example-skill"
    )

    assert canonical is not None
    assert canonical.owner == "gaelic-ghost"
    assert canonical.repo == "productivity-skills"
    assert canonical.option_skill == "example-skill"
    assert canonical.legacy_skill is None

    assert legacy is not None
    assert legacy.legacy_skill == "example-skill"
    assert legacy.option_skill is None


def test_check_commands_flags_legacy_and_unknown_skill(tmp_path: Path) -> None:
    repo = tmp_path / "productivity-skills"
    repo.mkdir()
    text = "\n".join(
        [
            "```bash",
            "npx skills add gaelic-ghost/productivity-skills",
            "npx skills add gaelic-ghost/productivity-skills@example-skill",
            "npx skills add gaelic-ghost/productivity-skills --skill missing-skill",
            "```",
        ]
    )

    issues = m.check_commands(repo, "public-curated", text, ["example-skill"])

    assert any(issue.issue_id == "legacy-skills-add-syntax" for issue in issues)
    assert any(issue.issue_id == "missing-skill-ref-missing-skill" for issue in issues)


def test_apply_fixes_for_repo_normalizes_legacy_install_syntax(tmp_path: Path) -> None:
    repo = tmp_path / "productivity-skills"
    repo.mkdir()
    (repo / "example-skill").mkdir()
    (repo / "example-skill" / "SKILL.md").write_text("---\nname: example-skill\ndescription: Example.\n---\n", encoding="utf-8")
    readme = repo / "README.md"
    readme.write_text(
        VALID_PUBLIC_README.replace(
            "npx skills add gaelic-ghost/productivity-skills --skill example-skill",
            "npx skills add gaelic-ghost/productivity-skills@example-skill",
        ),
        encoding="utf-8",
    )

    changed, fixes, reason = m.apply_fixes_for_repo(repo, "public-curated", ["example-skill"])

    assert changed is True
    assert reason is None
    updated = readme.read_text(encoding="utf-8")
    assert "npx skills add gaelic-ghost/productivity-skills --skill example-skill" in updated
    assert "@example-skill" not in updated
    assert any(fix["rule"] == "normalize-skills-add-syntax" for fix in fixes)


def test_validate_roadmap_flags_missing_required_sections(tmp_path: Path) -> None:
    repo = tmp_path / "plugin-skills"
    repo.mkdir()
    roadmap = """# Project Roadmap

## Vision

- Example vision.
"""

    findings = m.validate_roadmap(repo, roadmap)

    issue_ids = {issue.issue_id for issue in findings}
    assert "roadmap-missing-section-product-principles" in issue_ids
    assert "roadmap-missing-section-milestone-progress" in issue_ids
    assert "roadmap-missing-milestones" in issue_ids


def test_apply_fixes_for_roadmap_creates_default_when_missing(tmp_path: Path) -> None:
    repo = tmp_path / "plugin-skills"
    repo.mkdir()

    changed, fixes, reason = m.apply_fixes_for_roadmap(repo)

    assert changed is True
    assert reason is None
    roadmap = (repo / "ROADMAP.md").read_text(encoding="utf-8")
    assert "## Product Principles" in roadmap
    assert "## Milestone Progress" in roadmap
    assert any(fix["rule"] == "create-missing-roadmap" for fix in fixes)


def test_check_cross_doc_consistency_flags_legacy_skill_name(tmp_path: Path) -> None:
    repo = tmp_path / "plugin-skills"
    repo.mkdir()

    findings = m.check_cross_doc_consistency(
        repo,
        "Use maintain-skills-readme here.",
        "Milestone notes still mention maintain-plugin-docs.",
    )

    assert any(issue.issue_id == "cross-doc-legacy-skill-name" for issue in findings)


def test_validate_roadmap_flags_progress_reality_mismatch_and_bad_format(tmp_path: Path) -> None:
    repo = tmp_path / "plugin-skills"
    repo.mkdir()
    roadmap = """# Project Roadmap

## Vision

- Example vision.

## Product Principles

- Example principle.

## Milestone Progress

- [x] Milestone 0: Foundation
- [ ] Wrong freeform status line

## Milestone 0: Foundation

Scope:

- Foundation scope.

Tickets:

- [ ] Add implementation.

Exit criteria:

- [ ] Validate milestone.
"""

    findings = m.validate_roadmap(repo, roadmap)

    issue_ids = {issue.issue_id for issue in findings}
    assert "roadmap-progress-reality-mismatch-0" in issue_ids
    assert "roadmap-progress-entry-format-14" in issue_ids


def test_apply_fixes_for_roadmap_normalizes_progress_and_subsection_order(tmp_path: Path) -> None:
    repo = tmp_path / "plugin-skills"
    repo.mkdir()
    roadmap = repo / "ROADMAP.md"
    roadmap.write_text(
        """# Project Roadmap

## Product principles

- Keep docs aligned.

## Vision

- Build the repo.

## Milestone 1: Finish

Exit criteria:

- [x] Exit.

Scope:

- Scope item.

Tickets:

- [x] Ticket item.
""",
        encoding="utf-8",
    )

    changed, fixes, reason = m.apply_fixes_for_roadmap(repo)

    assert changed is True
    assert reason is None
    updated = roadmap.read_text(encoding="utf-8")
    assert "## Vision" in updated
    assert "## Product Principles" in updated
    assert "## Milestone Progress" in updated
    assert "- [x] Milestone 1: Finish" in updated
    assert updated.index("## Vision") < updated.index("## Product Principles") < updated.index("## Milestone Progress") < updated.index("## Milestone 1: Finish")
    assert updated.index("Scope:") < updated.index("Tickets:") < updated.index("Exit criteria:")
    assert any(fix["rule"] == "normalize-roadmap-structure" for fix in fixes)


def test_check_cross_doc_consistency_flags_missing_plugin_sections(tmp_path: Path) -> None:
    repo = tmp_path / "agent-plugin-skills"
    repo.mkdir()
    skill_root = repo / "skills" / "maintain-plugin-docs"
    skill_root.mkdir(parents=True)
    (skill_root / "SKILL.md").write_text("---\nname: maintain-plugin-docs\ndescription: Example.\n---\n", encoding="utf-8")
    codex_manifest = repo / "plugins" / "agent-plugin-skills" / ".codex-plugin"
    claude_manifest = repo / "plugins" / "agent-plugin-skills" / ".claude-plugin"
    codex_manifest.mkdir(parents=True)
    claude_manifest.mkdir(parents=True)
    (codex_manifest / "plugin.json").write_text("{}", encoding="utf-8")
    (claude_manifest / "plugin.json").write_text("{}", encoding="utf-8")

    readme = """## Active Skills

- `maintain-plugin-docs`
  - Current implementation: docs checks.
  - Intended scope: wider docs maintainer.

## Install

Install one skill through the Vercel `skills` CLI:

```bash
npx skills add gaelic-ghost/agent-plugin-skills --skill maintain-plugin-docs
```
"""
    roadmap = """# Project Roadmap

## Vision

- Example vision.

## Product Principles

- Example principle.

## Milestone Progress

- [ ] Milestone 1: `maintain-plugin-docs` evolution

## Milestone 1: `maintain-plugin-docs` evolution

Scope:

- Example scope.

Tickets:

- [ ] Rebalance README install guidance so Codex Plugin and Claude Code Plugin installs are primary.

Exit criteria:

- [ ] Scope is complete.
"""

    findings = m.check_cross_doc_consistency(repo, readme, roadmap)

    issue_ids = {issue.issue_id for issue in findings}
    assert "cross-doc-missing-codex-plugin-install" in issue_ids
    assert "cross-doc-missing-claude-plugin-install" in issue_ids
