# Code Coverage Contract

Code coverage is execution evidence: it shows which instrumented code ran during a test run. It does not prove behavior is correct, tests assert the right outcomes, or UI and device paths are adequately verified.

## Default Policy

- Report coverage by target and file, and include function-level detail when the tool provides it.
- Keep test failures, coverage-collection failures, and missing-report failures as separate results.
- Default to reporting only. Do not invent a global coverage percentage, fail a build, exclude a source path, or claim changed-line coverage without an explicit repository policy.
- Treat generated, vendored, test-target, and platform-glue sources as visible in the first report. Exclude them only with a checked-in, human-readable reason.
- Do not commit generated coverage reports by default. Keep local reports ephemeral and upload CI reports only when that repository's CI policy asks for it.

## Required Evidence Packet

Every coverage result should state the toolchain and coverage command; configuration, scheme or package, and destination when applicable; report artifact path and format; target and file summary; exclusions and their reason; whether the result is comparable with a baseline; and test, collection, and report-extraction failures independently.

## Comparison And Gates

Compare coverage only when the source revision, toolchain, build configuration, selected targets, destination, and exclusion policy are compatible. A raw project-wide percentage is not a substitute for changed-file or changed-line evidence.

Add a CI gate only after the repository chooses one concrete metric: an overall minimum, target minimum, changed-file minimum, or changed-line minimum. Record the policy and allowed exceptions in the repository; keep the Apple Dev Skills default report-only.
