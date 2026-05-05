# Accessibility Maintenance Plan

This document is maintainer-only. It records the proposed baseline design for a new `maintain-project-accessibility` skill and the related `maintain-project-contributing` schema expansion that will make accessibility expectations part of the contributor contract.

## Status

- Proposal drafted
- Not implemented yet
- Intended repo: `productivity-skills`

## Direction Summary

- Add a new baseline documentation-maintenance skill named `maintain-project-accessibility`.
- Treat `ACCESSIBILITY.md` as a repo-local control document, not as a standardized public accessibility-statement filename.
- Use `ACCESSIBILITY.md` to define accessibility standards, architecture, verification, ownership, and known exceptions.
- Keep public-facing accessibility statements, formal ACR/VPAT artifacts, and procurement-facing conformance reporting out of scope for the first pass.
- Extend `maintain-project-contributing` so contributor expectations explicitly require work to stay aligned with the canonical `ACCESSIBILITY.md`.

## Why This Belongs In `productivity-skills`

- Accessibility standards and verification are broadly reusable maintainer concerns across many repositories.
- The repository already keeps document-maintenance workflows split by document type instead of collapsing them into one oversized skill.
- `ACCESSIBILITY.md` fills a real gap between user-facing README material and contributor-facing CONTRIBUTING guidance.
- A dedicated baseline skill gives downstream plugins a stable extension point when narrower stacks need stronger accessibility rules later.

## Scope Boundaries

### In Scope

- Canonical `ACCESSIBILITY.md` schema and bootstrap template
- Deterministic `check-only` and bounded `apply` modes
- Accessibility standards wording, implementation expectations, testing requirements, ownership, and known-gap tracking
- A contributor-facing `Accessibility Expectations` subsection in `CONTRIBUTING.md`

### Out Of Scope For The First Pass

- Public website accessibility statement generation
- Formal VPAT, ACR, or procurement reporting
- Stack-specific accessibility heuristics baked into the baseline workflow
- Automatic code scanning beyond what the document-maintenance skill can truthfully audit from repo evidence

## Proposed Skill Surface

Create a new sibling directory:

```text
skills/maintain-project-accessibility/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── ACCESSIBILITY.template.md
├── config/
│   └── accessibility-customization.template.yaml
├── references/
│   ├── accessibility-config-schema.md
│   ├── accessibility-customization.md
│   ├── fix-policies.md
│   ├── output-contract.md
│   ├── project-accessibility-maintenance-automation-prompts.md
│   ├── section-schema.md
│   ├── standards-positioning.md
│   └── style-rules.md
├── scripts/
│   └── maintain_project_accessibility.py
└── tests/
    └── test_maintain_project_accessibility.py
```

## Canonical Purpose

`maintain-project-accessibility` should be the default baseline path for `ACCESSIBILITY.md` maintenance across most repositories unless a narrower plugin owns that repo shape.

The skill should treat `ACCESSIBILITY.md` as the project's canonical accessibility control document. It should explain:

- which standards the project targets
- which product surfaces those standards apply to
- how the project implements accessibility in practice
- how contributors and maintainers verify accessibility before merge
- which exceptions or known gaps still exist
- who owns remediation and feedback handling

## Proposed `SKILL.md` Contract

### Frontmatter Direction

```yaml
---
name: maintain-project-accessibility
description: Maintain canonical ACCESSIBILITY.md files through deterministic audit and bounded apply modes. Use when a project needs a durable accessibility control document that defines standards, implementation expectations, testing coverage, known exceptions, and contributor obligations.
---
```

### Workflow Direction

- Required inputs:
  - `--project-root <path>`
  - `--run-mode <check-only|apply>`
- Optional inputs:
  - `--accessibility-path <path>`
  - `--config <path>`
- `check-only` should audit:
  - required title and summary
  - required table of contents
  - required top-level sections and subsection schema
  - placeholder content
  - unsupported compliance claims
  - missing known-gap or ownership surfaces
  - weak or missing evidence language for verification
- `apply` should:
  - create a missing `ACCESSIBILITY.md` from the template
  - normalize the file to the configured schema
  - preserve useful preamble material before the first H2
  - keep edits bounded to the target `ACCESSIBILITY.md`

### Output Contract Direction

Return Markdown plus JSON with:

- `run_context`
- `schema_contract`
- `schema_violations`
- `claim_integrity_issues`
- `verification_evidence_issues`
- `content_quality_issues`
- `fixes_applied`
- `post_fix_status`
- `errors`

If there are no issues and no errors, output exactly `No findings.`

### Guardrail Direction

- Never auto-commit, auto-push, or open a PR.
- Never invent compliance claims, test coverage, supported assistive technologies, or audit history that are not grounded in the repo.
- Never edit files other than the target `ACCESSIBILITY.md`.
- Do not let the baseline skill claim legal conformance by default.
- Prefer target-language such as "targets WCAG 2.2 AA" unless the repo has grounded evidence that stronger language is accurate.

## Proposed Canonical `ACCESSIBILITY.md` Schema

### Top-Level Shape

1. top-level title
2. short one-line summary
3. `## Table of Contents`
4. `## Overview`
5. `## Standards Baseline`
6. `## Accessibility Architecture`
7. `## Engineering Workflow`
8. `## Known Gaps`
9. `## User Support and Reporting`
10. `## Verification and Evidence`

### Required Subsection Shape

- `Overview`
  - `Status`
  - `Scope`
  - `Accessibility Goals`
- `Standards Baseline`
  - `Target Standard`
  - `Conformance Language Rules`
  - `Supported Platforms and Surfaces`
- `Accessibility Architecture`
  - `Semantic Structure`
  - `Input and Keyboard Model`
  - `Focus Management`
  - `Naming and Announcements`
  - `Color, Contrast, and Motion`
  - `Zoom, Reflow, and Responsive Behavior`
  - `Media, Captions, and Alternatives`
- `Engineering Workflow`
  - `Design and Implementation Rules`
  - `Automated Testing`
  - `Manual Testing`
  - `Assistive Technology Coverage`
  - `Definition of Done`
- `Known Gaps`
  - `Current Exceptions`
  - `Planned Remediation`
  - `Ownership`
- `User Support and Reporting`
  - `Feedback Path`
  - `Triage Expectations`
- `Verification and Evidence`
  - `CI Signals`
  - `Audit Cadence`
  - `Review History`

### Hard-Enforced Writing Expectations

- `Overview > Status` must be short, plain, and current.
- `Overview > Scope` must define which product or repo surfaces this document covers.
- `Standards Baseline > Target Standard` must name the actual target standard or internal accessibility baseline.
- `Conformance Language Rules` must distinguish target standards from verified legal conformance claims.
- `Engineering Workflow > Definition of Done` must make accessibility a merge-quality requirement for relevant work.
- `Known Gaps` must always exist, even when it only records that there are no currently documented exceptions.
- `Verification and Evidence` must prefer grounded tools, commands, audit dates, and evidence over general promises.

## Proposed Bootstrap Template

```md
# Accessibility

Describe the project's accessibility posture in one short sentence.

## Table of Contents

- [Overview](#overview)
- [Standards Baseline](#standards-baseline)
- [Accessibility Architecture](#accessibility-architecture)
- [Engineering Workflow](#engineering-workflow)
- [Known Gaps](#known-gaps)
- [User Support and Reporting](#user-support-and-reporting)
- [Verification and Evidence](#verification-and-evidence)

## Overview

### Status

State the current accessibility posture in one short, plain sentence.

### Scope

Describe which project surfaces this accessibility contract covers.

### Accessibility Goals

Describe the real accessibility outcomes this project is trying to deliver.

## Standards Baseline

### Target Standard

Name the target standard or internal baseline this project is working toward.

### Conformance Language Rules

Explain what language the project may or may not use when describing accessibility status.

### Supported Platforms and Surfaces

List the concrete environments, platforms, or user-facing surfaces this document applies to.

## Accessibility Architecture

### Semantic Structure

Describe how the project preserves headings, landmarks, labels, structure, and other semantic meaning.

### Input and Keyboard Model

Describe how the project handles keyboard access, direct input, and interaction behavior.

### Focus Management

Describe how focus order, focus visibility, and focus recovery are handled.

### Naming and Announcements

Describe how controls, state changes, and dynamic updates are named or announced to assistive technology.

### Color, Contrast, and Motion

Describe the rules for contrast, color meaning, animation, and motion reduction.

### Zoom, Reflow, and Responsive Behavior

Describe how the project handles zoom, text scaling, reflow, and narrow layouts.

### Media, Captions, and Alternatives

Describe the project's expectations for media alternatives such as captions, transcripts, and text equivalents.

## Engineering Workflow

### Design and Implementation Rules

Describe the concrete implementation rules contributors should follow when changing accessibility-relevant surfaces.

### Automated Testing

Document the automated accessibility checks used by this project.

### Manual Testing

Document the manual accessibility checks required for relevant changes.

### Assistive Technology Coverage

Document the assistive technologies, browsers, devices, or operating environments the team actively tests.

### Definition of Done

Describe what must be true before accessibility-relevant work is considered ready for review or merge.

## Known Gaps

### Current Exceptions

List known accessibility limitations, unsupported surfaces, or temporary exceptions.

### Planned Remediation

Describe how known accessibility gaps are tracked or remediated.

### Ownership

Describe who is responsible for keeping this document and its follow-up work current.

## User Support and Reporting

### Feedback Path

Describe how users or maintainers should report accessibility issues or request support.

### Triage Expectations

Describe how accessibility reports should be acknowledged, triaged, or escalated.

## Verification and Evidence

### CI Signals

List the CI or automation signals that support the project's accessibility claims.

### Audit Cadence

Describe how often accessibility review happens and when it is required.

### Review History

Record notable accessibility-review checkpoints, updates, or resets.
```

## Proposed `maintain-project-contributing` Expansion

### Direction

Add one new required subsection under `Development Expectations`:

- `Accessibility Expectations`

This subsection should keep the contributor contract short and should point contributors back to the canonical `ACCESSIBILITY.md` instead of duplicating the entire accessibility document.

### Proposed Template Text

```md
### Accessibility Expectations

Contributors must keep changes aligned with the project's accessibility contract in [`ACCESSIBILITY.md`](./ACCESSIBILITY.md).

If a change affects UI semantics, input behavior, focus flow, labels, announcements, motion, contrast, zoom behavior, content structure, or assistive-technology compatibility, verify the affected surface against the documented accessibility standards before asking for review.

If a change introduces a new accessibility limitation, exception, or remediation plan, update `ACCESSIBILITY.md` in the same pass unless maintainers have explicitly agreed on a different tracking path.
```

### Schema Changes Needed

Update the `maintain-project-contributing` base schema to:

- require `Accessibility Expectations` under `Development Expectations`
- add alias handling if needed for migration paths such as `Accessibility` or `A11y Expectations`
- update the template asset, config template, `SKILL.md`, and tests together

## Proposed Implementation Sequence

1. Add the new `maintain-project-accessibility` skill directory with baseline files.
2. Clone and adapt the existing document-maintenance Python workflow implementation pattern.
3. Add the accessibility schema config and bootstrap template.
4. Add skill-local references for schema, customization, style rules, output contract, and positioning guidance.
5. Add tests covering clean runs, missing-file bootstrap, non-canonical headings, placeholder detection, and unsupported compliance claims.
6. Extend `maintain-project-contributing` schema, template, docs, and tests to require `Accessibility Expectations`.
7. Update repo-level docs that list active skills and maintainer workflows.
8. Update plugin metadata version and release notes when the implementation actually ships.

## Affected Files When Implementation Starts

### New Files

- `skills/maintain-project-accessibility/**`
- optional release notes once shipped

### Existing Files To Update

- `README.md`
- `ROADMAP.md`
- `docs/maintainers/workflow-atlas.md`
- `docs/maintainers/reality-audit.md`
- `skills/maintain-project-contributing/SKILL.md`
- `skills/maintain-project-contributing/assets/CONTRIBUTING.template.md`
- `skills/maintain-project-contributing/config/contributing-customization.template.yaml`
- `skills/maintain-project-contributing/references/section-schema.md`
- `skills/maintain-project-contributing/tests/test_maintain_project_contributing.py`
- `.codex-plugin/plugin.json`

## Validation Expectations For The Implementation Pass

- `uv sync --dev`
- `uv run pytest`
- targeted verification for both document-maintenance skills:
  - `maintain-project-accessibility`
  - `maintain-project-contributing`

## Open Questions

- Whether the baseline skill should require a `Feedback Path` even for private internal repos with no external user channel
- Whether `Assistive Technology Coverage` should be required or allowed to explicitly say "not yet defined"
- Whether future work should add a separate public accessibility-statement skill instead of overloading `ACCESSIBILITY.md`
