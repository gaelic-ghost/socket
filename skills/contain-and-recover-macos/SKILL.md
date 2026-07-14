---
name: contain-and-recover-macos
description: Contain a suspected or confirmed macOS threat and verify recovery. Use when a Mac may need network isolation, process or service containment, account and credential response, persistence removal, artifact quarantine, backup/restore, erase/reinstall, monitoring, or return-to-service decisions while evidence loss, user impact, and platform protections remain explicit.
---

# Contain And Recover macOS

## Overview

Choose actions proportionate to evidence and ongoing harm. Preserve what matters, use official lifecycle controls, and verify the system after eradication rather than declaring it clean because one artifact disappeared.

Read [references/macos-response-ladder.md](references/macos-response-ladder.md) for containment and recovery levels.

## Workflow

1. Confirm assessment, confidence, affected scope, ongoing behavior, critical data, and evidence needs.
2. Choose immediate containment.
   - Prefer reversible network/account/session isolation when it stops harm.
   - Record the effect on volatile evidence and business/user access.
3. Preserve decisive evidence.
   - Capture artifact, persistence, process/network/log, account, and timeline records before removal when delay is safe.
4. Stop active behavior through official controls.
   - End processes/services deliberately; use `launchctl bootout` for approved launch service removal from a domain, app-provided uninstallers for app components, and supported profile/extension management surfaces.
   - Never edit launchd's internal state directly.
5. Eradicate the verified mechanism.
   - Remove or quarantine confirmed artifacts, registrations, extensions, profiles, helpers, rules, and downloaded stages; preserve hashes and paths.
6. Respond to identity exposure.
   - Rotate affected credentials/tokens from a trusted device, revoke sessions/keys, review MFA and recovery methods, and notify owners/providers as warranted.
7. Recover.
   - Restore from a known-good point, reinstall/erase when integrity cannot be established, apply updates, reconfigure only needed access, and avoid restoring suspect persistence.
8. Verify and monitor.
   - Recheck persistence, runtime/network, accounts, security updates, backups, and recurrence across a defined observation window.

## Output

Return containment/impact, evidence preserved, eradication actions, credential response, recovery basis, verification results, residual uncertainty, and return-to-service decision.
