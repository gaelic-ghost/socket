# Trigger Evaluation

## Should Trigger

- Release version 1.4.0.
- Publish this package.
- Tag this commit and create the GitHub release.
- Prepare this branch for a protected-main release.
- Run the release workflow and clean up the merged branch.
- Install the repo-maintenance toolkit.
- Refresh our validation, sync, and release scripts.
- Use the checked-in release notes for this patch release.

## Should Not Trigger

- Explain this function.
- Fix this local test failure.
- Update the README.
- Commit and push this ordinary edit.
- Write the pull-request body.
- Audit branch protection and Dependabot settings.
- Apply my normal GitHub repository settings.
- Update `CONTRIBUTING.md`.

## Routing

- GitHub repository settings audit and alignment route to
  `maintain-github-repository`.
- Ordinary documentation work routes to the owning document-maintenance skill.
- Ordinary local Git work follows repo-local Git guidance without invoking the
  full release lifecycle.
