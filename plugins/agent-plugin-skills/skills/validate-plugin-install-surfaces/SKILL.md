---
name: validate-plugin-install-surfaces
description: Audit install surfaces, metadata overlays, plugin manifests, marketplace wiring, discovery mirrors, and README install examples in an agent-skills or agent-plugin repository. Use when a maintainer needs one bounded workflow to detect install-surface drift without mutating the repo.
---

# Validate Plugin Install Surfaces

Audit install surfaces and metadata overlays in an agent-skills or agent-plugin repository through one deterministic, audit-only workflow.

Current scope note:

- This skill is the audit-only metadata and install-surface validator for this repo family.
- It treats root `skills/` as canonical authored content and validates overlays around it.
- It is intentionally separate from `sync-skills-repo-guidance`, which handles broader guidance reconciliation, and from `install-plugin-to-socket`, which performs bounded install wiring actions.
- Version 1 is audit-only by design. It reports drift and missing surfaces without editing files.

## Inputs

- Required: `--repo-root <path>`
- Optional: `--plugin-name <name>` when the plugin directory name should not be inferred from the repo layout
- Optional: `--print-md`
- Optional: `--print-json`
- Optional: `--md-out <path>`
- Optional: `--json-out <path>`
- Optional: `--fail-on-findings`

## Workflow

1. Confirm the task is metadata or install-surface validation, not docs-only maintenance or local plugin installation.
2. Treat root `skills/` as the canonical authored surface.
3. Audit each skill directory for:
   - `SKILL.md`
   - frontmatter `name` and `description`
   - `agents/openai.yaml`
   - required OpenAI interface fields
4. Audit plugin packaging surfaces for:
   - `.codex-plugin/plugin.json`
   - `.claude-plugin/plugin.json`
   - naming and key metadata consistency
5. Audit marketplace metadata and local install surfaces for:
   - `.agents/plugins/marketplace.json`
   - local `source.path` correctness
   - referenced plugin roots existing on disk
6. Audit repo-level discovery mirrors for:
   - `.agents/skills -> ../skills`
   - `.claude/skills -> ../skills`
7. Audit the bundled plugin skills directory for:
   - `plugins/<plugin>/skills/` existing as a real directory
   - the bundled tree staying in sync with root `skills/`
8. Audit README install examples and install-surface references against the actual repo structure.
9. Return Markdown and JSON findings grouped by metadata, install surfaces, and bundled-skills or mirror drift.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `canonical_skill_dirs`
  - `plugin_roots`
  - `metadata_findings`
  - `install_surface_findings`
  - `mirror_findings`
  - `errors`
- If there are no findings and no errors, output exactly `No findings.`

## Guardrails

- Never auto-fix files in v1.
- Never edit plugin manifests, README files, marketplace metadata, or symlink surfaces.
- Never claim that mirrors are canonical. Root `skills/` remains canonical.
- Never replace `maintain-plugin-docs` for README or roadmap maintenance.
- Never replace `install-plugin-to-socket` for install, update, uninstall, verify, enable, disable, or promote operations.
- Never flatten repo-specific maintainer policy while validating shared install surfaces.

## References

- `references/validation-surface.md`
- `references/output-contract.md`
