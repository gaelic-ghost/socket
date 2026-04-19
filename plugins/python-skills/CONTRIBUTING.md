# Contributing to python-skills

## Table of Contents

- [Overview](#overview)
- [Contribution Workflow](#contribution-workflow)
- [Local Setup](#local-setup)
- [Development Expectations](#development-expectations)
- [Pull Request Expectations](#pull-request-expectations)
- [Communication](#communication)
- [Contribution Terms](#contribution-terms)

## Overview

### Who This Guide Is For

Use this guide when you are changing the root docs, packaged plugin metadata, validation helpers, or shipped skills in `python-skills`.

### Before You Start

This repository has a deliberate split between authored workflow content and packaging metadata. Root [`skills/`](./skills/) is the source of truth. The repo root is also the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json). Keep that split intact whenever you edit the repo.

## Contribution Workflow

### Choose the Right Surface

Use `python-skills` when Python-, `uv`-, FastAPI-, FastMCP-, or pytest-specific behavior should shape the workflow. If the change is really a general-purpose maintainer pattern, move it to `productivity-skills` instead of broadening this repo.

### Keep Changes Coherent

Keep each change focused on one outcome. When the shipped skill surface changes, update the affected skill docs, packaging metadata, and root inventory docs in the same pass.

### Keep The Docs Split Clean

Use [`README.md`](./README.md) for the public project overview, install surfaces, active skill inventory, and packaging shape. Use this file for maintainer workflow, contributor expectations, and validation habits. Use [`AGENTS.md`](./AGENTS.md) for durable repo-local instructions to Codex.

## Local Setup

### Runtime Config

Sync the maintainer environment before editing docs, metadata, or tests:

```bash
uv sync --dev
```

The repo uses [`pyproject.toml`](./pyproject.toml) and [`uv.lock`](./uv.lock) as the maintainer tooling baseline. There is no long-lived service config required for ordinary documentation and metadata work.

### Runtime Behavior

This repository is file-backed rather than service-backed. The normal contributor loop is: edit root `skills/`, keep the repo-root plugin metadata aligned, update the root docs if the shipped surface changed, then run the validation path. For Claude-side local discovery, the repo-root marketplace catalog is `.claude-plugin/marketplace.json`.

## Development Expectations

### Source Of Truth

Treat each skill directory's `SKILL.md` plus `agents/openai.yaml` as the canonical per-skill contract pair. Do not reintroduce a second packaged subtree for Codex, and do not reintroduce maintained per-skill `README.md` files.

### Verification

Run the repo checks before landing documentation or metadata work:

```bash
uv run scripts/validate_repo_metadata.py
uv run pytest
```

When a change touches Python tooling guidance, keep commands expressed with `uv run ...` and make sure the docs still match the real repo surface.

### Accessibility Expectations

Keep contributor-facing and user-facing documentation easy to scan, with clear headings, blunt status text, and packaging language that does not hide which surface is the source of truth. If a docs change affects how people install or discover the repo, make that path explicit.

## Pull Request Expectations

Summarize the real maintainer-facing behavior change, not just the edited files. Call out whether the change affects the authored `skills/` tree, the thin packaging layer, or only the repo docs. Include the validation you ran.

## Communication

Surface scope widening early. If the work starts as a repo-docs pass but actually needs packaging-policy changes, validator changes, or skill-surface changes, say that plainly before continuing.

## Contribution Terms

By contributing to this repository, you agree that your contributions will be licensed under the Apache License 2.0 project license.
