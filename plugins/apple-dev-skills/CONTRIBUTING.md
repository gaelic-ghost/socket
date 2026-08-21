# Contributing to apple-dev-skills

Use this guide when preparing changes so the repository stays understandable, testable, and truthful about the Apple workflow surface it actually ships.

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

Use this guide when you are changing the shipped skills, the maintainer docs, the validator, or the supporting tests for this repository.

### Before You Start

Read [`README.md`](./README.md), [`ROADMAP.md`](./ROADMAP.md), [`AGENTS.md`](./AGENTS.md), and [`docs/maintainers/reality-audit.md`](./docs/maintainers/reality-audit.md) before broadening a docs or workflow change. If the work touches one specific skill, read that skill directory first instead of generalizing from sibling skills.

## Contribution Workflow

### Choosing Work

Take work from the live repo surface, not from stale planning notes. Use `ROADMAP.md` for current milestone status, the validator and tests for the enforced public contract, and the active skill directories under [`skills/`](./skills/) for the shipped behavior.

### Making Changes

Keep changes bounded to the smallest coherent surface that fixes the real drift. When a shipped skill, maintainer doc, validator rule, or test expectation changes, update the nearby supporting docs and tests in the same pass so the repo stays self-consistent. Treat `README.md` as the public repo entrypoint, `CONTRIBUTING.md` as the maintainer workflow guide, `AGENTS.md` as durable agent policy, and `ROADMAP.md` as the durable planning and history surface.

### Asking For Review

Ask for review after the changed docs, validator expectations, and relevant tests agree with each other. Call out any deliberate scope cuts, any follow-up work left in `ROADMAP.md`, and any validation you could not run.

## Local Setup

### Runtime Config

Inspect the root managed commands with:

```bash
just --list
```

This repository does not require app secrets or background services for its normal docs and skill-validation workflow.

### Runtime Behavior

The repository is healthy when root validation and the single root E2E test pass, and the root docs describe the same shipped surface as the active skill directories. Use [`docs/maintainers/reality-audit.md`](./docs/maintainers/reality-audit.md) when you need the repo's source-of-truth order or audit procedure.

## Development Expectations

### Naming Conventions

Keep skill names literal and workflow-oriented. Preserve the existing Apple-specific terminology, the current active skill names, and the repo's distinction between canonical authored surfaces under [`skills/`](./skills/) and packaging metadata under the plugin manifests.

### Accessibility Expectations

When you change Apple accessibility guidance, keep it grounded in current Apple documentation, update the owning skill in the same pass, and avoid presenting generic visual-design advice as if it were accessibility guidance.

### Verification

Run only the root integration gates:

```bash
just repo-validate
just test
```

Do not add nested or unit tests for this plugin.

## Pull Request Expectations

Summarize what changed, why the docs or workflow contract needed to move, and which validator or test results support the change. Keep docs-only cleanup clearly separated from behavior-changing skill work when the split matters for review.

## Communication

Raise questions before widening scope into new skills, new export surfaces, or broader repo-structure changes. If a historical maintainer doc is no longer carrying live decision-making value, prefer collapsing its durable conclusions into `ROADMAP.md` or the still-live maintainer docs instead of preserving another orphan planning note.

## License and Contribution Terms

This repository is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for the governing contribution and reuse terms.
