# Swift File Headers

## Purpose

Use a short block-comment header near the top of each managed Swift source file to explain, in plain terms, what the file is for and what concern it owns.

## Required Shape

Use this shape:

```swift
/*
Purpose: Explains what this file is for in plain terms.
Concern: Explains the main responsibility or area of concern in plain terms.
*/
```

## Content Rules

- Keep the text short, concrete, and readable.
- Use plain terms instead of symbol-only shorthand.
- Do not repeat the filename as the full explanation.
- Do not use filler such as `misc`, `helpers`, `utilities`, `stuff`, or `various`.
- Treat `Purpose` as the job the file does for the repository.
- Treat `Concern` as the main responsibility boundary the file owns.

## Placement Rules

- Place the structured header near the top of the file.
- If a file already starts with a license banner or another preserved top-of-file comment, keep that prefix and place the structured header immediately after it.
- Keep exactly one structured header per file.

## Automation Boundary

- Use `scripts/normalize_swift_file_headers.py` to audit header presence and shape across `.swift` files.
- Use `scripts/normalize_swift_file_headers.py --apply --inventory <yaml>` when you already have explicit `Purpose` and `Concern` text for each file and want the script to normalize placement and formatting deterministically.
- Do not use the script to invent header text. The script normalizes shape and placement; the content still needs to come from actual code understanding or an explicit inventory.
