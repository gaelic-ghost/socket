from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parent.parent / "scripts" / "audit_xcode_plugin_compatibility.py"
SPEC = importlib.util.spec_from_file_location("audit_xcode_plugin_compatibility", MODULE_PATH)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(tmp_path: Path) -> Path:
    marketplace = {
        "plugins": [
            {
                "name": "skills-only",
                "source": {"source": "local", "path": "./plugins/skills-only"},
                "policy": {"installation": "AVAILABLE"},
            },
            {
                "name": "mixed",
                "source": {"source": "local", "path": "./plugins/mixed"},
                "policy": {"installation": "AVAILABLE"},
            },
            {
                "name": "remote",
                "source": {"source": "url", "url": "https://example.com/remote.git", "ref": "v1.0.0"},
                "policy": {"installation": "AVAILABLE"},
            },
        ]
    }
    write(tmp_path / ".agents/plugins/marketplace.json", json.dumps(marketplace))
    for name in ("skills-only", "mixed"):
        write(
            tmp_path / f"plugins/{name}/.codex-plugin/plugin.json",
            json.dumps({"name": name, "skills": "./skills/", "mcpServers": "./.mcp.json"} if name == "mixed" else {"name": name, "skills": "./skills/"}),
        )
        write(tmp_path / f"plugins/{name}/skills/example/SKILL.md", "---\nname: example\ndescription: Example.\n---\n")
    write(
        tmp_path / "plugins/mixed/.mcp.json",
        json.dumps({"mcpServers": {"local": {"command": "uv", "cwd": "../../mcp"}}}),
    )
    write(tmp_path / "plugins/mixed/hooks/hooks.json", "{}")
    return tmp_path


def test_source_inventory_classifies_skill_only_mixed_and_remote(tmp_path: Path) -> None:
    report = audit.build_report(make_repo(tmp_path))

    by_name = {item.name: item for item in report}
    assert by_name["skills-only"].xcode_internal_plugin.status == "likely"
    assert by_name["mixed"].xcode_internal_plugin.status == "partial"
    assert by_name["mixed"].mcp_servers == ("local",)
    assert len(by_name["mixed"].mcp_risks) == 2
    assert by_name["remote"].xcode_internal_plugin.status == "unknown"


def test_markdown_report_names_three_xcode_targets(tmp_path: Path) -> None:
    markdown = audit.render_markdown(audit.build_report(make_repo(tmp_path)))

    assert "# Socket Xcode Plug-in Compatibility Audit" in markdown
    assert "Xcode internal" in markdown
    assert "Xcode Codex" in markdown
    assert "External agent" in markdown
    assert "Runtime-proof queue" in markdown


def test_real_socket_marketplace_is_fully_accounted_for() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    report = audit.build_report(repo_root)
    marketplace = json.loads((repo_root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))

    assert len(report) == len(marketplace["plugins"])
    assert len({item.name for item in report}) == len(report)
    assert all(item.xcode_internal_plugin.status in {"likely", "partial", "blocked", "unknown"} for item in report)
