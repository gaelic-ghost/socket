---
name: recover-security-incident
description: Eradicate verified compromise mechanisms, restore trusted service, and monitor after a cybersecurity incident. Use when affected hosts, identities, applications, cloud resources, network controls, or data need rebuild/restore, patching, secret rotation, configuration repair, validation, staged return to service, temporary-control removal, lessons learned, and residual-risk ownership.
---

# Recover Security Incident

## Overview

Return systems and people to a trusted operating state using explicit eradication and validation criteria. Recovery is complete only when restored behavior, security controls, access, monitoring, and residual risk are verified.

Read [references/recovery-gates.md](references/recovery-gates.md) for staged return-to-service gates.

## Workflow

1. Establish eradication criteria.
   - Identify root/access path, persistence, affected identities/secrets, vulnerable configuration/code, related artifacts, and known scope.
2. Choose restore basis.
   - Decide clean rebuild, known-good backup, patched image, repaired configuration, provider recovery, or controlled cleanup from evidence and integrity confidence.
3. Eradicate.
   - Remove verified mechanisms, patch or mitigate the entry path, rotate/revoke secrets and sessions from trusted systems, repair policies/configuration, and preserve evidence of changes.
4. Restore in stages.
   - Validate offline or isolated, restore dependencies/data, enable limited traffic/users, monitor, then broaden service.
5. Verify security and function.
   - Reproduce the original detection/path as a negative test, confirm expected functionality, review access/persistence/network/logging, and check backups and monitoring.
6. Remove temporary controls deliberately.
   - Inventory emergency rules, disabled services, isolation, temporary accounts, logging, tokens, and exceptions; retain only approved controls with owners/expiry.
7. Close and improve.
   - Record timeline, root cause, affected scope, actions, notifications, evidence retention, lessons, structural hardening, and residual risk owner.

## Output

Return eradication evidence, restore basis, staged recovery results, negative retest, temporary-control disposition, monitoring window, lessons/actions, and residual-risk decision.
