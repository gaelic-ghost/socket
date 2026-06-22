# Permissions And Artifacts

Last checked against Apple developer pages and WWDC26 transcripts on 2026-06-22.

## Permission Boundary

Name what the agent may do before granting tools:

- read project files
- edit source files
- change project settings, entitlements, signing, or file membership
- build or run the app
- run tests
- render previews
- inspect devices or simulators
- use shell commands
- access provider credentials or account-backed services

Do not grant broader permissions to work around unclear setup. Fix setup uncertainty first.

## Plan-First Bias

Use plan-first workflows for:

- architecture-sensitive changes
- broad refactors
- beta-SDK behavior
- project settings, entitlements, signing, or file membership
- localization changes across many files
- work that may require Device Hub, previews, or test iteration

Xcode 27 transcripts show plan mode gathering context before implementation and producing reviewable plans. Preserve that review boundary instead of asking an agent to immediately edit when the decision space is still open.

## Reviewable Artifacts

Treat agent-produced artifacts as evidence, not as proof of correctness. Review:

- source diffs
- new files
- generated project or package files
- rendered previews
- screenshots or videos
- build logs and issue lists
- test output
- localization changes in String Catalogs and XLIFF exports

When artifacts change tracked project state, commit them with the branch after ordinary review and validation.

## Credential Safety

Do not store provider API keys, auth tokens, or private credentials in repository files, app binaries, examples, generated configuration, screenshots, or logs.

If a third-party model provider needs credentials, use the provider's documented secure setup path and keep app-side access token flow separate from development-time Xcode setup.

## Handoffs

This skill names the permission boundary and setup path. It does not run validation:

- build and preview validation: `xcode-build-run-workflow`
- tests: `xcode-testing-workflow`
- current docs lookup: `explore-apple-swift-docs`
