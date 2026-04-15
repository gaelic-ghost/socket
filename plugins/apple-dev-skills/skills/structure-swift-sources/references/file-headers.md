# Swift File Headers

## Purpose

Use a structured block-comment banner near the top of each managed Swift source file to identify the project and file explicitly, record the copyright owner and year, and explain in plain terms what the file is for and what concern it owns.

## Required Shape

Use this shape:

```swift
/*
<Project Name>
<File Name>
© Gale Williams <YEAR>

Concern: Explains the main responsibility or area of concern in plain terms.
Purpose: Explains what this file is for in plain terms.
Key Types: Optional comma-separated type names or symbol groups.
See Also: Optional related files, symbols, or flows.
*/
```

`Key Types` and `See Also` are optional. Omit those lines entirely when they do not add signal.

## Content Rules

- Keep the text short, concrete, and readable.
- Use plain terms instead of symbol-only shorthand.
- Do not let `Purpose` or `Concern` collapse into a restatement of the filename.
- Do not use filler such as `misc`, `helpers`, `utilities`, `stuff`, or `various`.
- Keep `<Project Name>` and `<File Name>` literal and explicit.
- Keep the copyright line in the form `© <Owner> <YEAR>`.
- Treat `Purpose` as the job the file does for the repository.
- Treat `Concern` as the main responsibility boundary the file owns.
- Use `Key Types` only when naming the main types or symbols genuinely helps a reader orient themselves faster.
- Use `See Also` only when there are high-signal adjacent files, symbols, or flows worth following next.

## Placement Rules

- Place the structured header near the top of the file.
- If a file already starts with a license banner or another preserved top-of-file comment, keep that prefix and place the structured header immediately after it.
- Keep exactly one structured header per file.
- Infer `<Project Name>` from the repository root name unless a future workflow explicitly overrides it.
- Infer `<File Name>` from the source filename.
- When creating a new structured header, default `<YEAR>` to the current year. When updating an existing structured header, preserve its year unless there is an explicit reason to change it.

## Automation Boundary

- Use `scripts/normalize_swift_file_headers.py` to audit header presence and shape across `.swift` files.
- Start from `references/file-header-inventory.template.yaml` when you want a user-editable inventory file for `--apply` mode.
- Use `scripts/normalize_swift_file_headers.py --apply --inventory <yaml>` when you already have explicit `Purpose` and `Concern` text for each file and want the script to normalize placement and formatting deterministically.
- The script fills `<Project Name>`, `<File Name>`, and `<YEAR>` deterministically.
- The inventory may also provide optional `key_types` and `see_also` entries.
- Do not use the script to invent `Purpose` or `Concern` text. The script normalizes shape and placement; the meaning-bearing content still needs to come from actual code understanding or an explicit inventory.

## Inventory Template

Start from this checked-in template:

- `references/file-header-inventory.template.yaml`

It is meant to be copied and edited by maintainers or end users before running:

```bash
scripts/normalize_swift_file_headers.py --apply --inventory path/to/headers.yaml
```

The expected shape is:

```yaml
entries:
  - path: "Sources/Feature.swift"
    concern: "<Explain the file's main responsibility boundary in plain terms.>"
    purpose: "<Explain what job this file does for the repository in plain terms.>"
    key_types:
      - "FeatureView"
      - "FeatureState"
    see_also:
      - "FeatureView+Model.swift"
      - "FeatureView+Modifier.swift"
```

`key_types` and `see_also` may be omitted when they do not add signal.
