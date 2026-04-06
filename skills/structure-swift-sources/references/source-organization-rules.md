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

- Every Swift file should be organized into section groups.
- Each group should start with `// MARK: - <Heading>`.
- Place a descriptive secondary line immediately below it as `// MARK: <Comment>`.
- Group declarations by declaration kind or responsibility rather than by arbitrary source order.

## SwiftUI Rule

- Once any one view has more than `3` chained modifiers, strongly consider extracting a custom `ViewModifier`.
- Place that modifier in `<Name>+Modifier.swift` when the modifier belongs to one view family.

## DocC Rule

- Every symbol declaration should carry DocC-compliant documentation comments during a full structure pass.
- Prefer concise symbol docs that explain role, inputs, outputs, and important invariants over filler prose.
