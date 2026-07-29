# Accessibility Config Schema

The accessibility customization file uses this shape:

```yaml
schemaVersion: 1
isCustomized: false
profile: base
settings:
  preservePreamble: true
  allowAdditionalSections: true
  requiredSections: []
  sectionOrder: []
  requiredSubsections: {}
  sectionAliases: {}
  subsectionAliases: {}
  sectionTemplates: {}
  subsectionTemplates: {}
```

Notes:

- `requiredSections` declares the canonical top-level `##` sections.
- `sectionOrder` controls normalized output order.
- `requiredSubsections` maps each canonical top-level section to its required `###` subsections.
- `sectionAliases` and `subsectionAliases` are migration helpers for apply mode, not canonical output.
- `sectionTemplates` and `subsectionTemplates` supply fallback content when apply mode must create missing structure.
