# Custom Symbols and App Inspection

Use this reference when the task needs the SF Symbols app, custom symbols, export behavior, or live visual inspection.

## Local App Evidence

Observed on Gale's Mac on 2026-06-28:

- App path: `/Applications/SF Symbols.app`
- Bundle identifier: `com.apple.SFSymbols`
- Version: `7.2`
- Build: `119`
- Main library count in the visible window: `7,007 Symbols`
- Sidebar categories exposed through accessibility include What's New, Draw, Variable, Multicolor, and Custom Symbols.
- Toolbar controls expose symbol family, weight, grid/list/gallery view, inspector, and search.
- Inspectors exposed through accessibility include Info, Format, and Animation.

Treat these as local evidence, not permanent API facts. Re-check the app before making current-version claims.

## App Inspection Workflow

1. Inspect the app through Computer Use only after verifying it is open or safe to open.
2. Use search for exact symbol names when repairing code.
3. Use category rows such as Variable or Multicolor when checking support families.
4. Use the Format inspector for rendering and color behavior.
5. Use the Animation inspector for symbol effect support and behavior.
6. Use Custom Symbols only when importing, validating, or comparing custom symbol templates.
7. Capture screenshots or notes for user-facing visual decisions when useful.

Do not save, overwrite, export, or mutate user collections without explicit confirmation.

## Custom Symbol Workflow

- Start from a real need for an app-specific symbol.
- Use Apple's custom-symbol documentation before giving template, annotation, or export instructions.
- Keep source artwork simple and symbol-like.
- Preserve SF Symbols metrics, alignment, and optical weight when building template variants.
- Annotate layers only when non-monochrome rendering is required.
- Validate custom symbol behavior in the SF Symbols app before integrating into an app project.
- Hand off Xcode asset integration, previews, builds, and target membership to `xcode-build-run-workflow`.

## Export and Project Boundaries

- Custom symbol output can become an app resource; adding it to the repo or asset catalog is project work.
- Built-in SF Symbols should usually remain referenced by name in code instead of copied into the project.
- Do not commit machine-local export paths or SF Symbols app cache paths.
- Do not represent SF Symbols app GUI inspection as project validation. Build or preview validation belongs to Xcode workflows.

## Licensing Boundary

If the user asks to extract, modify, redistribute, package, or publish Apple symbol assets outside normal app-development use, state the licensing or redistribution concern once, then continue with private local work if that is the user's explicit scope. Public redistribution decisions need a separate explicit approval path.
