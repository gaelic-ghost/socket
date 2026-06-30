# Socket Xcode Workspace

This document records the browse-only Xcode workspace at the root of the
`socket` superproject.

## Purpose

`Socket.xcworkspace` exists so maintainers can open the repository in Xcode,
use Xcode's file navigator, and edit Markdown through Xcode 27 beta's WYSIWYG
Markdown editor.

The workspace is not a build surface. It does not create schemes, targets,
package products, generated projects, or root-level Xcode build settings.

## Shape

The workspace references the root maintainer files plus the main authored
source directories:

- root docs such as `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `TODO.md`,
  `AGENTS.md`, and `ACCESSIBILITY.md`
- the root marketplace file at `.agents/plugins/marketplace.json`
- `docs/`
- `plugins/`
- `scripts/`

This keeps Xcode useful for browsing and editing without implying that Socket
itself is an Apple app, Swift package, or generated Xcode project.

## Maintenance Rules

- Keep the workspace browse-only until Socket has a concrete root build product
  that needs an Xcode scheme.
- Do not add generated `.xcodeproj` files, schemes, or package manifests just to
  improve Markdown editing.
- If a child plugin gains its own Xcode project, keep that child project owned
  by the child plugin and add a workspace reference only when it helps root
  maintainers browse the superproject.
- If the workspace starts carrying build behavior, update this document,
  `CONTRIBUTING.md`, and any affected validation guidance in the same pass.

## Validation

For a browse-only workspace change, validate that Xcode can parse the workspace
metadata:

```bash
xcodebuild -list -workspace Socket.xcworkspace
```

The command is expected to report no schemes unless a future approved change
adds buildable project references.
