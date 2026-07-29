# Project Documentation Boundaries

Use this reference when an audit finds repeated content or a doc section that seems to belong in another file.

## Canonical Owners

| File | Owns | Should Link To |
| --- | --- | --- |
| `README.md` | Product identity, current status, quick start, usage, repo structure, and a short development pointer. | `CONTRIBUTING.md`, `ROADMAP.md`, relevant package or product docs. |
| `CONTRIBUTING.md` | Human contributor setup, workflow, verification, PR expectations, and communication guidance. | `README.md`, `ACCESSIBILITY.md`, repo-maintenance docs, `AGENTS.md` only when contributors need to know agent rules exist. |
| `AGENTS.md` | Durable instructions for Codex and other repo agents: scope, routing, commands, workflow constraints, delivery rules, safety boundaries, and local overrides. | `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, maintainer docs. |
| `ACCESSIBILITY.md` | Accessibility target standards, implementation expectations, known gaps, support paths, and verification evidence. | `CONTRIBUTING.md` for contributor obligations and `README.md` for user-facing support pointers. |
| `ROADMAP.md` | Milestones, small tickets, imported TODO/FIXME work, issue links, and notable planning history. | GitHub issues, source references, docs that explain accepted scope. |

## Drift Signals

- README contains full branch, PR, release, or maintainer workflow instructions instead of a short pointer.
- CONTRIBUTING repeats product overview or roadmap history instead of contributor workflow.
- AGENTS repeats public product marketing, contributor onboarding prose, or detailed accessibility standards.
- ACCESSIBILITY makes ungrounded legal conformance claims or repeats general contributor workflow.
- ROADMAP contains long procedural guidance that should live in AGENTS, CONTRIBUTING, or maintainer docs.

## Fixing Policy

In `check-only`, report the owning file and the likely destination. In `apply`, only run the owner document skills. Do not move content across files unless the user explicitly asks for that cleanup or a future deterministic cross-doc fixer owns it.
