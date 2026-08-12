# Trigger Evaluation

## Should Trigger

- Apply my normal GitHub repository settings.
- Audit this repo's branch protection and Dependabot settings.
- Configure the GitHub settings for this new repository.
- Turn on private vulnerability reporting and push protection.
- Check whether web commit sign-off is enabled for our DCO policy.
- Align merge methods, issue tracking, and branch cleanup with our defaults.
- Why can I not enable this security setting on the repository?
- Verify that the `validate` status check is required on `main`.

## Should Not Trigger

- Commit and push these changes.
- Rebase this branch onto `main`.
- Write the pull-request body.
- Address this review comment.
- Release version 1.4.0.
- Tag this commit and create the GitHub release.
- Install the repo-maintenance toolkit.
- Update `CONTRIBUTING.md` with our DCO policy.

## Routing

- Local Git and pull-request mechanics follow repo-local Git guidance.
- Release, publish, tag, protected-main, cleanup, and branch-accounting requests
  route to `maintain-project-repo`.
- Contribution-document changes route to `maintain-project-contributing`.
