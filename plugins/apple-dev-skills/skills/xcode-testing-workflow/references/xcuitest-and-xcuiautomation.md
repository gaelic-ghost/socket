# XCUITest and XCUIAutomation-Oriented Mechanics

## Core stability rules

- Prefer explicit state waits such as `waitForExistence(timeout:)`, `waitForNonExistence(timeout:)`, and related state checks over fixed sleeps.
- Keep element lookup grounded in stable semantics such as accessibility labels, values, roles, and identifiers, instead of brittle view-order assumptions.
- Use `XCTContext.runActivity(named:block:)` to break long UI tests into named substeps so reports stay readable.

## Interruption handling

- Use UI interruption monitors only when unrelated system or app UI blocks the workflow under test.
- Do not treat interruption monitors as the default way to handle expected modal steps that are part of the workflow.
- Remove or simplify stale monitors when they are papering over a test design problem instead of handling a real intermittent interruption surface.

## Attachments and evidence

- Capture screenshots, logs, strings, or other attachments when they materially improve post-failure diagnosis.
- Keep attachments meaningful and named clearly enough that the test report explains the failure instead of adding generic noise.

## Launch setup

- Keep launch arguments and environment variables explicit when UI state, feature flags, locale, accessibility matrices, or deterministic fixtures depend on them.
- Prefer `.xctestplan` when those launch settings are part of a repeatable verification matrix instead of a one-off local run.

## Review questions

- What makes this UI test stable?
- What evidence will a maintainer get when it fails?
- Is the test depending on an unrelated interruption or trying to hide a real app-state problem?
