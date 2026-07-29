---
name: maintain-github-repository
description: Audit or align a GitHub repository's server-side settings, including repository features, merge methods, branch protection or rulesets, Dependabot, secret scanning, push protection, private vulnerability reporting, DCO web sign-off, and related defaults. Use when the user asks to configure a new GitHub repo, apply normal repository settings, inspect settings drift, audit branch protection or security settings, or change specific GitHub repository policy. Do not use for ordinary local Git commits, branches, pushes, pull-request prose, code review replies, or release choreography.
---

# Maintain GitHub Repository

## Purpose

Audit or align server-side GitHub repository settings without mixing those
changes into local Git operations or release automation. The default path is a
read-only audit. Apply changes only when the user requests mutation.

## When To Use

- Use this skill when creating or configuring a GitHub repository.
- Use this skill when the user asks to apply their normal GitHub repository
  defaults.
- Use this skill when auditing repository features, merge methods, security
  automation, sign-off requirements, branch protection, or rulesets.
- Use this skill when GitHub settings may have drifted from repo policy.
- Use this skill when a bootstrap or sync workflow reaches the GitHub remote
  configuration step.
- Do not use this skill for local commits, branches, rebases, merges, pushes,
  pull-request bodies, review replies, tags, or GitHub release creation.
- Use `maintain-project-repo` for protected-main releases, publishing, tags,
  GitHub release objects, release cleanup, and branch accounting.
- Use `maintain-project-contributing` when the repository's DCO, contributor
  grant, or sign-off documentation needs to change.

## Workflow

1. Resolve the repository:
   - confirm `owner/repo`, default branch, visibility, and current user
     permissions
   - verify the target is the repository the user intended
   - read repo-local `AGENTS.md`, contribution policy, security policy, and
     release guidance before selecting a baseline
2. Load `references/github-repository-settings.md`.
3. Audit before mutation:
   - read supported repository settings with `gh repo view` and `gh api`
   - inspect branch protection or rulesets separately from general repo
     settings
   - inspect Dependabot, secret scanning, push protection, private
     vulnerability reporting, web commit sign-off, and auto-close behavior
     independently
   - verify required status-check names against actual recent check runs when
     branch protection depends on CI
4. Classify every relevant setting as:
   - `aligned`
   - `drifted`
   - `unavailable`
   - `unknown`
   - `not applicable`
5. Report current values, recommended values, unavailable settings, and exact
   planned mutations separately.
6. Apply only requested changes:
   - use `gh repo edit` for supported general toggles
   - use current documented `gh api` endpoints for security, sign-off,
     auto-close, branch-protection, and ruleset settings
   - prefer file-backed `.github/dependabot.yml`, `CODEOWNERS`, `SECURITY.md`,
     workflow, and contribution-policy changes when the behavior is owned by
     repository files
   - keep visibility changes separately approval-gated
   - preserve documented maintainer direct-push workflows
7. Re-read every changed setting and report the verified result.

## Inputs

- `repository`: optional `owner/repo`; default to the current checkout's GitHub
  remote only when unambiguous
- `mode`: `audit` or `apply`
- `requested_changes`: optional explicit settings changes
- `baseline`: repo-local policy or the recommended baseline reference
- Defaults:
  - `mode=audit`
  - visibility remains unchanged
  - no settings are mutated without an apply request

## Output

- `Repository`: exact `owner/repo`, visibility, and default branch
- `Current Settings`: observed values
- `Recommended Settings`: repo-policy or fallback baseline
- `Unavailable Settings`: plan, visibility, permission, or API limitations
- `Planned Changes`: exact mutations, empty in audit-only mode
- `Applied Changes`: mutation results, apply mode only
- `Verification`: post-mutation values or audit evidence
- `Follow-Up`: file-backed policy, DCO check, CI check-name, release, or
  contributor-doc work that belongs to another skill

## Guards

- Never infer or bundle a repository visibility change.
- Never weaken security settings just to make an audit pass.
- Never require approving reviews when the repo has no independent reviewer
  unless the user explicitly wants that policy.
- Never block a documented maintainer direct-push workflow accidentally.
- Never guess a required status-check context from a workflow display name.
- Do not treat GitHub web sign-off as command-line DCO enforcement.
- Apply all available requested settings before reporting settings that GitHub
  cannot expose for the current plan or visibility.
- Keep credentials, tokens, and private vulnerability details out of reports.

## Trigger Evaluation

Use `references/trigger-eval.md` to verify that settings and policy requests
trigger this skill while ordinary Git and release requests route elsewhere.

## References

- `references/github-repository-settings.md`
- `references/trigger-eval.md`
