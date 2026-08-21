# Project Documentation Prompts

## Audit

Run `just docs-check`. Report findings for README, CONTRIBUTING, AGENTS, and
ROADMAP in that order, including responsibility drift. Do not mutate files.

## Apply

Run `just docs-apply`. Apply the planned four-document transaction atomically,
verify the result, and require a second apply to be byte-identical.

These are the only supported documentation operations. Never split work by
file or add a project-specific schema, status vocabulary, or fix policy.
