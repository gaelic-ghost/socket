from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "validate_plugin_install_surfaces.py"
    spec = importlib.util.spec_from_file_location("validate_plugin_install_surfaces", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


def make_valid_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "agent-plugin-skills"
    skill_dir = repo / "skills" / "example-skill"
    plugin_root = repo / "plugins" / "agent-plugin-skills"
    (repo / ".agents" / "plugins").mkdir(parents=True)
    (repo / ".agents").mkdir(exist_ok=True)
    (repo / ".claude").mkdir(exist_ok=True)
    (skill_dir / "agents").mkdir(parents=True)
    (plugin_root / ".codex-plugin").mkdir(parents=True)
    (plugin_root / ".claude-plugin").mkdir(parents=True)
    repo.mkdir(exist_ok=True)

    (skill_dir / "SKILL.md").write_text(
        "---\nname: example-skill\ndescription: Example skill.\n---\n",
        encoding="utf-8",
    )
    (skill_dir / "agents" / "openai.yaml").write_text(
        "interface:\n  display_name: Example Skill\n  short_description: Example.\n  default_prompt: Use $example-skill.\n",
        encoding="utf-8",
    )
    (plugin_root / ".codex-plugin" / "plugin.json").write_text(
        '{"name":"agent-plugin-skills","version":"0.1.0","description":"Example."}',
        encoding="utf-8",
    )
    (plugin_root / ".claude-plugin" / "plugin.json").write_text(
        '{"name":"agent-plugin-skills","version":"0.1.0","description":"Example."}',
        encoding="utf-8",
    )
    (repo / ".agents" / "plugins" / "marketplace.json").write_text(
        '{\n  "plugins": [\n    {\n      "name": "agent-plugin-skills",\n      "source": {"path": "./plugins/agent-plugin-skills"}\n    }\n  ]\n}\n',
        encoding="utf-8",
    )
    (repo / "README.md").write_text(
        "# agent-plugin-skills\n\n"
        "Maintainer repo.\n\n"
        "## Install\n\n"
        "### Codex Plugin\n\n"
        "Use the plugin in `plugins/agent-plugin-skills/.codex-plugin/plugin.json`.\n\n"
        "### Claude Code Plugin\n\n"
        "Use the plugin in `plugins/agent-plugin-skills/.claude-plugin/plugin.json`.\n\n"
        "### Vercel `skills` CLI\n\n"
        "```bash\n"
        "npx skills add gaelic-ghost/agent-plugin-skills --skill example-skill\n"
        "```\n",
        encoding="utf-8",
    )
    (repo / ".agents" / "skills").symlink_to("../skills")
    (repo / ".claude" / "skills").symlink_to("../skills")
    (plugin_root / "skills").symlink_to("../../skills")
    return repo


def test_audit_valid_repo_has_no_findings(tmp_path: Path) -> None:
    repo = make_valid_repo(tmp_path)

    skill_dirs = m.canonical_skill_dirs(repo)
    plugin_dirs = m.plugin_roots(repo)

    metadata = []
    for skill_dir in skill_dirs:
        metadata.extend(m.audit_skill_metadata(repo, skill_dir))
    for plugin_root in plugin_dirs:
        metadata.extend(m.audit_plugin_metadata(repo, plugin_root))
    metadata.extend(m.audit_marketplace(repo, plugin_dirs))
    install_findings = m.audit_install_surfaces(repo, skill_dirs, plugin_dirs)
    mirror_findings = m.audit_mirrors(repo, "agent-plugin-skills")

    assert metadata == []
    assert install_findings == []
    assert mirror_findings == []


def test_detects_missing_openai_yaml_and_bad_skill_reference(tmp_path: Path) -> None:
    repo = make_valid_repo(tmp_path)
    (repo / "skills" / "example-skill" / "agents" / "openai.yaml").unlink()
    (repo / "README.md").write_text(
        "# agent-plugin-skills\n\n## Install\n\n```bash\nnpx skills add gaelic-ghost/agent-plugin-skills --skill missing-skill\n```\n",
        encoding="utf-8",
    )

    skill_dirs = m.canonical_skill_dirs(repo)
    metadata = []
    for skill_dir in skill_dirs:
        metadata.extend(m.audit_skill_metadata(repo, skill_dir))
    install_findings = m.audit_install_surfaces(repo, skill_dirs, m.plugin_roots(repo))

    issue_ids = {item.issue_id for item in metadata + install_findings}
    assert "missing-openai-yaml" in issue_ids
    assert "readme-install-missing-skill" in issue_ids


def test_detects_bad_marketplace_path_and_wrong_symlink(tmp_path: Path) -> None:
    repo = make_valid_repo(tmp_path)
    (repo / ".agents" / "plugins" / "marketplace.json").write_text(
        '{\n  "plugins": [\n    {\n      "name": "agent-plugin-skills",\n      "source": {"path": "plugins/agent-plugin-skills"}\n    }\n  ]\n}\n',
        encoding="utf-8",
    )
    (repo / ".claude" / "skills").unlink()
    (repo / ".claude" / "skills").symlink_to("../wrong-skills")

    metadata = m.audit_marketplace(repo, m.plugin_roots(repo))
    mirrors = m.audit_mirrors(repo, "agent-plugin-skills")

    issue_ids = {item.issue_id for item in metadata + mirrors}
    assert "marketplace-nonrelative-source-path" in issue_ids
    assert "wrong-symlink-target" in issue_ids


def test_detects_marketplace_root_source_path_as_invalid(tmp_path: Path) -> None:
    repo = make_valid_repo(tmp_path)
    (repo / ".agents" / "plugins" / "marketplace.json").write_text(
        '{\n  "plugins": [\n    {\n      "name": "agent-plugin-skills",\n      "source": {"path": "./"}\n    }\n  ]\n}\n',
        encoding="utf-8",
    )

    metadata = m.audit_marketplace(repo, m.plugin_roots(repo))
    issue_ids = {item.issue_id for item in metadata}

    assert "marketplace-empty-relative-source-path" in issue_ids
