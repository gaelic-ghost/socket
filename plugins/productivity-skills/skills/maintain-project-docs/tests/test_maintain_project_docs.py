from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/maintain-project-docs/scripts/maintain_project_docs.py"

spec = importlib.util.spec_from_file_location("maintain_project_docs", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["maintain_project_docs"] = module
spec.loader.exec_module(module)


class MaintainProjectDocsTests(unittest.TestCase):
    def test_select_workflows_preserves_canonical_order(self) -> None:
        selected, errors = module.select_workflows(None, None)
        self.assertEqual(errors, [])
        self.assertEqual([workflow.key for workflow in selected], ["readme", "contributing", "agents", "accessibility", "roadmap"])

    def test_select_workflows_reports_unknown_keys(self) -> None:
        selected, errors = module.select_workflows("readme,unknown", "roadmap")
        self.assertEqual([workflow.key for workflow in selected], ["readme"])
        self.assertEqual(errors, ["Unknown document workflow key: unknown"])

    def test_build_child_command_passes_ticket_flags_only_to_roadmap(self) -> None:
        args = module.parse_args(
            [
                "--project-root",
                "/tmp/demo",
                "--run-mode",
                "check-only",
                "--collect-source-tickets",
                "--collect-github-issues",
                "--github-repo",
                "owner/repo",
            ]
        )
        readme_command = module.build_child_command(args, module.DOCUMENT_WORKFLOWS[0], Path("/tmp/demo"))
        roadmap_command = module.build_child_command(args, module.DOCUMENT_WORKFLOWS[-1], Path("/tmp/demo"))
        self.assertNotIn("--collect-source-tickets", readme_command)
        self.assertIn("--collect-source-tickets", roadmap_command)
        self.assertIn("--collect-github-issues", roadmap_command)
        self.assertIn("owner/repo", roadmap_command)

    def test_responsibility_audit_flags_cross_doc_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "README.md").write_text("# Demo\n\n## Contribution Workflow\n\nDo all the things.\n", encoding="utf-8")
            (root / "ROADMAP.md").write_text("# Roadmap\n\n## Safety Boundaries\n\nDo not.\n", encoding="utf-8")
            issues = module.audit_responsibility_boundaries(root, module.DOCUMENT_WORKFLOWS)
            issue_ids = {issue["issue_id"] for issue in issues}
            self.assertIn("readme-contains-maintainer-workflow", issue_ids)
            self.assertIn("roadmap-contains-procedural-guidance", issue_ids)

    def test_script_reports_selection_errors_as_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-root",
                    tmpdir,
                    "--run-mode",
                    "check-only",
                    "--include",
                    "missing",
                    "--print-json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1)
            self.assertIn("Unknown document workflow key: missing", proc.stdout)
