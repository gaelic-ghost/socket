---
name: resume-repo-line-items
description: Generate software-engineering resume line items from local repositories. Use when the user wants project-based resume bullets built from repos under ~/Workspace and filtered to GitHub-owned repos with tagged releases that are not forks, with collaboration-aware language and plaintext output.
---

# Resume Repo Line Items

Produce plaintext resume entries from local repositories in a consistent, professional format.

## Workflow

1. Scan repos under `~/Workspace` with strict selection rules.
2. Mark selected repos as collaborative when applicable.
3. Generate plaintext line items with one short summary and 3-6 bullets per repo.
4. Review output quality and adjust if a repo needs stronger technical or impact framing.

## Commands

Run from this skill directory.

```bash
scripts/scan_repos.py \
  --root ~/Workspace \
  --github-owner <github_owner> \
  --fork-check github \
  --output /tmp/resume_repo_scan.json

scripts/generate_resume_items.py \
  --scan-json /tmp/resume_repo_scan.json \
  --output /tmp/resume_line_items.txt
```

If GitHub fork checks are unavailable (for example, missing `gh` auth), run:

```bash
scripts/scan_repos.py \
  --root ~/Workspace \
  --github-owner <github_owner> \
  --fork-check none \
  --output /tmp/resume_repo_scan.json
```

In that mode, fork status is not validated. State that limitation before finalizing output.

## Selection Rules

Include a repository only if all are true:

- Has at least one GitHub remote owned by the configured GitHub owner.
- Has at least one git tag.
- Is not a fork (`--fork-check github`) unless fork checks are explicitly disabled.

Mark a selected repository as `collaborative` if either is true:

- Contributors besides the user are detected in git shortlog.
- `AGENTS.md` is present in the repo root.

## Output Contract

For each selected repo, produce:

- Project heading line (`<repo-name>` and `[Collaborative]` when applicable).
- One short summary sentence.
- 3-6 bullets.

Each bullet must contain:

- One or more high-value tools/languages/systems.
- What they were used to accomplish.
- Positive result or expected impact.

For collaborative repos:

- Include teamwork or collaboration in some bullets.
- Include leadership language in some bullets.
- Include communication language for a subset of collaborative repos.

## Style Constraints

- Professional, concise, matter-of-fact.
- Third person.
- Avoid repeatedly using the user's name.
- Keep bullets at 1-3 sentences.

## Quality Pass

Use [references/bullet-quality.md](references/bullet-quality.md) before final output.

Check for:

- Concrete tools and actions in every bullet.
- Clear outcome language in every bullet.
- Collaboration/leadership/communication coverage where required.
- No first-person phrasing.
