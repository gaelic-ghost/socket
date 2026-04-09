from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_readme.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_readme", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_readme"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(project_root: Path, run_mode: str = "check-only", readme_path: Path | None = None):
    args = argparse.Namespace(
        project_root=str(project_root),
        readme_path=str(readme_path) if readme_path else None,
        run_mode=run_mode,
        json_out=None,
        md_out=None,
        print_json=False,
        print_md=False,
        fail_on_issues=False,
    )
    return MODULE.run_maintenance(args)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_valid_library_readme_has_no_findings(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-lib

A reusable Python package for demo purposes.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [License](#license)

## Overview

demo-lib provides reusable helpers for the surrounding application code.

### Motivation

It keeps common Python behaviors in one package so downstream code stays simpler.

## Setup

```bash
uv sync
```

## Usage

Import the package from Python code that needs the shared helpers.

## Development

Make changes locally and keep the package behavior focused and testable.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path)
    assert report["schema_violations"] == []
    assert report["command_integrity_issues"] == []
    assert report["content_quality_issues"] == []
    assert report["errors"] == []


def test_valid_cli_readme_has_no_findings(tmp_path: Path) -> None:
    write(
        tmp_path / "package.json",
        json.dumps({"name": "demo-cli", "bin": {"demo": "./bin/demo.js"}}, indent=2),
    )
    write(
        tmp_path / "README.md",
        """
# demo-cli

A command-line tool for demo workflows.

## Overview

demo-cli wraps a focused command surface for local developer tasks.

### Motivation

It keeps common commands easy to discover and run from one CLI entrypoint.

## Setup

```bash
pnpm install
```

## Usage

```bash
pnpm demo --help
```

## Development

Iterate on command behavior locally and keep examples current with the shipped CLI.

## Verification

```bash
pnpm test
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path)
    assert report["profile_assignment"]["selected_profile"] == "cli-tool"
    assert report["schema_violations"] == []
    assert report["errors"] == []


def test_valid_app_service_readme_has_no_findings(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-service"
version = "0.1.0"
dependencies = ["fastapi", "uvicorn"]
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-service

A small API service for demo requests.

## Overview

demo-service exposes a local API surface for development and testing.

### Motivation

It provides a stable local service shell for integrating and verifying API behavior.

## Setup

```bash
uv sync
```

## Usage

Run the service locally and send requests to its documented endpoints.

## Development

Keep local changes small and verify that handler behavior still matches the intended API.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path)
    assert report["profile_assignment"]["selected_profile"] == "app-service"
    assert report["schema_violations"] == []
    assert report["errors"] == []


def test_valid_monorepo_readme_has_no_findings(tmp_path: Path) -> None:
    write(tmp_path / "pnpm-workspace.yaml", "packages:\n  - apps/*\n  - packages/*\n")
    write(
        tmp_path / "README.md",
        """
# demo-workspace

A multi-package workspace for demo apps and packages.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Verification](#verification)
- [License](#license)
- [Repository Layout](#repository-layout)

## Overview

demo-workspace groups related apps and packages in one repository.

### Motivation

It keeps shared tooling and changes coordinated across packages that ship together.

## Setup

```bash
pnpm install
```

## Usage

Use the workspace commands from the repository root.

## Development

Work within the relevant package or app while keeping shared workspace tooling green.

## Verification

```bash
pnpm test
```

## License

See [LICENSE](./LICENSE).

## Repository Layout

- `apps/` for applications
- `packages/` for shared packages
""".strip(),
    )
    report, _md = run(tmp_path)
    assert report["profile_assignment"]["selected_profile"] == "monorepo-workspace"
    assert report["schema_violations"] == []
    assert report["errors"] == []


def test_missing_motivation_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-lib

A reusable Python package for demo purposes.

## Overview

demo-lib provides reusable helpers for the surrounding application code.

## Setup

```bash
uv sync
```

## Usage

Import the package from Python code that needs the shared helpers.

## Development

Make changes locally.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-motivation-subsection" in issue_ids


def test_incompatible_command_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-lib

A reusable Python package for demo purposes.

## Overview

demo-lib provides reusable helpers for the surrounding application code.

### Motivation

It keeps Python-only reuse in one place.

## Setup

```bash
pnpm install
```

## Usage

Import the package from Python code that needs the shared helpers.

## Development

Make changes locally.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path)
    assert report["command_integrity_issues"]


def test_missing_required_sections_are_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "package.json",
        json.dumps({"name": "demo-cli", "bin": {"demo": "./bin/demo.js"}}, indent=2),
    )
    write(
        tmp_path / "README.md",
        """
# demo-cli

A command-line tool for demo workflows.

## Overview

demo-cli wraps a focused command surface for local developer tasks.
""".strip(),
    )
    report, _md = run(tmp_path)
    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-motivation-subsection" in issue_ids
    assert "missing-section-setup" in issue_ids
    assert "missing-section-usage" in issue_ids
    assert "missing-section-development" in issue_ids
    assert "missing-section-verification" in issue_ids
    assert "missing-section-license" in issue_ids


def test_ambiguous_profile_detection_is_reported(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-hybrid"
version = "0.1.0"
dependencies = ["fastapi"]

[project.scripts]
demo = "demo:main"
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-hybrid

A hybrid repo for demo purposes.

## Overview

demo-hybrid mixes command and service entrypoints.

### Motivation

It supports both a CLI entrypoint and a local API shell.

## Setup

```bash
uv sync
```

## Usage

Run the command or the service entrypoint depending on the workflow.

## Development

Keep both surfaces consistent while changing shared code.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path)
    assert report["profile_assignment"]["ambiguous"] is True
    issue_ids = {issue["issue_id"] for issue in report["content_quality_issues"]}
    assert "ambiguous-profile-detection" in issue_ids


def test_skills_repo_is_rejected(tmp_path: Path) -> None:
    write(tmp_path / ".codex-plugin" / "plugin.json", '{"name":"demo"}')
    write(tmp_path / "skills" / "demo-skill" / "SKILL.md", "---\nname: demo-skill\n---\n")
    write(tmp_path / "README.md", "# demo\n\ntext\n")
    report, _md = run(tmp_path)
    assert report["errors"]
    assert "maintain-skills-readme" in report["errors"][0]


def test_apply_mode_repairs_readme_and_only_touches_readme(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    write(
        pyproject,
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    original_pyproject = pyproject.read_text(encoding="utf-8")
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-lib

A reusable Python package for demo purposes.

## Overview

demo-lib provides reusable helpers for the surrounding application code.
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated_readme = readme.read_text(encoding="utf-8")
    assert report["fixes_applied"]
    assert "### Motivation" in updated_readme
    assert "## Setup" in updated_readme
    assert "## Verification" in updated_readme
    assert "## API Notes" in updated_readme
    assert report["post_fix_status"] == []
    assert pyproject.read_text(encoding="utf-8") == original_pyproject


def test_apply_mode_preserves_rich_preamble_content(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-lib

A reusable Python package for demo purposes.

![CI](https://example.com/badge.svg)

> Early access package. Interfaces may still evolve.

Additional intro context that should stay in the preamble.

## Overview

demo-lib provides reusable helpers for the surrounding application code.
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated_readme = readme.read_text(encoding="utf-8")
    assert report["fixes_applied"]
    assert "![CI](https://example.com/badge.svg)" in updated_readme
    assert "> Early access package. Interfaces may still evolve." in updated_readme
    assert "Additional intro context that should stay in the preamble." in updated_readme
    assert updated_readme.index("![CI](https://example.com/badge.svg)") < updated_readme.index("## Overview")
    assert updated_readme.index("> Early access package. Interfaces may still evolve.") < updated_readme.index("## Overview")


def test_apply_mode_adds_library_profile_section_when_profile_is_clear(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-lib

A reusable Python package for demo purposes.

## Overview

demo-lib provides reusable helpers for the surrounding application code.

### Motivation

It keeps common Python behaviors in one package so downstream code stays simpler.

## Setup

```bash
uv sync
```

## Usage

Import the package from Python code that needs the shared helpers.

## Development

Make changes locally and keep the package behavior focused and testable.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["profile_assignment"]["selected_profile"] == "library-package"
    assert "## API Notes" in updated
    assert updated.index("## API Notes") > updated.index("## License")


def test_apply_mode_adds_cli_profile_section_when_profile_is_clear(tmp_path: Path) -> None:
    write(
        tmp_path / "package.json",
        json.dumps({"name": "demo-cli", "bin": {"demo": "./bin/demo.js"}}, indent=2),
    )
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-cli

A command-line tool for demo workflows.

## Overview

demo-cli wraps a focused command surface for local developer tasks.

### Motivation

It keeps common commands easy to discover and run from one CLI entrypoint.

## Setup

```bash
pnpm install
```

## Usage

```bash
pnpm demo --help
```

## Development

Iterate on command behavior locally and keep examples current with the shipped CLI.

## Verification

```bash
pnpm test
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["profile_assignment"]["selected_profile"] == "cli-tool"
    assert "## Command Reference" in updated


def test_apply_mode_adds_app_service_profile_section_when_profile_is_clear(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-service"
version = "0.1.0"
dependencies = ["fastapi", "uvicorn"]
""".strip(),
    )
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-service

A small API service for demo requests.

## Overview

demo-service exposes a local API surface for development and testing.

### Motivation

It provides a stable local service shell for integrating and verifying API behavior.

## Setup

```bash
uv sync
```

## Usage

Run the service locally and send requests to its documented endpoints.

## Development

Keep local changes small and verify that handler behavior still matches the intended API.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["profile_assignment"]["selected_profile"] == "app-service"
    assert "## Configuration" in updated


def test_apply_mode_adds_monorepo_profile_section_when_profile_is_clear(tmp_path: Path) -> None:
    write(tmp_path / "pnpm-workspace.yaml", "packages:\n  - apps/*\n  - packages/*\n")
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-workspace

A multi-package workspace for demo apps and packages.

## Overview

demo-workspace groups related apps and packages in one repository.

### Motivation

It keeps shared tooling and changes coordinated across packages that ship together.

## Setup

```bash
pnpm install
```

## Usage

Use the workspace commands from the repository root.

## Development

Work within the relevant package or app while keeping shared workspace tooling green.

## Verification

```bash
pnpm test
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["profile_assignment"]["selected_profile"] == "monorepo-workspace"
    assert "## Repository Layout" in updated


def test_apply_mode_preserves_existing_profile_section_without_duplication(tmp_path: Path) -> None:
    write(
        tmp_path / "package.json",
        json.dumps({"name": "demo-cli", "bin": {"demo": "./bin/demo.js"}}, indent=2),
    )
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-cli

A command-line tool for demo workflows.

## Overview

demo-cli wraps a focused command surface for local developer tasks.

### Motivation

It keeps common commands easy to discover and run from one CLI entrypoint.

## Setup

```bash
pnpm install
```

## Usage

```bash
pnpm demo --help
```

## Development

Iterate on command behavior locally and keep examples current with the shipped CLI.

## Verification

```bash
pnpm test
```

## License

See [LICENSE](./LICENSE).

## Command Reference

- `demo --help`
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["profile_assignment"]["selected_profile"] == "cli-tool"
    assert updated.count("## Command Reference") == 1
    assert "- `demo --help`" in updated


def test_apply_mode_does_not_add_profile_section_when_profile_is_ambiguous(tmp_path: Path) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-hybrid"
version = "0.1.0"
dependencies = ["fastapi"]

[project.scripts]
demo = "demo:main"
""".strip(),
    )
    readme = tmp_path / "README.md"
    write(
        readme,
        """
# demo-hybrid

A hybrid repo for demo purposes.

## Overview

demo-hybrid mixes command and service entrypoints.

### Motivation

It supports both a CLI entrypoint and a local API shell.

## Setup

```bash
uv sync
```

## Usage

Run the command or the service entrypoint depending on the workflow.

## Development

Keep both surfaces consistent while changing shared code.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    report, _md = run(tmp_path, run_mode="apply")
    updated = readme.read_text(encoding="utf-8")
    assert report["profile_assignment"]["ambiguous"] is True
    assert "## Command Reference" not in updated
    assert "## Configuration" not in updated
def test_main_prints_no_findings_for_clean_readme(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-lib

A reusable Python package for demo purposes.

## Overview

demo-lib provides reusable helpers for the surrounding application code.

### Motivation

It keeps common Python behaviors in one package so downstream code stays simpler.

## Setup

```bash
uv sync
```

## Usage

Import the package from Python code that needs the shared helpers.

## Development

Make changes locally and keep the package behavior focused and testable.

## Verification

```bash
uv run pytest
```

## License

See [LICENSE](./LICENSE).
""".strip(),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "maintain_project_readme.py",
            "--project-root",
            str(tmp_path),
            "--run-mode",
            "check-only",
        ],
    )
    exit_code = MODULE.main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "No findings.\n"


def test_main_respects_fail_on_issues_exit_code(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    write(
        tmp_path / "pyproject.toml",
        """
[project]
name = "demo-lib"
version = "0.1.0"
""".strip(),
    )
    write(
        tmp_path / "README.md",
        """
# demo-lib

A reusable Python package for demo purposes.

## Overview

demo-lib provides reusable helpers for the surrounding application code.
""".strip(),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "maintain_project_readme.py",
            "--project-root",
            str(tmp_path),
            "--run-mode",
            "check-only",
            "--fail-on-issues",
        ],
    )
    exit_code = MODULE.main()
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "## Schema Violations" in captured.out


def test_main_rejects_skills_repo_with_nonzero_exit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    write(tmp_path / ".codex-plugin" / "plugin.json", '{"name":"demo"}')
    write(tmp_path / "skills" / "demo-skill" / "SKILL.md", "---\nname: demo-skill\n---\n")
    write(tmp_path / "README.md", "# demo\n\ntext\n")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "maintain_project_readme.py",
            "--project-root",
            str(tmp_path),
            "--run-mode",
            "check-only",
        ],
    )
    exit_code = MODULE.main()
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "maintain-skills-readme" in captured.out
