---
name: report-security-assessment
description: Write a reproducible security assessment or penetration-test report from validated evidence. Use when technical findings, negative results, scope, methodology, limitations, exposure, impact, confidence, remediation, retest criteria, evidence handling, and a plain-language executive explanation must be assembled without overstating scanner output or untested coverage.
---

# Report Security Assessment

## Overview

Produce a report that lets technical owners reproduce findings and non-specialists understand what matters. Preserve uncertainty, scope limits, and negative results that materially constrain conclusions.

Read [references/security-report-shape.md](references/security-report-shape.md) for the required structure.

## Workflow

1. Fix report identity.
   - Record title, client/project, assessment type, dates, version, authors, classification, and distribution.
2. State scope and authority.
   - List included/excluded targets, environments, accounts/roles, techniques, time windows, constraints, and changes from the approved scope.
3. Summarize outcomes plainly.
   - Explain what was found, affected assets, practical consequence, urgent actions, and material uncertainty without jargon or panic.
4. Describe methodology and coverage.
   - Name standards/guidance, tools/versions, manual checks, evidence sources, assumptions, unavailable telemetry, and untested areas.
5. Write each finding.
   - Include identity, status/confidence, affected assets, prerequisites, evidence/reproduction, impact, exposure, severity/vector if used, remediation, mitigation, and retest steps.
   - Keep raw secrets and unnecessary personal data out of the report.
6. Record negative results and limitations.
7. Build a remediation plan.
   - Group immediate containment, near-term fixes, structural hardening, owners, deadlines, and dependencies.
8. Verify the report.
   - Cross-check evidence links, commands, screenshots, identifiers, redaction, scope, and status.

## Output

Return a self-contained report with executive summary, scope, methodology, findings, negative results, limitations, prioritized remediation, and retest plan.
