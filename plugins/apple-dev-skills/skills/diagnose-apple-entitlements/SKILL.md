---
name: diagnose-apple-entitlements
description: Diagnose why an Apple capability or entitlement is missing, rejected, ineffective, or different across app, helper, extension, XPC, daemon, build, archive, export, and runtime states. Use when a capability appears in Xcode or an entitlements file but is absent from a profile or final signature, an exported artifact differs from Debug, a nested executable fails authorization, a restricted/private entitlement is suspected, or runtime policy and user consent must be separated from signed declarations.
---

# Diagnose Apple Entitlements

## Purpose

Trace one desired behavior through tracked project source, developer-account/profile authorization, the final signed artifact and all nested code, and the observed runtime result. Identify the owner that must change without treating an entitlement as user consent or successful access.

## When To Use

- Use for capability/entitlement/profile mismatches, export-only failures, nested-code differences, restricted entitlement questions, and re-signed artifacts.
- Use before editing project settings when the actual owner could be the developer account, profile, signer, export transform, runtime policy, or user decision.
- Do not use to invent or recommend private entitlements for ordinary third-party products.

## Single-Path Workflow

1. Define the desired operation, target, platform/OS, distribution channel, artifact, and exact runtime error. Apply the Apple docs gate through `explore-apple-swift-docs` and establish whether current Apple documentation requires or permits the capability.
2. Create the five-state record in `references/five-state-entitlement-comparison.md`: desired behavior, tracked source, account/profile authorization, signed result, and runtime result.
3. Inspect tracked source: Xcode capability, `.entitlements`, Info.plist usage description, build settings, target membership, helper/extension/XPC configuration, generated-project source, configuration, and archive/export settings.
4. Inspect account authorization: Team/App ID, capability enablement, restricted-entitlement approval, certificate, provisioning profile entitlements, environment/device scope, and whether the change is portal-only or API-supported.
5. Treat the actual built/exported artifact as source of truth for signed state. Follow `references/artifact-and-nested-code-inspection.md` for the main executable, helpers, extensions, XPC services, frameworks, daemons/tools, and embedded profiles.
6. Compare exact keys and values. Preserve public, restricted, private/undocumented, development-only, environment, and exception classifications only when supported by current evidence. Read `references/restricted-and-private-entitlements.md`.
7. Evaluate runtime controls separately: App Sandbox, Hardened Runtime, library validation, TCC/user consent, service authorization, Gatekeeper/notarization, Data Vault/SIP/platform policy, and responsible process identity.
8. If the artifact was re-signed, patched, exported differently, or otherwise transformed, record a new artifact identity and invalidate assumptions about the original signature/notarization behavior.
9. Classify the mismatch and select exactly one next owner using `references/routing-and-validation.md`. Make the source/account/build change through that owner's workflow, rebuild/export, and repeat the signed and runtime comparisons.
10. Report every state, exact mismatch, owner, evidence/confidence, validation result, and what remains unproven.

## Inputs

- desired behavior, target/platform/OS, distribution channel, artifact, and exact error
- project/capability source, build settings, entitlements, Info.plist, and target graph
- Team/App ID/profile/certificate/approval context
- signed main and nested artifacts, embedded profiles, transformations, and runtime environment

## Outputs

- five-state entitlement comparison with exact key/value differences
- entitlement classification and responsible owner
- minimum correction/rebuild/export path
- final signed-artifact and runtime validation result with remaining uncertainty

## Guards and Stop Conditions

- Do not invent entitlement keys, values, availability, restricted approval, or profile support.
- Do not hand-edit generated project/profile artifacts or casually re-sign a bundle to hide a source mismatch.
- Do not call an entitlement effective until the final responsible executable and required runtime operation are checked.
- Do not confuse a usage description, capability, entitlement, sandbox exception, profile allowance, or user consent.
- Stop when the actual artifact or responsible nested executable is unavailable; report source-only conclusions as unverified.

## Fallbacks and Handoffs

- Use `apple-developer-provisioning-workflow` for App ID, capability, certificate, profile, or account-side changes.
- Use Xcode project/build workflows for tracked capability, target, signing, archive, and export changes.
- Use `macos-distribution-workflow` for Hardened Runtime, nested signing, Gatekeeper, notarization, and stapling.
- Use `macos-privacy-permissions-workflow` for user or managed privacy authorization.
- Use `audit-apple-signing-and-containment` for forensic artifact audit and `research-macos-security-control` for private entitlement or exact-build enforcement research.

## Customization

Use `references/customization-flow.md`. The workflow has no runtime knobs; comparison states and evidence levels may not be skipped.

## References

- `references/five-state-entitlement-comparison.md`
- `references/restricted-and-private-entitlements.md`
- `references/artifact-and-nested-code-inspection.md`
- `references/routing-and-validation.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the correction belongs to an Xcode target or build configuration.
- [Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements)
- [Diagnosing issues with entitlements](https://developer.apple.com/documentation/bundleresources/diagnosing-issues-with-entitlements)
