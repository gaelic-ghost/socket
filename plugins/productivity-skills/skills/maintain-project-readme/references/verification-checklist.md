# Verification Checklist

- The README has a title and one-line summary.
- The README has a table of contents.
- The configured canonical top-level sections all exist.
- The configured required subsections all exist beneath the correct parent section, including `Overview > Status`, `Overview > What This Project Is`, `Overview > Motivation`, `Development > Setup`, `Development > Workflow`, and `Development > Validation`.
- Canonical sections appear in canonical order.
- Alias headings are migrated or reported as non-canonical.
- The table of contents lists the actual H2 headings in order.
- Placeholder-style content is reported instead of silently accepted.
- `apply` mode changes only the target `README.md`.
- Clean runs emit exactly `No findings.`
