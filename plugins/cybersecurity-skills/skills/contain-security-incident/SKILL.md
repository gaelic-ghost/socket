---
name: contain-security-incident
description: Contain an active or credible cybersecurity incident across hosts, identities, applications, services, cloud resources, networks, or data. Use when ongoing access, execution, exfiltration, fraud, destruction, lateral movement, unsafe service behavior, or repeated compromise must be interrupted with authorized, reversible actions while evidence, business impact, dependencies, communication, and rollback are tracked.
---

# Contain Security Incident

## Overview

Interrupt the validated path of harm with the smallest effective action, then verify the containment. Do not confuse a blocked symptom with eradication or recovery.

Read [references/containment-plan.md](references/containment-plan.md) before making disruptive changes.

## Workflow

1. Confirm incident lead, authority, current scope, harm path, critical services, evidence priorities, and emergency contacts.
2. Model containment choices.
   - Consider host/network isolation, process/service suspension, account disablement, session/token/key revocation, access-policy change, application feature disablement, route/rule changes, or provider controls.
   - Record expected harm reduction, operational impact, volatile evidence loss, dependencies, rollback, and attacker visibility.
3. Sequence actions.
   - Address active exfiltration/destruction/safety first, then privileged access, propagation, persistence, and re-entry paths.
   - Coordinate simultaneous identity, host, application, and network actions when staggered changes would alert or strand access.
4. Apply approved changes.
   - Record exact target, operator, time, command/control surface, result, failures, and unexpected effects.
5. Verify containment.
   - Check that the harmful path stopped, access/session state changed, affected services remain understood, and monitoring still functions.
6. Expand scope carefully.
   - Hunt for related indicators and access paths; update the incident record before new targets or actions.
7. Define exit criteria.
   - State what evidence permits eradication/recovery and what temporary controls must remain.

## Output

Return containment objective, options/tradeoffs, actions/results, verification, residual access, business impact, temporary controls, rollback, and next-phase criteria.
