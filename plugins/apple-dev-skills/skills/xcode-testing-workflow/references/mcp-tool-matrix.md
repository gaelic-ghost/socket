# MCP Tool Matrix

These are Xcode-owned MCP tools exposed through `xcrun mcpbridge` after external-agent access is enabled in Xcode. Do not substitute a bundled or third-party Xcode MCP server when following this matrix.

## Workspace and session

- `XcodeListWindows`
- `XcodeListNavigatorIssues`

## Discovery and read/search

- `DocumentationSearch`
- `XcodeLS`
- `XcodeGlob`
- `XcodeRead`
- `XcodeGrep`

## Diagnostics, build, and tests

- `XcodeRefreshCodeIssuesInFile`
- `GetBuildLog`
- `GetTestList`
- `BuildProject`
- `RunAllTests`
- `RunSomeTests`

## Runtime and previews

- `ExecuteSnippet`
- `RenderPreview`

## Structured mutation

- `XcodeWrite`
- `XcodeUpdate`
- `XcodeMakeDir`
- `XcodeMV`
- `XcodeRM`

## Known constraints

- Runtime and preview operations require files in active scheme targets.
- Tab indices can remain stable after window closure; always resolve by workspace path.
- Deep directory creation may require parent-by-parent creation.

## Xcode 27 Beta Additions

Apple documents additional beta-era MCP capability groups for active run-state control, debugger-console interaction, scheme and run-destination management, build-setting/compiler-flag/entitlement/Info.plist inspection and mutation, runtime health insights, simulator interaction, preview variants, and String Catalog workflows.

These are capability groups, not stable tool names. Discover the live Xcode tool inventory before invoking a tool, apply the existing permission boundary, and hand off to the owning build, testing, debugger, Device Hub, preview, or localization workflow.

Apple does not document a code-coverage MCP tool. Use the official `xcodebuild` and `xccov` coverage path when a deterministic report is required.
