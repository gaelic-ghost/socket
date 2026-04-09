from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_repo_metadata import run


def test_repo_metadata_validation_passes() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    findings = run(repo_root)
    assert findings == []
