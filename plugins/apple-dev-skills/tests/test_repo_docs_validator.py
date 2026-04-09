from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / ".github/scripts/validate_repo_docs.sh"


class RepoDocsValidatorTests(unittest.TestCase):
    def test_repo_docs_validator_passes(self) -> None:
        proc = subprocess.run(
            ["bash", str(VALIDATOR)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr or proc.stdout)
        self.assertIn("All validation checks passed.", proc.stdout)


if __name__ == "__main__":
    unittest.main()
