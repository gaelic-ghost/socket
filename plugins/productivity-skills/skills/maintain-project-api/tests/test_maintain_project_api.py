from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "maintain_project_api.py"
SPEC = importlib.util.spec_from_file_location("maintain_project_api", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules["maintain_project_api"] = MODULE
SPEC.loader.exec_module(MODULE)


def run(project_root: Path, run_mode: str = "check-only", api_path: Path | None = None):
    args = argparse.Namespace(
        project_root=str(project_root),
        api_path=str(api_path) if api_path else None,
        run_mode=run_mode,
        config=None,
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


VALID_API = """
# API Reference for demo-project

Use this reference to understand the public API surface, how to call it, what it returns, and how to verify behavior locally.

## Table of Contents

- [Overview](#overview)
- [API Surface](#api-surface)
- [Authentication and Access](#authentication-and-access)
- [Requests and Responses](#requests-and-responses)
- [Errors](#errors)
- [Versioning and Compatibility](#versioning-and-compatibility)
- [Local Development and Verification](#local-development-and-verification)
- [Support and Ownership](#support-and-ownership)

## Overview

### Who This API Is For

This API is for local tools and maintainers that need to inspect demo-project state from automated checks.

### Stability Status

The API is stable for documented fields and experimental for any field explicitly marked internal.

## API Surface

### Entry Points

The public entry point is `GET /v1/status`.

### Protocols and Transports

The API is exposed over local HTTP and returns JSON.

## Authentication and Access

### Credentials

Local development calls do not require credentials.

### Permissions

The caller must be able to reach the local development server.

## Requests and Responses

### Request Shape

`GET /v1/status` accepts no request body.

### Response Shape

The response contains a `status` string and an `updatedAt` timestamp.

### Data Models

`status` is one of `ok`, `degraded`, or `offline`.

## Errors

### Error Shape

Errors return a JSON object with `code`, `message`, and `requestId`.

### Common Failure Modes

Connection failures usually mean the local server is not running.

## Versioning and Compatibility

### Supported Versions

The documented surface covers version `v1`.

### Breaking Changes

Breaking changes require an explicit migration note in this file.

## Local Development and Verification

### Runtime Configuration

The local API uses the default development server configuration.

### Verification

```bash
uv run pytest
```

## Support and Ownership

Open an issue in this repository when the documented contract does not match the implementation.
""".strip()


def test_valid_api_file_has_no_findings(tmp_path: Path) -> None:
    write(tmp_path / "API.md", VALID_API)

    report, markdown = run(tmp_path)

    assert report["schema_violations"] == []
    assert report["command_integrity_issues"] == []
    assert report["content_quality_issues"] == []
    assert report["errors"] == []
    assert markdown == "No findings."


def test_apply_creates_api_from_template_when_missing(tmp_path: Path) -> None:
    report, _markdown = run(tmp_path, run_mode="apply")
    created = (tmp_path / "API.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "# API Reference for" in created
    assert "## Table of Contents" in created
    assert "## API Surface" in created
    assert "## Local Development and Verification" in created
    assert "### Runtime Configuration" in created
    assert "### Verification" in created


def test_apply_normalizes_structure_and_aliases(tmp_path: Path) -> None:
    write(
        tmp_path / "API.md",
        """
# API Reference for demo-project

Short reference.

## Overview

### Audience

This API is for local tools.

### Status

Stable for documented fields.

## Endpoints

### Routes

`GET /v1/status`

### Protocols

Local HTTP.

## Authentication

### Secrets

No token is required.

### Scopes

Local network access is required.

## Schemas

### Requests

No body is required.

### Responses

JSON is returned.

### Models

The response has a `status` field.

## Error Handling

### Error Format

Errors are JSON objects.

### Failure Modes

The server may be offline.

## Compatibility

### Versions

Version `v1` is supported.

### Migration Notes

Breaking changes are documented here.

## Local Setup

### Runtime Config

Use the development server defaults.

### Validation

```bash
pnpm test
```

## Support

Open an issue.
""".strip(),
    )

    report, _markdown = run(tmp_path, run_mode="apply")
    updated = (tmp_path / "API.md").read_text(encoding="utf-8")

    assert report["fixes_applied"]
    assert "## Table of Contents" in updated
    assert "## API Surface" in updated
    assert "## Endpoints" not in updated
    assert "## Authentication and Access" in updated
    assert "## Local Setup" not in updated
    assert "### Audience" not in updated
    assert "### Who This API Is For" in updated
    assert "### Runtime Configuration" in updated
    assert report["schema_violations"] == []


def test_check_only_flags_missing_table_of_contents(tmp_path: Path) -> None:
    write(
        tmp_path / "API.md",
        VALID_API.replace(
            """## Table of Contents

- [Overview](#overview)
- [API Surface](#api-surface)
- [Authentication and Access](#authentication-and-access)
- [Requests and Responses](#requests-and-responses)
- [Errors](#errors)
- [Versioning and Compatibility](#versioning-and-compatibility)
- [Local Development and Verification](#local-development-and-verification)
- [Support and Ownership](#support-and-ownership)

""",
            "",
        ),
    )

    report, _markdown = run(tmp_path, run_mode="check-only")

    issue_ids = {issue["issue_id"] for issue in report["schema_violations"]}
    assert "missing-table-of-contents" in issue_ids


def test_check_only_flags_verification_fence_without_info_string(tmp_path: Path) -> None:
    write(
        tmp_path / "API.md",
        VALID_API.replace("```bash\nuv run pytest\n```", "```\nuv run pytest\n```"),
    )

    report, _markdown = run(tmp_path, run_mode="check-only")

    issue_ids = {issue["issue_id"] for issue in report["command_integrity_issues"]}
    assert any(issue_id.startswith("missing-code-fence-info-string-") for issue_id in issue_ids)
