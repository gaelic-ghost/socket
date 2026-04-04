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


def _write_repo(repo_root: Path, plugin_name: str) -> None:
    (repo_root / "plugins" / plugin_name).mkdir(parents=True)
    (repo_root / "docs" / "maintainers").mkdir(parents=True)
    (repo_root / ".claude-plugin").mkdir()
    (repo_root / "README.md").write_text(
        "\n".join(
            [
                "root `skills/` as the canonical authoring surface",
                "plugins/",
                ".agents/plugins/marketplace.json",
                "~/.codex/plugins/",
                ".claude-plugin/marketplace.json",
                "claude --plugin-dir",
                "Track canonical plugin source trees and shared marketplace catalogs in git.",
                "OpenAI Codex Skills",
                "Claude Code Plugins",
                "uv tool install ruff",
                "uv tool install mypy",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / "AGENTS.md").write_text(
        "\n".join(
            [
                "canonical workflow-authoring surface",
                "plugin packaging root",
                ".agents/plugins/marketplace.json",
                ".claude-plugin/marketplace.json",
                "Track canonical plugin source trees and shared marketplace catalogs in git.",
                "uv-managed tools",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".gitignore").write_text(
        "\n".join(
            [
                "# Agent plugin repo local runtime state",
                ".codex/plugins/",
                ".claude/settings.local.json",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".claude-plugin" / "marketplace.json").write_text(
        "\n".join(
            [
                "{",
                f'  "name": "{plugin_name}",',
                '  "plugins": [',
                "    {",
                f'      "name": "{plugin_name}",',
                f'      "source": "./plugins/{plugin_name}"',
                "    }",
                "  ]",
                "}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / "docs" / "maintainers" / "reality-audit.md").write_text(
        "\n".join(
            [
                "Root `skills/` is the canonical workflow-authoring surface.",
                ".claude-plugin/marketplace.json",
                "plugin packaging root",
                "uv tool install",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".agents").mkdir()
    (repo_root / ".claude").mkdir()
    os.symlink("../skills", repo_root / ".agents" / "skills")
    os.symlink("../skills", repo_root / ".claude" / "skills")
    os.symlink("../../skills", repo_root / "plugins" / plugin_name / "skills")


def test_audit_repo_accepts_expected_repo_shape(tmp_path: Path) -> None:
    _write_repo(tmp_path, "example-skills")

    findings = m.audit_repo(tmp_path, "example-skills")

    assert findings == []


def test_audit_repo_flags_missing_guidance_and_symlink_drift(tmp_path: Path) -> None:
    (tmp_path / "plugins" / "example-skills").mkdir(parents=True)
    (tmp_path / "README.md").write_text("plugins/\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "maintainers").mkdir(parents=True)
    (tmp_path / "docs" / "maintainers" / "reality-audit.md").write_text("", encoding="utf-8")

    findings = m.audit_repo(tmp_path, "example-skills")

    issue_ids = {finding.issue_id for finding in findings}
    assert "readme-missing-snippet" in issue_ids
    assert "agents-missing-snippet" in issue_ids
    assert "missing-path" in issue_ids
    assert "missing-symlink" in issue_ids
