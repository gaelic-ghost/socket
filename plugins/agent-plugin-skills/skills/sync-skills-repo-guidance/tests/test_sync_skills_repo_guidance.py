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
                "Installable maintainer skills for skills-export repositories.",
                "OpenAI's documented Codex plugin system exposes repo-visible plugins through marketplace catalogs and does not document a richer repo-private scoping model beyond that.",
                "codex plugin marketplace add ./path/to/marketplace-root",
                "`agent-plugin-skills` entry points at `./plugins/agent-plugin-skills`",
                "declare the required dev dependencies in `pyproject.toml`",
                "`pytest`, `ruff`, and `mypy`",
                "the plugin manifest points to bundled skills with `\"skills\": \"./skills/\"`",
                "Follow the current OpenAI plugin structure literally: only `plugin.json` belongs in `.codex-plugin/`, while `skills/` stays at the plugin root.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / "AGENTS.md").write_text(
        "\n".join(
            [
                "Root `skills/` is the canonical authored and exported surface",
                'the manifest points to it with `"skills": "./skills/"`',
                "Do not recreate nested staged plugin directories",
                "Do not recreate `skills/install-plugin-to-socket` or `skills/validate-plugin-install-surfaces`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".gitignore").write_text(".claude/settings.local.json\n", encoding="utf-8")
    (repo_root / ".codex-plugin").mkdir()
    (repo_root / ".codex-plugin" / "plugin.json").write_text('{"skills": "./skills/"}\n', encoding="utf-8")
    (repo_root / "docs" / "maintainers" / "reality-audit.md").write_text(
        "\n".join(
            [
                "This repository ships root `.codex-plugin` packaging and does not track a nested staged plugin directory for itself.",
                'Its plugin manifest must declare `"skills": "./skills/"`',
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
                "Documented plugin path: `~/.codex/config.toml`",
                "If you mention project-scoped `.codex/config.toml`, label it as a general Codex config capability rather than part of the documented plugin install-surface map.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / "docs" / "maintainers" / "workflow-atlas.md").write_text(
        "\n".join(
            [
                "No skill in this repo should treat repo-local Codex plugin installs as a richer private scoping model than the marketplace-based behavior OpenAI documents.",
                'Root `.codex-plugin/plugin.json` points at that surface with `"skills": "./skills/"`.',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".agents").mkdir()
    (repo_root / ".claude").mkdir()
    os.symlink("../skills", repo_root / ".agents" / "skills")
    os.symlink("../skills", repo_root / ".claude" / "skills")


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


def test_audit_repo_flags_manifest_without_skills_component(tmp_path: Path) -> None:
    _write_repo(tmp_path, "example-skills")
    (tmp_path / ".codex-plugin" / "plugin.json").write_text("{}\n", encoding="utf-8")

    findings = m.audit_repo(tmp_path, "example-skills")

    assert any(finding.issue_id == "missing-skills-component" for finding in findings)
