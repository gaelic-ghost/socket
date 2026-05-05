from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "sync_skills_repo_guidance.py"
    spec = importlib.util.spec_from_file_location("sync_skills_repo_guidance", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def _write_repo(repo_root: Path, _plugin_name: str) -> None:
    (repo_root / "skills" / "example-skill").mkdir(parents=True)
    (repo_root / "docs" / "maintainers").mkdir(parents=True)
    (repo_root / "README.md").write_text(
        "\n".join(
            [
                "Installable maintainer skills for skills-export and plugin-export repositories.",
                "OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that.",
                "codex plugin marketplace add gaelic-ghost/socket",
                "codex plugin marketplace upgrade socket",
                "`agent-plugin-skills` entry points at `./plugins/agent-plugin-skills`",
                "Git-backed marketplace sources",
                "dev dependencies in `pyproject.toml`",
                "`pytest`, `ruff`, and `mypy`",
                "`\"skills\": \"./skills/\"`",
                "Only `plugin.json` belongs in `.codex-plugin/`",
                "refresh the official OpenAI docs",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / "AGENTS.md").write_text(
        "\n".join(
            [
                "canonical authored and exported surface",
                'manifest points to bundled skills with `"skills": "./skills/"`',
                "`hooks/`",
                "Resolve shared project dependencies only from GitHub repository URLs, package managers, package registries, or other real remote repositories",
                "Machine-local dependency paths are expressly prohibited in any project that is public or intended to be shared publicly",
                "Default user-facing install and update guidance to Git-backed marketplace sources",
                "`skills/install-plugin-to-socket`",
                "`skills/validate-plugin-install-surfaces`",
                "check the current OpenAI Codex docs",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".gitignore").write_text(".venv/\n", encoding="utf-8")
    (repo_root / ".codex-plugin").mkdir()
    (repo_root / ".codex-plugin" / "plugin.json").write_text('{"skills": "./skills/"}\n', encoding="utf-8")
    (repo_root / "docs" / "maintainers" / "reality-audit.md").write_text(
        "\n".join(
            [
                "This repository ships root `.codex-plugin` packaging and does not track a nested staged plugin directory for itself.",
                'Its plugin manifest must declare `"skills": "./skills/"`',
                "user installs normally come through the Git-backed `socket` marketplace",
                "This repository does not ship `install-plugin-to-socket`.",
                "This repository does not ship `validate-plugin-install-surfaces`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / "docs" / "maintainers" / "codex-plugin-install-surfaces.md").write_text(
        "\n".join(
            [
                "only `plugin.json` belongs in `.codex-plugin/`",
                'plugin manifests point to bundled skill folders with a root-relative `"skills": "./skills/"` field',
                "Tracked marketplace source",
                "Preferred User Install And Update Path",
                "codex plugin marketplace add gaelic-ghost/socket",
                "codex plugin marketplace upgrade socket",
                "Documented plugin path: `~/.codex/config.toml`",
                "If you mention project-scoped `.codex/config.toml`, label it as a general Codex config capability rather than part of the documented plugin install-surface map.",
                "first route through the Codex harness surfaces that are already available in the current session",
                "install the plugin through Codex's plugin directory for future sessions",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".agents").mkdir()
    os.symlink("../skills", repo_root / ".agents" / "skills")


def test_audit_repo_accepts_expected_repo_shape(tmp_path: Path) -> None:
    _write_repo(tmp_path, "example-skills")

    findings = m.audit_repo(tmp_path, "example-skills")

    assert findings == []


def test_audit_repo_flags_missing_guidance_and_forbidden_path(tmp_path: Path) -> None:
    (tmp_path / "plugins").mkdir(parents=True)
    (tmp_path / "README.md").write_text("", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "maintainers").mkdir(parents=True)
    (tmp_path / "docs" / "maintainers" / "reality-audit.md").write_text("", encoding="utf-8")

    findings = m.audit_repo(tmp_path, "example-skills")

    issue_ids = {finding.issue_id for finding in findings}
    assert "readme-missing-snippet" in issue_ids
    assert "agents-missing-snippet" in issue_ids
    assert "missing-symlink" in issue_ids
    assert "forbidden-path" in issue_ids
    assert "missing-plugin-manifest" in issue_ids


def test_audit_repo_does_not_require_optional_maintainer_docs(tmp_path: Path) -> None:
    _write_repo(tmp_path, "example-skills")
    (tmp_path / "docs" / "maintainers" / "reality-audit.md").unlink()
    (tmp_path / "docs" / "maintainers" / "codex-plugin-install-surfaces.md").unlink()

    findings = m.audit_repo(tmp_path, "example-skills")

    assert findings == []


def test_audit_repo_flags_manifest_without_skills_component(tmp_path: Path) -> None:
    _write_repo(tmp_path, "example-skills")
    (tmp_path / ".codex-plugin" / "plugin.json").write_text("{}\n", encoding="utf-8")

    findings = m.audit_repo(tmp_path, "example-skills")

    assert any(finding.issue_id == "missing-skills-component" for finding in findings)
