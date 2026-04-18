# Source Organization Rules

## File Splitting Thresholds

- Strongly consider a split once a file exceeds `400` lines and clearly holds `2` or more separate concerns.
- Always split once a file exceeds `800` lines.
- Prefer a complete pass over a temporary partial split.

## Split Shape

- If one type is still coherent but too large, extract grouped responsibilities into extension files.
- Prefer names such as:
  - `<Original>+Models.swift`
  - `<Original>+Persistence.swift`
  - `<Original>+Validation.swift`
  - `<Original>+Modifier.swift`
- Treat Swift access control as part of the design; confirm the extracted file shape still supports the intended visibility.

## MARK Rules

- Use section groups only when they add real navigation value inside a file that is large enough, mixed enough, or layered enough to justify them.
- Do not force section groups into small or already-obvious files just to satisfy a formatting pattern.
- When a group is warranted, start it with `// MARK: - <Heading>`.
- Use headings that identify a meaningful responsibility, boundary, or decision surface instead of lightly rephrasing symbol names or obvious declaration kinds.
- Add a secondary line immediately below it as `// MARK: <Comment>` only when that extra line answers a useful question such as why the section exists, what it is for, or how it differs from neighboring sections.
- Skip the secondary comment line when the heading already says enough and no deeper navigational distinction needs explanation.
- Group declarations by responsibility or navigational intent rather than by arbitrary source order.

## File Header Rule

- Managed Swift source files should carry the structured block-comment header described in `references/file-headers.md`.
- The header should identify the project and file explicitly, then explain the file's concern and purpose in plain terms.
- Keep the header requirement separate from DocC authoring. It is a file-level structure rule, not symbol-level documentation.

## SwiftUI Rule

- Once any one view has more than `3` chained modifiers, strongly consider extracting a custom `ViewModifier`.
- Place that modifier in `<Name>+Modifier.swift` when the modifier belongs to one view family.

## Documentation Boundary

- Keep this workflow focused on source layout and declaration organization.
- When the task becomes symbol documentation, DocC article work, landing-page structure, topic groups, or DocC-oriented review, hand off to `author-swift-docc-docs`.
