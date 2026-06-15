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
