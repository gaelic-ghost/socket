# Fix Policies

## Allowed Automatic Fixes

- add missing canonical top-level sections from the configured schema
- add missing required subsections inside existing canonical sections
- normalize top-level section ordering into the configured canonical order
- migrate configured alias headings into canonical heading names
- add or refresh the required H2-only table of contents
- replace a missing title/summary block with grounded repo-neutral wording
- fill empty required sections or subsections with readable neutral scaffolding

## Disallowed Automatic Fixes

- invent quick-start, setup, workflow, validation, deploy, or release commands
- invent audience claims, performance claims, guarantees, or support promises
- rewrite healthy prose just to make it sound more generated
- edit files other than the target `README.md`
- rewrite specialized skills/plugin repository READMEs

## Review Bias

- prefer hard structural normalization over soft structural hints
- prefer preserving good existing prose within a section while normalizing the surrounding schema
- prefer alias migration over deleting useful content
- preserve preamble material before the first H2 when it remains coherent
- report placeholder-style content instead of pretending the repo provides facts that are not visible
