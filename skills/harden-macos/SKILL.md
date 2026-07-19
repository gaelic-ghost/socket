---
name: harden-macos
description: Review and improve macOS defensive posture after a threat assessment, incident, or general security request. Use for updates, XProtect/Gatekeeper posture, FileVault, firewall and sharing, remote access, accounts, login/background items, profiles/extensions, browser safety, privacy permissions, backups, credential habits, and monitoring while preserving usability and managed-device policy.
---

# Harden macOS

## Overview

Strengthen the actual exposure found on the Mac and verify each change. Preserve built-in protections, user access, recoverability, and organization management requirements.

Read [references/macos-hardening-review.md](references/macos-hardening-review.md) for a risk-ordered review.

## Workflow

1. Establish context.
   - Record exact macOS build/hardware, device ownership/management, users, role, exposed services, sensitive data, backups, and the threat being reduced.
2. Apply supported updates.
   - Verify OS, rapid/security data updates, browsers, extensions, apps, and package managers from authoritative channels.
3. Preserve platform protections.
   - Verify Gatekeeper/XProtect automatic protection, SIP, TCC/privacy access, code-signing expectations, and sandbox/container use where applicable.
   - Keep this defensive posture review separate from developer prompt/request implementation; route ordinary app permission design to `macos-privacy-permissions-workflow`.
4. Protect data and recovery.
   - Review FileVault/recovery ownership, screen lock, backup availability and restore testing, account separation, and secure disposal/export practices.
5. Reduce exposed services and persistence.
   - Review sharing, remote login/management, firewall policy, listeners, login/background items, profiles, system/network/browser extensions, and privileged helpers.
6. Improve identity/browser behavior.
   - Review MFA, password manager use, recovery methods, session/token hygiene, download sources, extensions, phishing-resistant habits, and administrator use.
7. Add proportionate visibility.
   - Define which alerts/logs or endpoint tooling are maintained, who reviews them, and how false positives are handled.
8. Verify and document.
   - Re-read changed settings, test access/recovery, record exceptions and owner, and avoid claiming perfect prevention.

## Output

Return baseline, prioritized changes, applied/verified settings, deferred items and tradeoffs, recovery check, and residual risk.
