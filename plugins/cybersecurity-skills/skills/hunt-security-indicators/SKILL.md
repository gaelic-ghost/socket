---
name: hunt-security-indicators
description: Hunt scoped systems and telemetry for supplied indicators or behaviors. Use for hashes, paths, domains, addresses, accounts, processes, persistence, ATT&CK behaviors, cloud events, or incident expansion with explicit scope and validation.
---

# Hunt Security Indicators

## Overview

Turn validated evidence into bounded queries across known data sources, then validate matches in context. Absence of matches means only that the indicator was not observed in the recorded coverage.

Read [references/hunt-record.md](references/hunt-record.md) for query and coverage fields.

## Workflow

1. Define the hunt question and scope.
   - Record incident/finding, assets, identities, environments, time window, data owners, privacy constraints, and expected decision.
2. Normalize indicators and behaviors.
   - Preserve type, value, source, confidence, first/last seen, expected context, variants, and expiration.
   - Prefer behavior chains over one mutable hash/domain when telemetry supports them.
3. Inventory data sources.
   - Record endpoint/process/file, identity, DNS/network/proxy, application, cloud, email, vulnerability, and backup evidence plus retention, collection delay, and gaps.
4. Write reproducible queries.
   - Record platform/tool/version, exact query, normalization/timezone, filters, exclusions, and expected benign matches.
5. Validate matches.
   - Correlate asset/user/time/process/parent/path/signer/network or application context; preserve false-positive rationale.
6. Expand deliberately.
   - Pivot only from validated relations and update scope, indicators, and confidence.
7. Report coverage.
   - State searched/failed sources, earliest/latest available data, assets not covered, matches, negative results, and next response/detection action.

## Output

Return hypothesis, indicators/behaviors, data coverage, queries, validated matches, false positives, gaps, pivots, and response recommendations.
