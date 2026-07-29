# Visual Grammar

The architecture viewer should use a custom visual language, not Mermaid as the primary surface.

## Hard Rules

- No center-aligned text.
- No large decorative whitespace.
- No curved-line diagrams.
- No labels that interrupt connector lines.
- No unlabeled arrows.
- No ambiguous arrows whose direction does not say what relationship is represented.
- No generic boxes such as "Runtime" or "API" unless those are real repo symbols, products, targets, or filenames.

## Preferred Layout

- Use a clear top-to-bottom reading path.
- Use left/top as the starting point.
- Put data models at the top of slice views.
- Use stacked dense panels for slice steps.
- Use familiar icons or symbols to distinguish products, modules, types, functions, properties, storage, external systems, and generated artifacts.
- Use color for category and relationship meaning, not decoration.

## Relationship Kinds

Use explicit relationship kinds in structured data:

- `creates`
- `initializes`
- `passes`
- `stores`
- `reads`
- `writes`
- `calls`
- `returns`
- `owns`
- `depends-on`
- `exposes`

Every relationship should carry a source anchor, target anchor, and evidence when possible.
