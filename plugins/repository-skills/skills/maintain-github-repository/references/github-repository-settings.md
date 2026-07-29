# GitHub Repository Settings

Use this reference when a repository is hosted on GitHub and the user asks to
create, bootstrap, sync, audit, or update repository settings.

## Audit Before Mutation

1. Confirm the repository, owner, default branch, visibility, and current user
   permissions.
2. Read the repository's `AGENTS.md`, contributor policy, release workflow, and
   current GitHub settings before choosing a baseline.
3. Report current values, recommended values, unavailable settings, and planned
   changes separately.
4. Treat visibility changes as explicit approval-gated operations. Never infer
   a visibility change from a settings audit.
5. Apply available settings first. Record plan, visibility, permission, or API
   limitations instead of changing visibility or weakening the baseline.

## Recommended Baseline

Use narrower repo policy when it exists. Otherwise, prefer this baseline for a
maintained software repository:

- issues enabled
- wiki, projects, and discussions disabled unless the repository actively uses
  them
- delete pull-request branches after merge enabled
- pull-request branch updates enabled
- auto-merge enabled when the repository uses pull-request automation
- merge commits and rebase merges enabled
- squash merges enabled unless repository policy intentionally narrows merge
  methods
- auto-close linked issues enabled when supported
- Dependabot alerts and security updates enabled
- secret scanning and push protection enabled when supported
- private vulnerability reporting enabled for public repositories
- web commit sign-off required when the repository uses DCO or another sign-off
  policy

Do not require approving reviews by default for a single-maintainer repository.
Do not add branch restrictions that block the owner or maintainer's documented
direct-push workflow.

## Branch Protection

Branch protection must match the repository's real workflow:

- require the exact status-check context emitted by CI; for the managed
  repo-maintenance workflow, require `validate`
- keep force pushes and branch deletion disabled unless repo policy explicitly
  allows them
- use strict required checks only when keeping pull-request branches current is
  acceptable for that repository
- do not require pull-request reviews by default when the repository has no
  independent reviewer
- preserve documented owner or maintainer direct pushes when that is an
  intentional workflow
- distinguish branch protection from DCO sign-off enforcement; GitHub's web
  sign-off setting covers web commits only, while command-line sign-off needs a
  separate status check or contribution gate

## Apply Surfaces

Use `gh repo edit` for supported repository toggles:

```bash
gh repo edit OWNER/REPO \
  --enable-issues=true \
  --enable-wiki=false \
  --enable-projects=false \
  --enable-discussions=false \
  --delete-branch-on-merge=true \
  --allow-update-branch=true \
  --enable-auto-merge=true \
  --enable-merge-commit=true \
  --enable-rebase-merge=true \
  --enable-squash-merge=true
```

Use `gh api` for settings that are not exposed by `gh repo edit`, including
Dependabot security updates, private vulnerability reporting, web commit
sign-off, auto-closing linked issues, and branch protection details. Read the
current REST documentation before constructing mutation requests.

Prefer repository-owned `.github/dependabot.yml`, workflow files, `CODEOWNERS`,
`SECURITY.md`, and contribution policy when the requested behavior is
file-backed rather than a server-side toggle.

## Verification

After applying settings:

1. Re-read repository settings through `gh repo view`, `gh api`, and branch or
   ruleset endpoints.
2. Verify required status-check names against an actual recent check run.
3. Verify Dependabot, secret scanning, push protection, private vulnerability
   reporting, and web sign-off independently.
4. Record settings that could not be applied and why.
5. Keep the repository's visibility unchanged unless the user separately
   approved a visibility transition.

## Official Sources

- [GitHub CLI `gh repo edit`](https://cli.github.com/manual/gh_repo_edit)
- [Managing the commit signoff policy](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-the-commit-signoff-policy-for-your-repository)
- [Configuring Dependabot security updates](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates)
- [Configuring private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository)
- [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [REST API endpoints for repositories](https://docs.github.com/en/rest/repos/repos)
- [REST API endpoints for protected branches](https://docs.github.com/en/rest/branches/branch-protection)
