---
name: assess-exposure-and-impact
description: Prioritize a validated or plausible vulnerability using actual asset exposure and impact. Use when affected versions, deployment reachability, attacker prerequisites, privileges, sensitive data, exploit maturity, CISA KEV status, vendor guidance, mitigations, detection, business criticality, CVSS, and remediation urgency must be combined without relying on a severity score alone.
---

# Assess Exposure And Impact

## Overview

Translate a technical finding into asset-specific risk and action. Treat CVSS as one technical severity input and current exploitation intelligence as another; neither replaces deployed context.

Read [references/exposure-impact-model.md](references/exposure-impact-model.md) for the decision factors.

## Workflow

1. Confirm finding confidence and exact affected/fixed versions.
2. Inventory affected assets.
   - Record internet/internal/local reachability, environment, owner, business function, data, users, privileges, and compensating controls.
3. Model attacker requirements.
   - Record access position, authentication, user interaction, configuration, chaining, reliability, and detection likelihood.
4. Check current intelligence.
   - Review vendor advisory, fixed release, exploit maturity, CISA KEV/ransomware status, ecosystem advisories, and known active campaigns; date sources.
5. Evaluate consequence.
   - Assess confidentiality, integrity, availability, privilege, blast radius, persistence, recovery difficulty, safety/legal/privacy obligations, and business interruption.
6. Evaluate mitigations.
   - Test whether configuration, network controls, feature disablement, isolation, monitoring, or virtual patching actually blocks the validated path.
7. Prioritize action.
   - Recommend patch, mitigate, isolate, monitor, accept temporarily with owner/expiry, or investigate further; include retest criteria.

## Output

Return affected assets, exposure path, impact, current exploitation context, mitigations, priority/rationale, action owner/deadline, and residual uncertainty.
