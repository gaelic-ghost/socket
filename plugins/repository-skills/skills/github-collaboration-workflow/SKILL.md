---
name: github-collaboration-workflow
description: Prepare and maintain GitHub pull requests, reviews, issues, CI triage, and durable handoffs. Use for collaboration work after local Git changes exist; not for GitHub settings or release publication.
---

# GitHub Collaboration Workflow

## Purpose

Own the collaboration layer around a change: pull requests, review and comment
triage, issue linkage, CI status, and durable handoffs. Keep local Git,
GitHub-settings, and release operations with their focused owners.

## Workflow

1. Confirm the exact repository, branch, base branch, current `git status`,
   remote visibility, and `gh` authentication before a remote action.
2. Read repository contribution and review policy. Inspect existing pull
   requests and issues before creating duplicates.
3. Prepare a PR only after the change is committed, validated proportionately,
   and pushed with explicit authority. Use a concise body that explains intent,
   risk, and verification; link the governing issue when one exists.
4. Inspect CI checks, reviews, and unresolved comments as separate gates. Name
   failures, requested changes, and unknown states precisely.
5. Address valid review feedback in the owning branch; route broader follow-up
   to the repository's roadmap or issue system. Re-read the changed thread and
   checks before reporting it resolved.
6. For an external wait, do one bounded snapshot. Use the host's supported
   continuation mechanism no sooner than five minutes later; do not keep a
   shell watch or poll loop running.
7. Merge, label, close, reopen, or delete remote work only with explicit
   authority or a repository-owned release contract. Verify the resulting
   GitHub state after each mutation.

## Boundaries

- Route local branch, commit, rebase, conflict, and recovery work to
  `git-workflow`.
- Route GitHub server settings, rulesets, and security configuration to
  `maintain-github-repository`.
- Route protected-main release PRs, tags, releases, and branch-accounting
  cleanup to `maintain-project-repo`.
- Keep credentials, private issue content, and security findings out of public
  PR bodies and reports.

## Hermes Notes

This is portable guidance. Verify `gh` availability and authentication before
remote actions. On a pending CI or review gate, Hermes uses a self-contained
`cronjob` delivered to the origin session with `attach_to_session=true`; the
packet must include repository, branch, PR, commit, gate, and safe inspection.
