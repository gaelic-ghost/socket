# Contributing to agent-plugin-skills

Use this guide when preparing changes so the repository stays understandable, runnable, and reviewable for the next maintainer.

## Table of Contents

- [Overview](#overview)
- [Contribution Workflow](#contribution-workflow)
- [Local Setup](#local-setup)
- [Development Expectations](#development-expectations)
- [Pull Request Expectations](#pull-request-expectations)
- [Communication](#communication)
- [License and Contribution Terms](#license-and-contribution-terms)

## Overview

### Who This Guide Is For

Use this guide if you are changing the shipped maintainer skills, the repo-local maintainer docs, or the small Python-backed audit tooling that supports those skills.

### Before You Start

Read [README.md](./README.md) for the public project shape, [AGENTS.md](./AGENTS.md) for durable repo rules, and the relevant maintainer docs under [`docs/maintainers/`](./docs/maintainers/) before changing packaging or guidance wording.

If your change touches a skill contract, plan to update the nearest docs and tests in the same pass.

## Contribution Workflow

### Choosing Work

Pick work that clearly belongs to this repository's narrow role: maintainer guidance for skills-export and plugin-export repos. General repo-doc cleanup belongs in `productivity-skills` unless this repo's narrower plugin-repo boundary is the real subject.

When the work is about Codex plugin behavior, confirm the current OpenAI docs first instead of relying on older local assumptions.

### Making Changes

Keep root [`skills/`](./skills/) canonical, keep repo-level maintainer explanations under [`docs/maintainers/`](./docs/maintainers/), and keep source-repo plugin metadata under [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).

Do not reintroduce nested staged plugin directories, installer-era workflows, or vague install-surface language while making an unrelated fix.

### Asking For Review

A change is ready for review when the docs split still makes sense, nearby tests are updated when needed, and the final wording is explicit about which Codex surface or repo contract it is talking about.

## Local Setup

### Runtime Config

This repository uses `uv` for local Python tooling. Sync the dev environment before running tests:

```bash
uv sync --dev
```

This repo does not require dedicated local services or repo-specific secret configuration for normal docs and test work.

### Runtime Behavior

Most changes here are static docs, skill content, and small audit scripts. The main sign that the repo is healthy is that the shipped tests pass and the updated docs still match the shipped skill surface.

Run the normal validation flow with:

```bash
uv run pytest
```

## Development Expectations

### Naming Conventions

Keep the repo's core terms stable:

- `skill` means the reusable workflow-authoring unit under `skills/`
- `plugin` means the installable Codex distribution bundle rooted at `.codex-plugin/plugin.json`
- `subagent` means a delegated runtime worker, not a packaged repo surface

Match existing file, skill, and maintainer-doc names unless the change is explicitly about renaming.

### Accessibility Expectations

This repository is mostly docs and maintainer tooling rather than end-user UI, but contributors should still keep instructions, prompts, and audit output readable, plain, and unambiguous.

If a change makes maintainer-facing language harder to scan or more ambiguous, treat that as a quality issue and fix it before asking for review.

### Verification

Prefer the grounded repo checks:

```bash
uv sync --dev
uv run pytest
```

If you changed only prose, still sanity-check the nearby docs for split clarity and internal consistency before handing the work off.

## Pull Request Expectations

A good pull request keeps the scope narrow, explains which repo surface changed, and calls out any linked doc, test, or packaging updates that were needed to keep the repository coherent.

If the change updates skill behavior or audit expectations, mention the validation you ran and which nearby docs moved with it.

## Communication

Surface uncertainty early when a change might widen the repository's role, soften a documented Codex boundary, or reintroduce old installer-era assumptions.

If a task starts to require a new maintainer workflow, a new supported repo family, or a broader packaging model, pause and confirm that expansion before continuing.

## License and Contribution Terms

Contributions are governed by the repository license. See [LICENSE](./LICENSE) for the applicable terms.
