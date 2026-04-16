from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DOC = ROOT / "docs/maintainers/customization-consolidation-review.md"
ROADMAP = ROOT / "ROADMAP.md"
TEMPLATE_PATHS = sorted(ROOT.glob("skills/*/references/customization.template.yaml"))
FLOW_PATHS = sorted(ROOT.glob("skills/*/references/customization-flow.md"))
SCRIPT_PATHS = sorted(ROOT.glob("skills/*/scripts/customization_config.py"))


def _count_template_knobs() -> int:
    count = 0
    for path in TEMPLATE_PATHS:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("  ") and ":" in line:
                count += 1
    return count


def _count_statuses() -> tuple[int, int]:
    runtime_enforced = 0
    policy_only = 0
    row_pattern = re.compile(r"^\| `[^`]+` \| `[^`]*` \| `([^`]+)` \|")

    for path in FLOW_PATHS:
        for line in path.read_text(encoding="utf-8").splitlines():
            match = row_pattern.match(line)
            if not match:
                continue
            status = match.group(1)
            if status == "runtime-enforced":
                runtime_enforced += 1
            elif status == "policy-only":
                policy_only += 1
            else:
                raise AssertionError(f"Unexpected customization status {status!r} in {path}")

    return runtime_enforced, policy_only


class CustomizationConsolidationReviewTests(unittest.TestCase):
    def test_review_doc_exists_and_has_key_sections(self) -> None:
        text = REVIEW_DOC.read_text(encoding="utf-8")

        for section in (
            "## Current State Summary",
            "## Decision",
            "## Knob Classification",
            "## Sync Skill Simplification Decision",
            "## Shared Helper Decision",
            "## Follow-Up Plan",
            "## Outcome",
        ):
            with self.subTest(section=section):
                self.assertIn(section, text)

    def test_review_doc_counts_match_live_customization_surface(self) -> None:
        text = REVIEW_DOC.read_text(encoding="utf-8")
        template_count = len(TEMPLATE_PATHS)
        script_count = len(SCRIPT_PATHS)
        knob_count = _count_template_knobs()
        runtime_enforced, policy_only = _count_statuses()

        self.assertEqual(template_count, 16)
        self.assertEqual(script_count, 16)
        self.assertEqual(knob_count, 21)
        self.assertEqual(runtime_enforced, 20)
        self.assertEqual(policy_only, 1)

        self.assertIn(f"The active skill surface ships `{template_count}` separate `references/customization.template.yaml` files.", text)
        self.assertIn(f"The active skill surface ships `{script_count}` separate `scripts/customization_config.py` entrypoints.", text)
        self.assertIn(f"The current templates expose `{knob_count}` knobs total:", text)
        self.assertIn(f"- `{runtime_enforced}` are documented as `runtime-enforced`", text)
        policy_line = (
            f"- `{policy_only}` is documented as `policy-only`"
            if policy_only == 1
            else f"- `{policy_only}` are documented as `policy-only`"
        )
        self.assertIn(policy_line, text)

    def test_review_doc_records_sync_write_mode_decision(self) -> None:
        text = REVIEW_DOC.read_text(encoding="utf-8")

        self.assertIn("implemented replacement: `writeMode`", text)
        for value in (
            "`sync-if-needed`",
            "`create-missing-only`",
            "`append-existing-only`",
            "`report-only`",
        ):
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_roadmap_marks_review_and_implementation_done(self) -> None:
        text = ROADMAP.read_text(encoding="utf-8")

        self.assertIn("Completed Milestones 22 and 23", text)
        self.assertIn("customization consolidation review", text)
        self.assertIn("See `docs/maintainers/customization-consolidation-review.md`.", text)
        self.assertIn("Completed Milestones 30 through 36", text)
        self.assertIn("shrinking the customization surface", text)


if __name__ == "__main__":
    unittest.main()
