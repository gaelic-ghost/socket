---
name: project-docs-maintainer
description: Audit and maintain project documentation alignment with a deterministic two-pass workflow. Use when repository docs drift from tooling/manifests, when *-skills README standards need profile-aware alignment, or when you need Markdown plus JSON reports with optional bounded fixes.
---

# Project Docs Maintainer

Run documentation maintenance in explicit modes so behavior stays deterministic and bounded.

## Modes

- `workspace_docs_alignment`: general repository documentation drift checks and safe fixes.
- `skills_readme_alignment`: profile-aware README standards checks and safe fixes for `*-skills` repositories.

## Inputs

Pass runtime inputs from the calling prompt:

- `--mode <workspace_docs_alignment|skills_readme_alignment>`
- `--workspace <path>`
- Optional `--exclude <path>` (repeatable)
- Optional mode-specific flags shown below

## Workflow

1. Choose mode based on user intent.
2. Run pass 1 audit.
3. Review issue categories and impacted repositories.
4. If requested and safe, run pass 2 with `--apply-fixes`.
5. Re-check touched repositories and report Markdown plus JSON results.

## Commands

`workspace_docs_alignment` audit:

```bash
uv run python scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --print-md \
  --print-json
```

`workspace_docs_alignment` audit + fixes:

```bash
uv run python scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --apply-fixes \
  --md-out /tmp/docs-alignment-report.md \
  --json-out /tmp/docs-alignment-report.json
```

`skills_readme_alignment` audit:

```bash
uv run python scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --print-md \
  --print-json
```

`skills_readme_alignment` audit + fixes:

```bash
uv run python scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --apply-fixes \
  --md-out /tmp/readme-alignment-report.md \
  --json-out /tmp/readme-alignment-report.json
```

## Safety Rules

- Never commit changes automatically.
- Edit documentation files only.
- Never edit source code, manifests, lockfiles, or CI files.
- Treat `AGENTS.md` as out-of-scope for automated fixes unless user explicitly requests AGENTS maintenance.
- Apply only bounded replacements and minimal structural normalization.

## Output Contract

Both modes must provide:

- Human-readable Markdown summary.
- Machine-readable JSON report.
- Clear list of touched files and remaining issues.

## Automation Templates

Use `$project-docs-maintainer` in automation prompts.

Templates:

- `references/automation-prompts.md` for `workspace_docs_alignment`
- `references/automation-prompts-skills-readme.md` for `skills_readme_alignment`

## References

- `references/checks-common.md`
- `references/checks-swift.md`
- `references/checks-js-ts.md`
- `references/checks-python.md`
- `references/checks-rust.md`
- `references/fix-policies.md`
- `references/output-contract.md`
- `references/profile-model.md`
- `references/section-schema.md`
- `references/style-rules.md`
- `references/discoverability-rules.md`
- `references/verification-checklist.md`
- `references/seed-artifacts.md`
- `references/automation-prompts.md`
- `references/automation-prompts-skills-readme.md`
