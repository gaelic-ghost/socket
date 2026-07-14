# Detection Quality Checklist

- Objective describes one validated behavior and intended response.
- Telemetry source, version, permissions, fields, normalization, and gaps are explicit.
- Logic uses durable features with documented provenance.
- Positive fixtures reproduce the behavior; benign negatives challenge the same fields.
- Missing fields, duplicates, event order, time windows, platform variants, and load are tested.
- False-positive guidance explains analyst validation, not blanket suppression.
- Severity matches response urgency and evidence, not ATT&CK tactic alone.
- Rule ID/version, owner, deployment scope, alert health, exception expiry, and review trigger are recorded.

For artifact pattern matching, use `author-yara-x-rules`. For portable event rules, use the current target format specification rather than assuming Sigma or query-field compatibility across backends.
