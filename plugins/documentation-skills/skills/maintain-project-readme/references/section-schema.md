# Section Schema

## Canonical Base README Structure

The canonical base README structure is defined in `config/readme-customization.template.yaml`.

## Hard-Enforced Rules

- Top-level canonical sections use exact `##` heading names from the configured schema.
- Required subsections use exact `###` heading names from the configured schema.
- Canonical sections appear in canonical order.
- `Overview` owns the canonical `Status`, `What This Project Is`, and `Motivation` subsections.
- `Development` is a short handoff to contributor documentation, usually `CONTRIBUTING.md`; setup, workflow, validation, release, branch, and review procedures do not belong in the base README contract.
- `Table of Contents` is always required in the base workflow.
- Additional repo-specific sections may exist, but they follow the canonical block unless a customization override defines a different order.
- `Table of Contents` is generated from H2 headings only and should use the canonical heading names that appear in the README.
- The summary line directly beneath the title is part of the schema contract, not optional polish.

## Alias Policy

- Alias headings may be used as migration hints during apply mode.
- Alias headings are not canonical output.
- If a README uses an alias such as `Getting Started` where the canonical schema expects `Quick Start`, the audit should report the non-canonical heading and apply mode should migrate it to the configured canonical heading name.

## Downstream Customization

- Downstream plugins may add, remove, or reorder sections through the customization config.
- Downstream plugins may add required subsections and alias mappings.
- Even when customized, the configured schema remains hard-enforced for both `check-only` and `apply`.
