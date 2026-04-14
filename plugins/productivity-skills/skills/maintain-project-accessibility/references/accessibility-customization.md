# Accessibility Customization

Use `config/accessibility-customization.template.yaml` as the baseline schema contract for `ACCESSIBILITY.md`.

Downstream repos or narrower plugins may customize:

- required top-level sections
- section order
- required subsections
- section alias mappings for migration
- subsection alias mappings for migration
- default section and subsection template text

Customization rules:

- Keep the configured schema hard-enforced in both `check-only` and `apply`.
- Use aliases only as migration hints, not as canonical output.
- Do not remove `Known Gaps` or `Verification and Evidence` unless a narrower downstream plugin truly owns a different accessibility contract.
