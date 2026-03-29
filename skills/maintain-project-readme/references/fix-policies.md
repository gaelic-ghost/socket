# Fix Policies

## Allowed Automatic Fixes

- add missing required sections
- add the canonical profile-specific section when repo-profile detection is clear
- normalize section ordering
- add or repair `### Motivation` under `## Overview`
- add or refresh a compact H2-only table of contents when warranted
- replace missing title/value-proposition structure with grounded repo-neutral wording
- fill empty required sections with neutral scaffolding that does not invent commands or product claims

## Disallowed Automatic Fixes

- invent setup, test, deploy, or release commands
- invent audience claims, performance claims, or feature guarantees
- edit files other than the target `README.md`
- rewrite specialized skills/plugin repository READMEs

## Review Bias

- prefer preserving good existing prose over normalization for its own sake
- prefer small structural edits over large rewrites
- do not create new profile-specific sections when the repo profile is ambiguous
- report unsupported command examples instead of guessing replacements
