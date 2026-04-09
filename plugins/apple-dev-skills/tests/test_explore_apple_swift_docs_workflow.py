from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/explore-apple-swift-docs/scripts/run_workflow.py"


def write_config(tmpdir: str, skill: str, settings: dict) -> None:
    target = Path(tmpdir) / skill / "customization.yaml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schemaVersion: 1", "isCustomized: true", "settings:"]
    for key, value in settings.items():
        if isinstance(value, bool):
            raw = "true" if value else "false"
        elif isinstance(value, int):
            raw = str(value)
        else:
            raw = f'"{value}"'
        lines.append(f"  {key}: {raw}")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


@contextmanager
def fake_open_in_path(script_body: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        bin_dir = Path(tmpdir) / "bin"
        bin_dir.mkdir()
        open_path = bin_dir / "open"
        open_path.write_text(script_body, encoding="utf-8")
        open_path.chmod(0o755)
        env = dict(os.environ)
        env["PATH"] = f"{bin_dir}:{env['PATH']}"
        yield env


class ExploreAppleSwiftDocsWorkflowTests(unittest.TestCase):
    def run_script(self, *args: str, env: dict | None = None) -> tuple[int, dict]:
        command_env = dict(env or os.environ)
        command_env.setdefault("UV_CACHE_DIR", str(Path(tempfile.gettempdir()) / "apple-dev-skills-uv-cache"))
        proc = subprocess.run(
            [str(SCRIPT), *args],
            cwd="/tmp",
            env=command_env,
            capture_output=True,
            text=True,
            check=False,
        )
        return proc.returncode, json.loads(proc.stdout)

    def test_explore_uses_xcode_mcp_by_default(self) -> None:
        code, payload = self.run_script("--mode", "explore", "--query", "SwiftUI", "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(payload["source_used"], "xcode-mcp-docs")
        self.assertEqual(payload["path_type"], "primary")

    def test_explore_obeys_preferred_source_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            status_file = Path(tmpdir) / "dash-status.json"
            status_file.write_text('{"health_ok": true, "schema_ok": true}\n', encoding="utf-8")
            code, payload = self.run_script(
                "--mode",
                "explore",
                "--query",
                "Swift",
                "--preferred-source",
                "dash",
                "--status-file",
                str(status_file),
                "--dry-run",
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["source_used"], "dash")

    def test_explore_falls_back_to_official_web_when_xcode_and_dash_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            env = dict(os.environ)
            env["APPLE_DEV_SKILLS_CONFIG_HOME"] = tmpdir
            write_config(tmpdir, "explore-apple-swift-docs", {"defaultSourceOrder": "xcode-mcp-docs,dash,official-web"})
            code, payload = self.run_script(
                "--mode",
                "explore",
                "--query",
                "Foundation",
                "--mcp-failure-reason",
                "session-missing",
                "--status-file",
                str(Path(tmpdir) / "missing-status.json"),
                "--dry-run",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["source_used"], "official-web")
            self.assertEqual(payload["path_type"], "fallback")

    def test_explore_keeps_snippets_enabled_by_default(self) -> None:
        code, payload = self.run_script("--mode", "explore", "--query", "Swift", "--dry-run")
        self.assertEqual(code, 0)
        self.assertTrue(payload["search_snippets_enabled"])
        self.assertGreater(len(payload["matches"][0].keys()), 3)

    def test_dash_install_uses_built_in_priority_by_default(self) -> None:
        code, payload = self.run_script(
            "--mode",
            "dash-install",
            "--docset-request",
            "Swift",
            "--dry-run",
        )
        self.assertEqual(code, 0)
        self.assertEqual(payload["selected_match"]["source"], "built_in")

    def test_dash_install_requires_explicit_approval(self) -> None:
        code, payload = self.run_script("--mode", "dash-install", "--docset-request", "Swift")
        self.assertEqual(code, 1)
        self.assertEqual(payload["status"], "blocked")

    def test_dash_install_launches_open_when_approved(self) -> None:
        script_body = """#!/bin/sh
printf '%s\n' "$1" > "${TMPDIR:-/tmp}/apple-dev-skills-open-arg.txt"
exit 0
"""
        with tempfile.TemporaryDirectory() as tmpdir, fake_open_in_path(script_body) as env:
            env["TMPDIR"] = tmpdir
            code, payload = self.run_script(
                "--mode",
                "dash-install",
                "--docset-request",
                "Swift",
                "--yes",
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "success")
            self.assertEqual(payload["install_result"]["returncode"], 0)
            self.assertTrue(payload["install_result"]["launched"])
            launched_url = Path(tmpdir, "apple-dev-skills-open-arg.txt").read_text(encoding="utf-8").strip()
            self.assertTrue(launched_url.startswith("dash-install://?"))

    def test_dash_install_handoffs_to_generation_when_no_match_exists(self) -> None:
        code, payload = self.run_script(
            "--mode",
            "dash-install",
            "--docset-request",
            "DefinitelyNotARealDocsetName",
            "--dry-run",
        )
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "handoff")
        self.assertIn("dash-generate", payload["next_step"])

    def test_dash_generate_returns_structured_guidance(self) -> None:
        code, payload = self.run_script("--mode", "dash-generate", "--docset-request", "Swift", "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "success")
        self.assertIn("guidance", payload)
        self.assertEqual(payload["source_path"], "automation-guidance")

    def test_dash_generate_uses_automated_policy_default(self) -> None:
        code, payload = self.run_script(
            "--mode",
            "dash-generate",
            "--docset-request",
            "Swift",
            "--dry-run",
        )
        self.assertEqual(code, 0)
        self.assertEqual(payload["path_type"], "primary")
        self.assertEqual(payload["guidance"]["policy"], "automate-stable")


if __name__ == "__main__":
    unittest.main()
