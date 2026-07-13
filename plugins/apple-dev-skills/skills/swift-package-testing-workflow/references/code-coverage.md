# SwiftPM Code Coverage

Use SwiftPM coverage for a package-first test surface. Follow the shared [`code-coverage-contract`](../../../shared/references/code-coverage-contract.md) for evidence, artifacts, comparisons, and gates.

## Collection And Report Discovery

Run coverage as part of the test command:

```bash
swift test --enable-code-coverage
```

After a successful collection, ask the active toolchain for the exported JSON location instead of hard-coding a `.build` path:

```bash
swift test --show-codecov-path
```

Treat `--show-codecov-path` as a separate report-location query. Do not assume every SwiftPM release accepts it combined with `--enable-code-coverage`, and do not split coverage into a separate build plus `swift test --skip-build` path unless that exact toolchain has been verified.

## Reporting

Read the exported JSON from the reported path and summarize the targets and files it contains. Preserve the original artifact path in the evidence packet. If the file is missing, unreadable, or does not contain the expected coverage payload, report extraction failed; do not substitute a guessed `.build` location or a percentage inferred from test output.

SwiftPM coverage is appropriate for package targets and their ordinary tests. It does not replace app-host, XCUITest, simulator, physical-device, or Xcode test-plan coverage. Hand off to `xcode-testing-workflow` when those surfaces matter.

## Failure Boundaries

- A passing `swift test` without an exported coverage JSON is a coverage-collection failure, not a zero-coverage result.
- Keep package coverage reports out of version control unless the package has an explicit artifact policy.
- Do not create a coverage gate without a repository-owned metric and exclusion policy.
