# API Config Schema

The API-reference configuration file is YAML and uses this top-level shape:

- `schemaVersion`
- `isCustomized`
- `profile`
- `settings`

The `settings` map supports:

- `preservePreamble`
- `allowAdditionalSections`
- `requiredSections`
- `sectionOrder`
- `requiredSubsections`
- `sectionAliases`
- `subsectionAliases`
- `sectionTemplates`
- `subsectionTemplates`

Practical rules:

- `requiredSections` defines the canonical top-level sections, excluding the title, summary, and `Table of Contents`.
- `sectionOrder` defines the enforced top-level ordering.
- `requiredSubsections` defines required `###` headings under specific `##` sections.
- `sectionAliases` and `subsectionAliases` allow bounded migration from older heading names into canonical names.
- `sectionTemplates` and `subsectionTemplates` provide the base scaffolding used during apply mode when content is missing.
