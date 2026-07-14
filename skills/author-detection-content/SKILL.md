---
name: author-detection-content
description: Turn validated security behavior into tested detection content. Use for Sigma, osquery, YARA-X routing, endpoint queries, SIEM rules, cloud or application detections, correlation logic, alert enrichment, or regression fixtures when telemetry prerequisites, provenance, expected matches, benign negatives, false-positive controls, performance, severity, response, deployment, and maintenance ownership must be explicit.
---

# Author Detection Content

## Overview

Detect the validated behavior at the most reliable telemetry layer. Use `author-yara-x-rules` for artifact pattern rules; use this workflow for event, query, correlation, and alert content.

Read [references/detection-quality.md](references/detection-quality.md) before choosing logic or deployment severity.

## Workflow

1. Define objective and response.
   - State the behavior, threat/finding source, protected surface, expected alert consumer, urgency, and action.
2. Identify telemetry prerequisites.
   - Record source/product/version, event types/fields, collection permissions, normalization, retention, latency, and known blind spots.
3. Select durable features.
   - Prefer behavior and context combinations over mutable infrastructure or one noisy field.
   - Map to ATT&CK only when evidence supports it.
4. Author content.
   - Include title/ID, description, status, author/date, references, log source, logic/query, fields, false positives, level/severity, tags, and test notes as the target format permits.
5. Test fixtures.
   - Include validated positive events, benign near-misses, missing/renamed fields, ordering/time-window cases, duplicate events, volume/performance, and known platform variants.
6. Tune and validate response.
   - Improve logic before adding exclusions; verify enrichment and runbook lead an analyst to decisive evidence.
7. Deploy and maintain.
   - Record target environments, owner, version, rollout, alert volume, suppression/exception expiry, health checks, and review triggers.

## Output

Return detection content, telemetry contract, evidence provenance, fixture results, false positives/limits, performance, severity/response, deployment plan, and owner/review date.
