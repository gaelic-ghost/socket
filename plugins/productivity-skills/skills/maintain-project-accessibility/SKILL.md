---
name: maintain-project-accessibility
description: Maintain canonical ACCESSIBILITY.md files through deterministic audit and bounded apply modes. Use when a project needs a durable accessibility control document that defines standards, implementation expectations, testing coverage, known exceptions, and contributor obligations.
---

# Maintain Project Accessibility

Maintain canonical `ACCESSIBILITY.md` files through one deterministic accessibility-document workflow.

This skill is the default baseline path for `ACCESSIBILITY.md` maintenance across most repositories. It treats `ACCESSIBILITY.md` as the project's canonical accessibility control document for standards, architecture, verification, ownership, and known exceptions. Reach for a narrower plugin only when the target repo has a specialized shape that deserves its own accessibility contract.

## Inputs

- Required: `--project-root <path>`
- Required: `--run-mode <check-only|apply>`
- Optional: `--accessibility-path <path>`
- Optional: `--config <path>`

## Workflow

1. Validate the project root and resolve the target `ACCESSIBILITY.md`.
2. Load the canonical accessibility schema from `config/accessibility-customization.template.yaml`, then merge any explicit override or project-local customization file.
3. In `check-only`, audit the required section schema, required subsection schema, required table of contents, placeholder content, unsupported compliance claims, and thin or missing verification evidence.
4. In `apply`, keep edits bounded to the target `ACCESSIBILITY.md` while creating a missing file from the bundled template and normalizing the document to the canonical structure.
5. Preserve useful preamble material before the first H2 while normalizing the structural contract around it.
6. Re-run the same audit to confirm post-fix status.

## Canonical Base Contract

The source of truth for the base accessibility-document contract lives in:

- `config/accessibility-customization.template.yaml`
- `assets/ACCESSIBILITY.template.md`

The base contract requires:

- a top-level title and short summary
- a required `## Table of Contents`
- canonical top-level sections for overview, standards baseline, accessibility architecture, engineering workflow, known gaps, user support and reporting, and verification and evidence
- required subsection structure for each top-level section
- explicit language that distinguishes target standards from verified legal conformance claims

## Writing Expectations

- Keep the whole ACCESSIBILITY document near 300 lines or less by default. Treat 350 lines as a soft ceiling that should trigger consolidation into concise standards, known gaps, support paths, and evidence links.
- Keep most top-level sections near 45 lines or less and most subsections near 25 lines or less. Prefer current evidence and clear obligations over broad accessibility essays.
- `Overview > Status` should stay short, plain, and current.
- `Overview > Scope` should state exactly which project surfaces this accessibility contract covers.
- `Standards Baseline > Target Standard` should explicitly name the target standard or internal accessibility baseline.
- `Standards Baseline > Conformance Language Rules` should explain what the project may and may not claim about accessibility status.
- `Accessibility Architecture` should explain how the product handles semantic structure, focus, labeling, motion, contrast, zoom, and alternatives in practical engineering terms.
- `Engineering Workflow > Definition of Done` should make accessibility a merge-quality requirement for relevant changes.
- `Known Gaps` should always exist, even when it only records that there are no currently documented exceptions.
- `Verification and Evidence` should prefer grounded tools, commands, audit dates, and review history over general promises.
- Keep ACCESSIBILITY, CONTRIBUTING, README, and AGENTS responsibilities distinct. Accessibility standards, gaps, and evidence live here; contributor reminders should link here from `CONTRIBUTING.md`; product summary stays in `README.md`; agent-specific enforcement or routing belongs in `AGENTS.md`.

## Codex Subagent Fit

When the user explicitly asks for subagents or parallel agent work, use subagents only for read-heavy accessibility evidence gathering before the main workflow edits or reports. Good jobs include checking documented verification commands, inventorying UI surfaces, reading known-gap notes, or comparing accessibility claims against repo evidence.

Keep `apply` edits in the main thread because this skill owns one target `ACCESSIBILITY.md` file and must avoid unsupported compliance claims. Ask workers for concise evidence, risks, and file references rather than drafted conformance language.

## Output Contract

- Return Markdown plus JSON with:
  - `run_context`
  - `schema_contract`
  - `schema_violations`
  - `claim_integrity_issues`
  - `verification_evidence_issues`
  - `content_quality_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`
- If there are no issues and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never invent compliance claims, test coverage, supported assistive technologies, or audit history that are not grounded in the repo.
- Never edit files other than the target `ACCESSIBILITY.md`.
- Keep `ACCESSIBILITY.md` as the canonical filename for this skill.
- Treat this skill as a hard-enforced base template. Downstream plugins may specialize the schema, but the base skill should not do stack-profile inference.
- Do not let the baseline workflow claim verified legal conformance by default. Prefer target-language such as "targets WCAG 2.2 AA" unless the repo has grounded evidence for stronger wording.

## References

- `agents/openai.yaml`
- `references/section-schema.md`
- `references/output-contract.md`
- `references/fix-policies.md`
- `references/style-rules.md`
- `references/accessibility-customization.md`
- `references/accessibility-config-schema.md`
- `references/standards-positioning.md`
- `references/project-accessibility-maintenance-automation-prompts.md`
