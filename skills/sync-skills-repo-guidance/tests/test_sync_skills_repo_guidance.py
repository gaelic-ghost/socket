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
                "OpenAI's current documented Codex plugin system is too restricted to provide proper repo-private plugin scoping.",
                "npx skills add gaelic-ghost/agent-plugin-skills --all",
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
                "Root `skills/` is the canonical authored and exported surface",
                "Do not recreate nested plugin directories",
                "Do not recreate `skills/install-plugin-to-socket` or `skills/validate-plugin-install-surfaces`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo_root / ".gitignore").write_text(".claude/settings.local.json\n", encoding="utf-8")
    (repo_root / "docs" / "maintainers" / "reality-audit.md").write_text(
        "\n".join(
            [
                "This repository does not track a nested plugin directory for itself.",
                "This repository does not ship `install-plugin-to-socket`.",
                "This repository does not ship `validate-plugin-install-surfaces`.",
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
    (tmp_path / "README.md").write_text(".agents/plugins/marketplace.json\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("", encoding="utf-8")
    (tmp_path / "docs" / "maintainers").mkdir(parents=True)
    (tmp_path / "docs" / "maintainers" / "reality-audit.md").write_text("", encoding="utf-8")

    findings = m.audit_repo(tmp_path, "example-skills")

    issue_ids = {finding.issue_id for finding in findings}
    assert "readme-forbidden-snippet" in issue_ids
    assert "agents-missing-snippet" in issue_ids
    assert "missing-symlink" in issue_ids
    assert "forbidden-path" in issue_ids
