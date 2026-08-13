# Single-Project Apple Workspace Audit

The workspace root contains one generated `.xcodeproj` driven by root
`project.yml`. `Apps/` holds target specs and target-owned source/configuration
files; it does not hold child Xcode projects. `Packages/` contains local Swift
packages registered through `Packages/packages-shared.yml`.

Audit the source of truth, then run XcodeGen. Never repair generated project or
workspace data directly during a guidance sync.
