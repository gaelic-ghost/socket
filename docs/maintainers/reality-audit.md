# Reality Audit Guide

Use this guide when reconciling repository documentation with the actual shipped skill surface, local scripts, and tests.

## Source-of-Truth Order

Use the highest-confidence artifact first and only fall back when the higher layer is silent.

1. Runtime behavior proven by tests under `tests/`
2. Shipped skill assets under `skills/<skill>/`
   - `SKILL.md`
   - `agents/openai.yaml`
   - `references/`
   - `scripts/`
3. Repository validation rules in `.github/scripts/validate_repo_docs.sh`
4. Root maintainer and discoverability docs
   - `README.md`
   - `AGENTS.md`
   - `ROADMAP.md`
   - `docs/maintainers/`

## Audit Procedure

1. Confirm the active public skill surface from the directories under `skills/`.
2. Check each active skill for the documented contract:
   - required headings in `SKILL.md`
   - `agents/openai.yaml`
   - `references/customization.template.yaml`
   - `references/`
   - local snippet copy under `references/snippets/`
3. Run the repo docs validator and treat failures as documentation-contract drift unless code assets prove otherwise.
4. Run the Python test suite and treat failures as runtime drift.
5. Reconcile root docs to the tested, shipped state instead of preserving stale historical wording.
6. Update `ROADMAP.md` in the same change when milestone or status text is no longer truthful.

## Durable Review Criteria

- Root docs must describe the same active skill surface.
- Maintainer-doc links in root docs must resolve on disk.
- Validation rules must check the canonical maintainer-doc paths, not legacy locations.
- Historical notes may mention retired skills or paths only in migration context.
- Maintainer docs must not imply that repo-root files are required when the canonical files live under `docs/maintainers/`.

## Current Canonical Maintainer Docs

- Workflow diagrams and UX maps: `docs/maintainers/workflow-atlas.md`
- Audit procedure and source-of-truth order: `docs/maintainers/reality-audit.md`

## Reporting Shape

A maintainer audit report should summarize:

- documentation drift found
- validation health
- test health
- roadmap credibility or staleness
- remaining follow-up items
