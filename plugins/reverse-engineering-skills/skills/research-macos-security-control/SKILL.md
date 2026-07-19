---
name: research-macos-security-control
description: Research one macOS security or privacy control on an exact OS build and produce a reproducible technical note that separates public contracts, private implementation evidence, runtime observations, and hypotheses. Use for TCC services/frameworks/databases/attribution, sandbox profiles and extensions, public or private entitlements, Execution Policy, quarantine, Gatekeeper, XProtect, notarization, system policy, Hardened Runtime, library validation, SIP, Data Vaults, signed system volume, boot policy, security daemons/XPC, unified logs, Endpoint Security events, dyld/Mach-O symbols, or cross-build behavior changes.
---

# Research macOS Security Control

## Overview

Answer one narrow control question on named artifacts and exact macOS builds. Start from supported public behavior, preserve originals, and label private symbols, schemas, strings, logs, and observed behavior as implementation evidence rather than stable API.

## Workflow

1. State the question and decision.
   - Name the control, suspected behavior, affected actor/target, smallest falsifiable claim, expected decision, and stop condition.
2. Establish the evidence hierarchy.
   - Read [references/source-and-evidence-hierarchy.md](references/source-and-evidence-hierarchy.md).
   - Search Apple Platform Security, deployment/developer documentation, current SDK declarations, tool man pages, and checked-in source before private implementation.
3. Fix the environment and artifacts.
   - Record hardware/architecture, exact macOS version/build, security-data/update state, selected SDK/Xcode, device management, host/guest/physical context, SIP/boot policy when relevant, and every artifact's path, hash/UUID, signing identity, acquisition source, and transformation history.
4. Classify the control.
   - Use [references/control-research-matrix.md](references/control-research-matrix.md) to keep TCC, App Sandbox, entitlements, execution/distribution policy, malware protection, and system integrity distinct.
5. Inspect exact-build implementation without changing originals.
   - Inspect relevant binaries/frameworks/services, Mach-O metadata, signatures/entitlements, dependencies, strings, symbols, XPC/interface metadata, launch/service ownership, focused unified logs, and existing Endpoint Security evidence.
   - Use `evidence-notes-workflow`, `audit-apple-signing-and-containment`, and `compare-binary-versions` for their owned records.
6. Design the least invasive probe.
   - Follow [references/exact-build-probe-design.md](references/exact-build-probe-design.md). Prefer a read-only/static check, then a bounded supported observation, then a disposable SIP-enabled guest. Require explicit approval for visible prompts, live-host permission mutations, re-signing, patching, protection changes, or sensitive capture.
7. Execute and preserve results.
   - Record exact commands/tools/versions, inputs, timestamps, status/error/log fields, negative results and telemetry gaps, transformations, cleanup, and whether the observation occurred on host, guest, or physical Mac.
8. Compare builds correctly.
   - Match architecture, artifact identity, security state, and analysis method. Say `changed between A and B` unless intermediate builds establish a tighter bound; do not infer causality from a symbol/string delta alone.
9. Write the technical note.
   - Use [references/technical-note-contract.md](references/technical-note-contract.md). Separate public contract, direct observation, private evidence, hypothesis, conclusion/confidence, disproven explanations, and unresolved questions.
10. Route the result.
   - Hand ordinary app privacy, file access, entitlement/provisioning, distribution, threat response, or formal reporting to the existing owning skill with the exact-build evidence record.

## Guardrails

- Do not present private symbols, `kTCCService*` constants, database schemas, log strings, sandbox profiles, or daemon behavior as supported public API.
- Do not mutate live TCC or system-policy databases for convenience.
- Do not disable SIP, boot protections, Gatekeeper, XProtect, or other controls without a separate exact goal, minimum necessary change, recorded before/after state, rollback, and explicit approval.
- Do not generalize one build, VM, architecture, security-data version, or transformed artifact to another without comparison evidence.
- Preserve originals and treat every extraction, thinning, re-sign, patch, or copy with changed metadata as a distinct artifact.
- Absence of a log/event is not proof that behavior did not occur when collection permission, retention, filter, or telemetry coverage is incomplete.

## Output

Return a technical note containing question/decision, public contract, environment and artifact identity, method/tooling, direct observations, private implementation evidence, hypotheses/tests, conclusions/confidence, build bounds, disproven explanations, mutations/rollback, fidelity gaps, and the next owning workflow.

## Handoffs

- `macos-privacy-permissions-workflow`: supported app-facing privacy implementation and responsible-code diagnosis.
- `macos-sandbox-file-access-workflow`: containers, user selection, bookmarks, App Groups, and supported persistent file access.
- `diagnose-apple-entitlements`: source/profile/signed/runtime comparison for ordinary products.
- `macos-distribution-workflow`: Gatekeeper/notarization/Hardened Runtime repair for exported products.
- `assess-macos-threat`, `inspect-macos-runtime-activity`, or `contain-and-recover-macos`: suspicious-host defensive work.
- `report-apple-security-research`: a formal reproducible security report after the technical finding exists.
