# API Customization

The base API-reference contract is defined in `../config/api-customization.template.yaml`.

Downstream specializations may customize:

- canonical section order
- required sections
- required subsection structure
- section and subsection aliases
- section and subsection scaffold text

The base skill always requires:

- a top-level title and short summary
- a `Table of Contents`
- deterministic normalization to the configured schema

Use a project-local `config/api-customization.yaml` or `--config <path>` override when a downstream plugin needs a narrower or expanded API reference structure.
