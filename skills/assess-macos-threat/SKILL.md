---
name: assess-macos-threat
description: Assess a suspected macOS security threat using exact host, artifact, and platform evidence. Use for suspicious apps, packages, processes, prompts, downloads, profiles, extensions, XProtect or Gatekeeper alerts, account behavior, persistence, privacy access, or unexpected network activity when signing, notarization, quarantine, TCC, SIP, and observed behavior must remain distinct.
---

# Assess macOS Threat

## Overview

Establish the affected Mac and event timeline before changing the system. Use Apple security layers as separate evidence sources and route focused persistence, runtime, artifact, or containment work from the resulting record.

Read [references/macos-security-layers.md](references/macos-security-layers.md) when interpreting platform controls or alerts.

## Workflow

1. Identify the Mac and event.
   - Record model/chip, exact macOS build, update state, user/session, time/timezone, managed-device context, and what the person observed.
   - Record whether evidence comes from the affected physical host, a macOS guest, or a reproduction guest. For guest evidence, include the VM framework/tool, virtual hardware, restore image, integrations, baseline/reset state, and anti-VM or hardware fidelity limits.
2. Preserve the triggering evidence.
   - Record alert text/screenshots, file path/source/hash, quarantine metadata, process identity, prompts, downloads, and relevant logs before cleanup.
3. Inspect artifact identity.
   - Record real type, bundle/package metadata, signer, Team ID, signature verification, notarization assessment, entitlements, modifications, and source channel.
   - Route binary internals to Reverse Engineering Skills.
4. Inspect platform evidence.
   - Check Gatekeeper/quarantine context, XProtect detections or remediation evidence, TCC/privacy grants, profiles, login/background items, system extensions, and relevant system policy without disabling protections.
5. Correlate behavior.
   - Route process/file/network evidence to runtime inspection and startup/registration clues to persistence inspection.
   - Separate a blocked attempt from successful execution and successful execution from compromise.
6. Assess and advise.
   - State classification/confidence, immediate isolation needs, evidence gaps, and the smallest next workflow.
   - Do not generalize guest-observed behavior to a physical Mac when hardware, Secure Enclave, recoveryOS, kernel/system-extension, device, or anti-VM behavior remains unresolved.

## Output

Return host/event identity, platform-layer evidence, artifact identity, observed behavior, assessment/confidence, immediate advice, and focused next checks.
