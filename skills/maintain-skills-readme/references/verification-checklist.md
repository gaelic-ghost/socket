# Verification Checklist

- No TODO/TBD placeholders remain.
- Section presence/order matches profile requirements.
- `## Table of Contents` exists where required and is compact (H2 links only, no nested bullets).
- `## Install individually by Skill or Skill Pack` exists where required.
- `## Update Skills` exists and includes `npx skills check` plus `npx skills update`.
- `## More resources for similar Skills` exists where required.
- Required discoverability `###` subsections are present and canonically named.
- Optional extra `###` subsections, if any, appear only after `Then ask your Agent for help finding a skill for "" or ""`.
- `## Keywords` exists where required.
- Install commands are syntactically valid.
- Install commands use current syntax (`--all`, `--skill`); legacy `@skill` syntax is rewritten.
- `--skill` references map to real `SKILL.md` directories.
- Relative markdown links resolve.
- No duplicated install blocks unless intentional.
- README edits only (no non-doc changes).
