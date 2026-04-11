# AGENTS Customization

The base AGENTS contract is defined in `../config/agents-customization.template.yaml`.

Downstream specializations may customize:

- canonical section order
- required sections
- required subsection structure
- section and subsection aliases
- section and subsection scaffold text

The base skill always requires:

- a top-level title and short repo-local preamble
- deterministic normalization to the configured schema

Use a project-local `config/agents-customization.yaml` or `--config <path>` override when a downstream plugin needs a narrower or expanded AGENTS structure.
