# README Customization Guide

## Why Customization Exists

`maintain-project-readme` is the general template layer for ordinary project READMEs. The base schema is intentionally strict, but downstream plugins can adapt it through explicit config instead of forking the workflow into unrelated variants.

## Canonical Base Defaults

The built-in template config in `config/readme-customization.template.yaml` defines:

- title plus one-line summary
- always-required H2-only table of contents
- canonical top-level sections
- required `Overview` subsections
- a short `Development` handoff to contributor documentation, usually `CONTRIBUTING.md`

## Supported Customization Knobs

- `profile`
  - Human-readable label for the active schema profile.
- `settings.requiredSections`
  - Exact canonical top-level sections that must exist.
- `settings.sectionOrder`
  - Exact canonical top-level order used for normalization.
- `settings.requiredSubsections`
  - Exact required `###` subsections keyed by parent H2 section.
- `settings.sectionAliases`
  - Migration hints from non-canonical headings to canonical output headings.
- `settings.sectionTemplates`
  - Neutral scaffolding text for missing required sections.
- `settings.subsectionTemplates`
  - Neutral scaffolding text for missing required subsections.
- `settings.allowAdditionalSections`
  - Whether repo-specific extra sections are preserved after the canonical block.
- `settings.preservePreamble`
  - Whether content before the first H2 is preserved during apply mode.

## Customization Policy

- Downstream plugins may add sections, subsections, alias mappings, and scaffolding.
- Downstream plugins may reorder canonical sections.
- Downstream plugins should preserve the table of contents as part of the shared base structure.
- The configured structure remains authoritative once loaded.
- Apply mode should normalize into the configured schema, not negotiate with existing README drift.
