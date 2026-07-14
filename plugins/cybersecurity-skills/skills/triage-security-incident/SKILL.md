---
name: triage-security-incident
description: Triage a suspected cybersecurity incident across endpoints, identities, applications, services, cloud resources, networks, or data. Use when an alert, report, compromise indicator, service disruption, unauthorized access, malware event, credential concern, or data exposure needs an incident owner, affected scope, urgency, evidence plan, immediate harm-reduction decision, and communication path.
---

# Triage Security Incident

## Overview

Establish whether coordinated response is needed, what may be affected, and who owns decisions. Preserve uncertainty and avoid destructive cleanup while urgent harm reduction and evidence collection are balanced.

Read [references/incident-triage-record.md](references/incident-triage-record.md) for the initial record aligned with current NIST incident-response guidance.

## Workflow

1. Open the incident record.
   - Record reporter, detection source, time/timezone, symptoms, affected person/system, current status, and incident lead.
2. Validate the signal.
   - Preserve the original alert/report and confirm artifact, account, host, service, or event identity.
   - Separate direct observation, external intelligence, automation labels, and speculation.
3. Estimate scope and urgency.
   - Identify potentially affected assets, identities, data, users, environments, business function, privileges, and time window.
   - Record ongoing execution, access, exfiltration, destruction, fraud, safety, or service impact.
4. Decide immediate harm reduction.
   - Choose reversible isolation, session/token revocation, feature disablement, traffic control, or monitoring only when evidence and authority justify it.
   - State evidence loss and operational impact.
5. Preserve priority evidence.
   - Capture volatile state, logs, artifacts, identity/provider records, application events, network evidence, and timeline sources proportionately.
6. Establish coordination.
   - Name technical, business, legal/privacy, communications, vendor/provider, and affected-user contacts as applicable; keep sensitive details need-to-know.
7. Route the next phase.
   - Use containment for ongoing harm, hunting for scope, specialist analysis for evidence, and recovery only after eradication criteria are defined.

## Output

Return incident identity/owner, signal confidence, affected/potential scope, urgency, immediate actions, evidence plan, contacts, open questions, and next phase.
