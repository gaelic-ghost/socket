# Contributing to productivity-skills

## Overview

Use this guide when adding or revising skills in this repository. `productivity-skills` is both a public global-install plugin and the canonical general-purpose baseline layer for workflow families that may later specialize into stack-specific plugins such as `apple-dev-skills` or `python-skills`.

## Contribution Workflow

- Start from a clean branch or worktree and keep each change focused on one coherent maintainer or skill outcome.
- Update the skill, its metadata, its tests, and any affected repo inventory docs in the same pass.
- When a workflow belongs more naturally in a specialized plugin, move or incubate it there instead of widening this repo casually.
- When finishing milestone-sized work, update `ROADMAP.md` in the same change unless Gale explicitly says not to.

## Local Setup

### Runtime Config

```bash
uv sync --dev
```

No long-lived app configuration is required for ordinary maintainer work in this repository. Use the root `pyproject.toml` as the Python tooling baseline, and keep plugin packaging metadata under `plugins/productivity-skills/` aligned with the skill source of truth under `skills/`.

### Runtime Behavior

This repository does not have a service-style runtime. The main contributor loop is file-backed and validation-backed: update skill assets under `skills/`, keep metadata and maintainer docs synchronized, and run the relevant checks before committing. Treat this repo as the broad baseline layer; if a change only makes sense with strong stack-specific assumptions, that is a signal to move the work into the corresponding specialized plugin instead of forcing it into this repo.

## Naming Conventions

- Keep skill names clear, stable, and domain-grouped, usually in `<category>-<domain>-<purpose>` form.
- Use the same names for the same concepts across `SKILL.md`, `agents/openai.yaml`, scripts, references, plugin metadata, marketplace metadata, and maintainer docs.
- Treat `productivity-skills` as the general-purpose or superclass layer in docs and contributor notes; reserve specialization language for plugins that truly narrow the workflow.
- Do not rename fields, files, or workflow concepts casually when the underlying meaning has not changed.

## Verification

```bash
uv run --group dev pytest
```

Also run any narrower checks that directly match the touched surface when appropriate, such as targeted pytest invocations for a single Python-backed skill.

## Pull Request Expectations

- Explain whether the change strengthens the global baseline layer, introduces a new broadly reusable workflow, or moves a specialized concern out to a narrower plugin.
- Summarize the maintainer-facing behavior change, not just the files touched.
- Include the validation you ran and note any intentionally untouched unrelated workspace state, such as local untracked plugin trees.
