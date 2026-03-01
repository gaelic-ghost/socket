---
name: github-repo-defaults
description: Apply consistent default GitHub repository settings when creating a new GitHub remote, including generated description text and topic seeding. Use when creating or publishing a local repo to GitHub and the user wants their standard defaults applied.
---

# GitHub Repo Defaults

Create or update a GitHub repository with a stable default settings baseline.

## Workflow

1. Resolve target repository (`owner/name`) and remote name (`origin` unless the user specifies otherwise).
2. Generate a description candidate from local project metadata.
3. Generate initial topic candidates from repository signals (language and tooling files).
4. Apply repository settings and topics via `gh` CLI.
5. Show a concise summary of what was changed.

## Defaults Baseline

Apply these defaults unless the user explicitly asks otherwise:

- Visibility: private.
- Issues: enabled.
- Wiki: disabled.
- Projects: disabled.
- Discussions: disabled.
- Delete branch on merge: enabled.
- Always suggest updating pull request branches: enabled.
- Auto-close issues with merged linked pull requests: enabled.
- Merge strategy: squash only (`allow_squash_merge=true`, merge/rebase disabled).

## Description Heuristics

Use the first available source in this order:

1. First Markdown heading in `README.md` (without the leading `#`), plus a short purpose phrase from the first non-empty paragraph.
2. `description` from `package.json` or `pyproject.toml`.
3. Fallback: `<repo-name>: development project`.

Keep descriptions short and concrete (around 80-140 characters).

## Topic Heuristics

Start with normalized repo-name tokens, then add ecosystem topics inferred from files:

- `Package.swift` -> `swift`, `swiftpm`
- `pyproject.toml` -> `python`
- `package.json` -> `javascript` or `typescript` (use `typescript` when `tsconfig.json` exists)
- `Cargo.toml` -> `rust`
- `Dockerfile` -> `docker`
- `.github/workflows/*.yml` -> `github-actions`

Keep 3-8 topics total, lowercase, no duplicates.

## Command Patterns

Run from the target repository root.
`<skill-dir>` is the directory containing this `SKILL.md` file.

Primary one-command path:

```bash
<skill-dir>/scripts/apply_defaults.sh
```

Useful overrides:

```bash
<skill-dir>/scripts/apply_defaults.sh \
  --owner <owner> \
  --visibility private \
  --topics "topic-a,topic-b"
```

```bash
<skill-dir>/scripts/apply_defaults.sh --dry-run
```

Create new GitHub repo + remote:

```bash
gh repo create <owner>/<name> \
  --private \
  --source . \
  --remote origin \
  --push
```

Apply baseline settings:

```bash
gh api --method PATCH /repos/<owner>/<name> \
  -f description="<description>" \
  -F has_issues=true \
  -F has_wiki=false \
  -F has_projects=false \
  -F has_discussions=false \
  -F delete_branch_on_merge=true \
  -F allow_update_branch=true \
  -F auto_close_issues=true \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false
```

Apply topics:

```bash
gh api --method PUT /repos/<owner>/<name>/topics \
  -F names[]="<topic-1>" \
  -F names[]="<topic-2>" \
  -F names[]="<topic-3>"
```

Verify:

```bash
gh repo view <owner>/<name> --json description,visibility,repositoryTopics
```

## Notes

- If the repository already exists, skip creation and apply settings directly.
- If the user requests public visibility, call that out explicitly before applying.
- If topic inference is ambiguous, prefer fewer, higher-signal topics.
