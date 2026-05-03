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

Product records include `name`, `kind`, `targets`, and `evidence`.

Target records include `name`, `kind`, `dependencies`, `path`, and `evidence`.

Relationship records include `kind`, `from`, `to`, `label`, and `evidence`.

Do not create relationship records without evidence.
