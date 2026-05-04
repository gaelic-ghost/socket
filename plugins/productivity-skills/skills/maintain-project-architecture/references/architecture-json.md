# Architecture JSON

`architecture.json` is the structured source for future architecture viewers.

## Top-level Shape

```json
{
  "schemaVersion": 1,
  "generatedBy": "maintain-project-architecture",
  "projectRoot": "/path/to/repo",
  "detectedAt": "2026-05-03T00:00:00Z",
  "products": [],
  "targets": [],
  "relationships": [],
  "slices": [],
  "evidence": []
}
```

## Records

Product records include `name`, `kind`, `targets`, and `evidence`. Codex plugin repositories may also include a repo-relative `path`.

Target records include `name`, `kind`, `dependencies`, `path`, and `evidence`.

Relationship records include `kind`, `from`, `to`, `label`, and `evidence`.

Do not create relationship records without evidence.

## Codex Plugin Records

Use these product kinds when plugin evidence exists:

- `codex-plugin-marketplace` for `.agents/plugins/marketplace.json`
- `codex-plugin` for `.codex-plugin/plugin.json`
- `codex-plugin-entry` for local marketplace entries without a readable manifest
- `remote-plugin-entry` for Git-backed marketplace entries

Use these target kinds when plugin evidence exists:

- `codex-skill` for `skills/*/SKILL.md`
- `mcp-config` for declared `.mcp.json` files
