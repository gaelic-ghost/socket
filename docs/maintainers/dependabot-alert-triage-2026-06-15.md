# Dependabot Alert Triage, 2026-06-15

This note records the initial triage for the 46 open Dependabot alerts reported
after GitHub Dependabot security updates were enabled for `gaelic-ghost/socket`.

Source: GitHub Dependabot alerts API for `gaelic-ghost/socket`, queried on
2026-06-15.

## Summary

| Priority | Scope | Count | Action |
| --- | --- | ---: | --- |
| P0 | `plugins/cardhop-app/mcp/uv.lock` and `plugins/things-app/mcp/uv.lock` | 38 | Upgrade and validate the bundled MCP server dependencies first. |
| P1 | Plugin and skill lockfiles with dev/test or low-risk runtime alerts | 8 | Upgrade after MCP locks or in the same dependency-refresh pass if quick. |

Severity totals:

| Severity | Count |
| --- | ---: |
| Critical | 4 |
| High | 10 |
| Medium | 25 |
| Low | 7 |

All current alerts are Python package alerts from `uv.lock` files.

## P0: Bundled MCP Server Lockfiles

These alerts affect the bundled local MCP servers for Cardhop and Things:

- `plugins/cardhop-app/mcp/uv.lock`: 19 alerts
- `plugins/things-app/mcp/uv.lock`: 19 alerts

Both MCP server projects directly require `fastmcp>=3.0.2`. The alerts include
direct `fastmcp` advisories and transitive dependency advisories pulled through
the local FastMCP server stack.

Treat these first because they affect executable MCP server surfaces, not only
developer test tooling. The servers are local tools rather than public internet
services, which lowers exposure, but Things has HTTP smoke tooling and handles
task-update authorization paths, so the safer assumption is to refresh the MCP
dependency set promptly.

Patch targets identified by Dependabot:

| Package | Minimum patched version | Highest severity seen | Notes |
| --- | --- | --- | --- |
| `fastmcp` | `3.2.0` | Critical | Includes SSRF/path traversal and OAuth proxy advisories. |
| `authlib` | `1.6.12` | Critical | Multiple OIDC/JWS/JWE/OAuth advisories. |
| `PyJWT` | `2.12.0` | High | Unknown `crit` header handling. |
| `python-multipart` | `0.0.27` | High | Multipart denial-of-service advisories. |
| `starlette` | `1.0.1` | Medium | Host header validation issue. |
| `idna` | `3.15` | Medium | IDNA crafted-input bypass issue. |
| `python-dotenv` | `1.2.2` | Medium | Symlink-following overwrite issue. |
| `cryptography` | `46.0.7` | Medium | Includes medium and low cryptography advisories. |
| `Pygments` | `2.20.0` | Low | ReDoS in GUID matching. |
| `pytest` | `9.0.3` | Medium | Development-scope tmpdir handling advisory. |

Recommended remediation slice:

1. From `plugins/cardhop-app/mcp`, refresh the lockfile with `uv lock --upgrade`.
2. Run that MCP server's local validation from its own directory:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
3. From `plugins/things-app/mcp`, refresh the lockfile with `uv lock --upgrade`.
4. Run that MCP server's local validation from its own directory:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
5. Re-query open Dependabot alerts. If transitive packages remain vulnerable,
   decide whether to add targeted lower bounds in the MCP `pyproject.toml` files
   or wait for upstream FastMCP dependency constraints.

## P1: Remaining Plugin And Skill Lockfiles

These alerts are lower priority because they are development-scope test tooling
or low-severity runtime transitive dependencies in non-server plugin lockfiles:

| Manifest | Alerts | Packages |
| --- | ---: | --- |
| `plugins/agent-plugin-skills/uv.lock` | 1 | `pytest` |
| `plugins/apple-dev-skills/uv.lock` | 2 | `Pygments`, `pytest` |
| `plugins/productivity-skills/uv.lock` | 2 | `Pygments`, `pytest` |
| `plugins/python-skills/uv.lock` | 2 | `Pygments`, `pytest` |
| `plugins/things-app/uv.lock` | 1 | `pytest` |

Recommended remediation slice:

1. Refresh each affected lockfile with `uv lock --upgrade` from the owning
   plugin root.
2. Run the child-local validation command when the child repo has one.
3. Run root metadata validation after the lock refresh:
   - `uv run scripts/validate_socket_metadata.py`
4. Re-query Dependabot alerts and record any remaining alerts as either blocked
   by upstream constraints or intentionally deferred.

## Alert Inventory By Manifest

| Manifest | Critical | High | Medium | Low | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `plugins/cardhop-app/mcp/uv.lock` | 2 | 5 | 10 | 2 | 19 |
| `plugins/things-app/mcp/uv.lock` | 2 | 5 | 10 | 2 | 19 |
| `plugins/apple-dev-skills/uv.lock` | 0 | 0 | 1 | 1 | 2 |
| `plugins/productivity-skills/uv.lock` | 0 | 0 | 1 | 1 | 2 |
| `plugins/python-skills/uv.lock` | 0 | 0 | 1 | 1 | 2 |
| `plugins/agent-plugin-skills/uv.lock` | 0 | 0 | 1 | 0 | 1 |
| `plugins/things-app/uv.lock` | 0 | 0 | 1 | 0 | 1 |

## Current Decision

Do not dismiss any alerts yet. Patched versions exist for every listed package,
and the first remediation attempt should be dependency refresh plus validation.

If a lock refresh cannot clear an alert because an upstream package constrains a
vulnerable transitive dependency, record the blocking package and decide between
a targeted lower-bound override, an upstream issue, or a temporary documented
deferral.

## Remediation Plan

### Slice 1: MCP Server Lockfiles

Goal: clear the critical and high alerts first by refreshing the executable
Cardhop and Things MCP server dependency sets.

1. From `plugins/cardhop-app/mcp`, run `uv lock --upgrade`.
2. Validate Cardhop MCP from `plugins/cardhop-app/mcp`:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
3. From `plugins/things-app/mcp`, run `uv lock --upgrade`.
4. Validate Things MCP from `plugins/things-app/mcp`:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
5. Commit the two MCP lockfile refreshes if validation passes.

If either MCP lock refresh cannot reach the patched package versions, inspect
the locked dependency chain with `uv tree` from the affected MCP directory and
record the package that blocks the patched version.

### Slice 2: Remaining Plugin Lockfiles

Goal: clear the remaining medium and low alerts in skill/plugin lockfiles after
the executable MCP server surfaces are handled.

Refresh and validate these lockfiles one child at a time:

1. `plugins/agent-plugin-skills/uv.lock`
2. `plugins/apple-dev-skills/uv.lock`
3. `plugins/productivity-skills/uv.lock`
4. `plugins/python-skills/uv.lock`
5. `plugins/things-app/uv.lock`

For each child, run `uv lock --upgrade` from the owning plugin root, then run
that child's local validation if it exists. Prefer the child `AGENTS.md` and
`pyproject.toml` scripts over inventing a root-level check.

Commit the non-MCP lockfile refreshes separately from Slice 1 unless the diff is
tiny and all validation is clean.

### Slice 3: Alert Verification And Release

Goal: verify GitHub agrees the alerts are resolved, then publish a normal Socket
patch release if the dependency updates are clean.

1. Run root validation:
   - `uv run scripts/validate_socket_metadata.py`
2. Re-query open Dependabot alerts from GitHub.
3. If alerts remain, classify each remaining alert as:
   - blocked by an upstream constraint,
   - intentionally deferred,
   - or missed by the lock refresh and still actionable.
4. If the alert count reaches zero or only documented deferrals remain, release
   a Socket patch version with the repo-owned release script.

Do not tag the release until the final alert query has been recorded in this
note or a follow-up remediation note.

## Remediation Log

### 2026-06-15 MCP Lockfile Refresh

Commit `2b209d0d` refreshed these executable MCP server lockfiles:

- `plugins/cardhop-app/mcp/uv.lock`
- `plugins/things-app/mcp/uv.lock`

Both lockfiles now resolve the vulnerable packages above Dependabot's patched
floors:

| Package | Patched floor | Resolved version |
| --- | --- | --- |
| `fastmcp` | `3.2.0` | `3.4.2` |
| `authlib` | `1.6.12` | `1.7.2` |
| `PyJWT` | `2.12.0` | `2.13.0` |
| `python-multipart` | `0.0.27` | `0.0.32` |
| `starlette` | `1.0.1` | `1.3.1` |
| `idna` | `3.15` | `3.18` |
| `python-dotenv` | `1.2.2` | `1.2.2` |
| `cryptography` | `46.0.7` | `49.0.0` |
| `Pygments` | `2.20.0` | `2.20.0` |
| `pytest` | `9.0.3` | `9.1.0` |

Validation passed from each MCP directory:

- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy .`

The immediate post-push Dependabot API query on 2026-06-15 still listed the old
MCP alerts. Treat that as a GitHub rescan delay unless a later query still shows
the MCP alerts after GitHub has reprocessed the updated lockfiles.

### 2026-06-15 Plugin Maintainer Lockfile Refresh

The second remediation slice refreshed the remaining non-MCP plugin maintainer
lockfiles:

- `plugins/agent-plugin-skills/uv.lock`
- `plugins/apple-dev-skills/uv.lock`
- `plugins/productivity-skills/uv.lock`
- `plugins/python-skills/uv.lock`
- `plugins/things-app/uv.lock`

All five lockfiles now resolve `pytest` to `9.1.0`, above Dependabot's patched
floor of `9.0.3`. The refresh also moved the remaining `Pygments` alerts to
`2.20.0`, above Dependabot's patched floor of `2.20.0`.

`plugins/apple-dev-skills/pyproject.toml` now requires Python `>=3.10` for its
maintainer tooling because `pytest>=9.0.3` no longer supports Python 3.9. This
does not change the Apple skill content; it only narrows the Python version used
to run that child repo's maintainer tests.

Validation passed:

- `plugins/agent-plugin-skills`: `uv run pytest`, `uv run ruff check .`,
  `uv run mypy .`
- `plugins/apple-dev-skills`: `bash .github/scripts/validate_repo_docs.sh`,
  `uv run pytest`
- `plugins/productivity-skills`: `uv run pytest`
- `plugins/python-skills`: `uv run scripts/validate_repo_metadata.py`,
  `uv run pytest`, `uv run ruff check .`, `uv run mypy .`
- `plugins/things-app`: `uv run pytest`
- Socket root: `uv run scripts/validate_socket_metadata.py`
