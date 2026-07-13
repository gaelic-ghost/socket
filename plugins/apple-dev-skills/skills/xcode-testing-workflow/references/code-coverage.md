# Xcode Code Coverage

Use Xcode coverage for Xcode-managed test targets, UI tests, app-hosted tests, simulator or device destinations, and `.xctestplan` configurations. Follow the shared [`code-coverage-contract`](../../../shared/references/code-coverage-contract.md) for evidence, artifacts, comparisons, and gates.

## Collection

For an explicit CLI run, use a real project or workspace, scheme, and destination. Capture an `.xcresult` bundle so the coverage data is inspectable after the test process exits:

```bash
xcodebuild test -workspace <workspace>.xcworkspace -scheme <scheme> \
  -destination '<destination>' -enableCodeCoverage YES \
  -resultBundlePath <artifacts>/<run>.xcresult
```

Replace `-workspace` with `-project <project>.xcodeproj` only when the project is not workspace-managed. For repeatable named configurations, version an `.xctestplan` that enables coverage and run it with `-testPlan <plan>`; do not use a plan merely to hide an otherwise simple one-off coverage command.

## Reporting

Use `xccov` against the result bundle rather than scraping test logs:

```bash
xcrun xccov view --report --json <artifacts>/<run>.xcresult
xcrun xccov view --archive --json <artifacts>/<run>.xcresult
```

The report gives target, file, and function coverage. The archive provides execution-count detail. Use `xcrun xccov diff --json <before>.xcresult <after>.xcresult` only when the two runs meet the shared comparison contract.

## Xcode 27 MCP Boundary

Xcode 27 beta documents new MCP capabilities for active run-state control, debugger-console interaction, scheme and run-destination management, build-setting/compiler-flag/entitlement/Info.plist inspection and mutation, runtime health insights, simulator interaction, preview variants, and String Catalog workflows. Discover the tool inventory from the live Xcode session before naming or invoking a specific tool.

Apple does not document a coverage-report MCP tool in this beta. Use Xcode MCP for session discovery and test execution when the live session provides those tools, then use `xcodebuild` and `xccov` for deterministic coverage collection and report extraction.

## Failure Boundaries

- A successful test run without an `.xcresult` or readable `xccov` report is a coverage-collection failure, not a coverage result.
- A coverage report with failing tests remains a failing test run; do not report its percentage as a passing quality signal.
- Do not compare simulator and physical-device coverage, Debug and Release coverage, or different schemes as though they are the same baseline.
