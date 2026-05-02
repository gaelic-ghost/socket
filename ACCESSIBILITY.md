# Accessibility

Accessibility expectations for the `socket` superproject's root documentation, maintainer workflows, and metadata surfaces.

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

`socket` targets accessible documentation and maintainer-facing project surfaces, but it does not claim verified conformance to a formal accessibility standard.

### Scope

This document covers the root superproject surfaces in this repository:

- Markdown documentation such as [README.md](./README.md), [AGENTS.md](./AGENTS.md), [ROADMAP.md](./ROADMAP.md), and root maintainer docs under [`docs/`](./docs/)
- Root repository metadata such as [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)
- Root maintainer automation such as [`scripts/validate_socket_metadata.py`](./scripts/validate_socket_metadata.py) and [`.github/workflows/validate-socket-metadata.yml`](./.github/workflows/validate-socket-metadata.yml)

This document does not redefine accessibility policy for child repositories under [`plugins/`](./plugins/). Those repositories may maintain their own narrower accessibility contracts.

### Accessibility Goals

The root `socket` layer should stay understandable and operable for maintainers working through text-first tools, GitHub, local editors, terminals, and assistive technologies. In practice, that means keeping root docs structurally clear, preserving meaningful headings and lists, using descriptive link text and human-readable log output, and avoiding root-level workflow changes that make the superproject harder to navigate non-visually.

## Standards Baseline

### Target Standard

For the root superproject layer, `socket` targets WCAG 2.2 AA principles as a documentation and workflow baseline where they reasonably apply to repository content, static documentation, generated logs, and maintainer-facing automation output.

### Conformance Language Rules

This repository may say that its root documentation and maintainer workflow surfaces target WCAG 2.2 AA-inspired practices. It must not claim formal WCAG conformance, legal compliance, or audited accessibility status for the superproject unless that claim is backed by documented review evidence in this file.

### Supported Platforms and Surfaces

This accessibility contract currently applies to:

- GitHub-rendered Markdown for the root repository
- local Markdown viewing in ordinary editors
- terminal-readable output from the root validation script
- CI logs produced by the root GitHub Actions workflow

Because `socket` is a superproject rather than a shipped application, there is no separate root web UI, desktop UI, or mobile UI covered by this document today.

## Accessibility Architecture

### Semantic Structure

Root documentation should keep real heading hierarchy, ordered and unordered lists, fenced code blocks, and meaningful section titles so GitHub, editors, and assistive technologies can expose the structure correctly. Docs should prefer descriptive links over bare URLs where the link target has a specific role in the repo.

### Input and Keyboard Model

The root repository should remain fully usable from keyboard-first environments. Contributor workflows at the root level should not depend on pointer-only interactions, drag-and-drop-only actions, or GUI-only steps when an equivalent documented terminal path exists.

### Focus Management

`socket` does not ship an interactive root UI with custom focus management. The practical focus rule here is to preserve clear reading order in Markdown, avoid broken heading jumps, and keep docs organized so keyboard and screen-reader users can move predictably through the content.

### Naming and Announcements

Root scripts, workflow steps, validation failures, and documentation headings should use descriptive names that make the surface understandable without extra visual context. Operator-facing messages should identify what broke, which file or surface is involved, and the likely cause instead of using vague labels.

### Color, Contrast, and Motion

The root superproject should not rely on color alone to communicate meaning in documentation or generated summaries. Screenshots, diagrams, and other visual artifacts should include text labels or surrounding context that does not depend on color perception. Root docs should avoid animation-dependent explanations.

### Zoom, Reflow, and Responsive Behavior

Root documentation should remain readable under normal browser zoom and narrow layout behavior on GitHub. Prefer short paragraphs, flat list structures, and code blocks that are still understandable when horizontally scrolled.

### Media, Captions, and Alternatives

Root media assets live under [`docs/media/`](./docs/media/). Contributors should provide meaningful alt text plus adjacent text that explains the point of each screenshot, diagram, or recorded demo. If audio or video is ever added at the root level, include captions or a transcript where practical.

## Engineering Workflow

### Design and Implementation Rules

When editing root docs or maintainer automation:

- preserve heading structure and intentional document organization
- use descriptive labels for scripts, workflow steps, and validation errors
- keep command examples copyable and text-complete
- avoid adding root-level workflows that require inaccessible or undocumented GUI-only steps
- update accessibility-relevant root docs in the same pass when the superproject workflow meaningfully changes

### Automated Testing

The root repository does not currently run automated accessibility auditing tools. Its current automated evidence is structural:

- `uv run scripts/validate_socket_metadata.py` validates that the root marketplace wiring is present, readable, and correctly aligned with packaged plugin manifests
- [`.github/workflows/validate-socket-metadata.yml`](./.github/workflows/validate-socket-metadata.yml) runs that validation in CI on pushes to `main` and on pull requests

### Manual Testing

For accessibility-relevant root changes, contributors should manually review:

- heading hierarchy and section ordering in edited Markdown
- link text and table-of-contents accuracy
- code-block readability and command accuracy
- image alt text, adjacent media explanations, and relative media paths
- terminal output from root scripts for clarity and ambiguity
- GitHub-rendered formatting when a change significantly reshapes a root document

### Assistive Technology Coverage

The root repository does not currently keep a formally documented assistive-technology test matrix. The expected baseline is that root docs and script output remain usable in text-first environments, including screen readers that rely on semantic Markdown structure and terminals that expose plain text output.

### Definition of Done

Root documentation or maintainer-workflow changes are not ready for review until:

- the changed surface is structurally readable and semantically organized
- any new operator-facing message is descriptive and unambiguous
- root validation commands still pass when the change affects root automation or marketplace metadata
- this file is updated in the same pass if the root accessibility contract, known gaps, or verification story materially changed

## Known Gaps

### Current Exceptions

Current root-level gaps and limits:

- `socket` does not yet run automated accessibility tooling against its Markdown docs
- the root repo does not maintain a formal assistive-technology compatibility matrix
- accessibility expectations for child repositories are only covered here at the boundary level, not enforced uniformly across all nested repositories

### Planned Remediation

Known gaps should be addressed when the root maintainer workflow grows enough to justify stronger checks. That may include adding doc-focused linting or a documented manual review checklist if the superproject starts carrying more user-facing policy surfaces.

### Ownership

The root repository maintainers are responsible for keeping this document accurate when the root superproject workflow changes. Changes that materially affect root docs, validation, or maintainer automation should update this file in the same pass when the accessibility contract meaningfully changes.

## User Support and Reporting

### Feedback Path

Use the root repository's normal GitHub collaboration surfaces to report accessibility issues in the superproject layer. In practice, that usually means opening a GitHub issue or pull request against `gaelic-ghost/socket` with enough detail to identify the affected root doc, workflow, script output, or metadata surface.

### Triage Expectations

Accessibility reports should be treated as ordinary quality issues for the root superproject and scoped to the affected root surface first. If the report is really about a child repository under [`plugins/`](./plugins/), move the follow-up into the appropriate child repo or child-repo document set instead of leaving the concern ambiguously tracked at the superproject layer.

## Verification and Evidence

### CI Signals

Current root CI evidence:

- [`.github/workflows/validate-socket-metadata.yml`](./.github/workflows/validate-socket-metadata.yml)
- `uv run scripts/validate_socket_metadata.py`

These checks validate structural integrity for root marketplace metadata. They do not, by themselves, prove accessibility conformance.

### Audit Cadence

Root accessibility review should happen whenever:

- the root documentation structure changes substantially
- the root validator output changes materially
- the root GitHub workflow changes in a way that affects maintainer operability
- this document becomes stale relative to the root repo's actual workflow

### Review History

- 2026-05-02: Added root screenshot guidance after introducing README media under `docs/media/`.
- 2026-04-14: Added the first root `ACCESSIBILITY.md` for the `socket` superproject and documented the root-only accessibility boundary around docs, metadata, and maintainer automation.
