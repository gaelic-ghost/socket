# README Configuration Schema

Persistent README customization for `maintain-project-readme` is defined in:

- Template defaults: `config/readme-customization.template.yaml`
- User or downstream overrides: explicit `--config <path>` or project-local `config/readme-customization.yaml`

## Top-level fields

- `schemaVersion`: integer schema version (`1`)
- `isCustomized`: `true` when the loaded config is an override rather than only the built-in template
- `profile`: short profile label such as `base`, `python-library`, or `typescript-service`
- `settings`: README schema behavior controls

## `settings` fields

- `preservePreamble`: boolean
- `allowAdditionalSections`: boolean
- `requiredSections`: ordered list of exact canonical H2 headings
- `sectionOrder`: ordered list of exact canonical H2 headings used for normalization
- `requiredSubsections`: map of H2 heading to ordered list of exact canonical H3 headings
- `sectionAliases`: map of canonical H2 heading to alias heading list used for migration
- `sectionTemplates`: map of H2 heading to neutral scaffolding text
- `subsectionTemplates`: map of `Parent/Child` to neutral scaffolding text

## Runtime Behavior

- The merged config is authoritative for both `check-only` and `apply`.
- `requiredSections` and `sectionOrder` should describe the same canonical block.
- Alias headings are migration hints only and must not remain in canonical output after apply.
- The base contract treats `Table of Contents` as required unconditionally.
- Unknown keys should be tolerated but ignored unless a downstream plugin explicitly documents them.
