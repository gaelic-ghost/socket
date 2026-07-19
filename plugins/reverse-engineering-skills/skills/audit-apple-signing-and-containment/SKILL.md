---
name: audit-apple-signing-and-containment
description: Audit Apple code signatures, code directories, CDHashes, authorities, Team IDs, designated requirements, provisioning profiles, entitlements, hardened runtime, library validation, notarization, App Sandbox, SIP, Data Vaults, and platform-binary context. Use when Codex must explain an Apple artifact's declared identity and containment state, compare original and re-signed copies, or separate signed claims from access observed at runtime.
---

# Audit Apple Signing And Containment

## Overview

Inspect the original signature and declared capabilities before any transformation. Treat signing, notarization, sandboxing, SIP, and runtime access as related but distinct evidence.

Read [references/apple-signing-and-containment.md](references/apple-signing-and-containment.md) when interpreting signature layers, provisioning, mandatory access controls, or current Apple security documentation.

## Workflow

1. Fix artifact identity.
   - Record hash, UUID, bundle identifier and build, architecture, acquisition source, and whether the artifact is original, extracted, patched, or re-signed.

2. Inspect the signature without changing it.
   - Record code-directory versions and hashes, CDHash, signing authorities, Team ID, identifier, designated requirement, flags, and nested-code verification results.
   - Record unsigned or ad hoc state precisely instead of collapsing it into `invalid`.

3. Inspect provisioning when present.
   - Record application identifier, Team ID, platform, expiration, device scope, and profile entitlements.
   - Compare profile entitlements with the executable's signed entitlements rather than treating either set alone as the effective runtime state.

4. Inventory declared entitlements.
   - Preserve entitlement keys and values exactly.
   - Classify public capability, private or undocumented key, debugger/development capability, sandbox declaration, and environment-specific value only when supported by current sources.

5. Inspect containment context.
   - Record hardened runtime, library validation, App Sandbox, platform-binary clues, notarization evidence, SIP or system security state, and relevant Data Vault or mandatory access-control boundaries.
   - Distinguish host policy, process signature state, user consent, and service-mediated authorization.

6. Compare with observed access.
   - State `declares entitlement X` separately from `operation Y succeeded in environment Z`.
   - Record OS build, hardware, process path, signing state, and reproduction steps for runtime observations.

7. Compare transformed copies.
   - Create a transformation record for every re-sign, entitlement edit, binary patch, or bundle change.
   - Treat the transformed copy as a new behavioral artifact and never attribute its result to the original signature.

8. Route ordinary app signing, provisioning, notarization, or distribution work to `apple-dev-skills` after the artifact audit is complete.
   - Route private entitlement enforcement, TCC/sandbox attribution, Gatekeeper/XProtect internals, or other exact-build control questions to `research-macos-security-control` with this signature record.

## Guardrails

- Do not re-sign merely to make inspection convenient.
- Do not claim root access bypasses SIP, sandbox profiles, Data Vaults, TCC, or other mandatory controls.
- Do not treat successful signature verification as proof of trust, safety, notarization, or runtime authorization.
- Live-check entitlement availability and enforcement claims for the exact OS build when they affect a conclusion.

## Output

Return artifact identity, signature report, provisioning and entitlement comparison, containment context, observed-versus-declared access, transformations, and unresolved policy questions.
