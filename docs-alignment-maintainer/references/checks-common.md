# Common Checks

## Repository Discovery

- Walk the workspace recursively.
- Treat directory as project root when any is true:
  - `.git` directory exists.
  - `.git` file exists.
- After identifying a root, do not descend into child directories for nested root detection.
- Skip excluded paths and all descendants.

## Candidate Docs

Primary targets:
- `README.md`
- `ROADMAP.md`
- `CONTRIBUTING.md`
- `docs/**/*.md`
- `docs/*.md`

## Generic Alignment Checks

- Detect mismatch between manifest/tooling evidence and documented commands.
- Detect package manager drift in command examples.
- Detect missing minimal run/test guidance when a runnable project is evident.

## Severity

- `high`: direct contradiction of canonical package manager/tooling.
- `medium`: missing expected run/test guidance.
- `low`: wording drift where intent remains mostly clear.

## Fix Safety

Auto-fix only when there is explicit evidence and bounded replacement surface.
