# AGENTS.md

This file is the Productivity Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `productivity-skills` is the canonical home for broadly useful general-purpose productivity workflows.
- Keep this repo focused on reusable baseline workflow families whose best version does not depend on strong stack- or repo-specific assumptions.
- Root [`skills/`](./skills/) is the canonical authored surface.
- Treat plugin packaging and marketplace metadata as thin discovery layers around the authored skill surface.

## Local Rules

- Keep documentation-maintenance skills split by document type instead of collapsing README, AGENTS, CONTRIBUTING, ROADMAP, and other document maintenance into one oversized workflow.
- Keep framework-neutral automation and eval design in `design-agent-automation-workflow` and `design-agent-eval-workflow`; put runtime-specific implementation in the owning stack plugin, repo-local agent package, or official workflow surface.
- Prefer safe full automation when bounded scope, validation, rollback or no-op behavior, and side-effect controls make it reliable. Use human review only for the exact decision that cannot be made reasonably safe.
- Keep stack-specific or repo-family-specific maintainer skills in the dedicated repos that own them.
- `bootstrap-skills-plugin-repo` and `sync-skills-repo-guidance` moved to `agent-portability-skills` and should stay there.
- Treat `maintain-project-repo` release choreography as release-only guidance; it does not override narrower document-maintenance skills that forbid auto-commit, auto-push, or PR creation.
- Use the `repo-docs-auditor` custom-agent role only for explicit-trigger subagent workflows: broad read-heavy repo-document audits, stale-command checks, cross-document drift scans, and review-packet planning. Keep final edits, validation, commits, pushes, PRs, and releases in the main thread.
- Use the `code-slice-tracer` custom-agent role only for explicit-trigger subagent workflows: bounded call-site mapping, branch tracing, test/doc correlation, and comparison support. Keep the final explanation and any `SLICES.md` writes in the main thread.

## Validation

```bash
uv run pytest
```
