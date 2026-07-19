---
name: macos-distribution-workflow
description: Inspect, prepare, validate, and troubleshoot exported macOS distribution artifacts. Use when checking signing identities, entitlements, hardened runtime, nested code, Gatekeeper, notarization readiness/results, stapling, or distribution-only launch failures.
---

# macOS Distribution Workflow

## Purpose

Treat a signed exported artifact as the source of truth for macOS distribution diagnosis. This workflow distinguishes project/account provisioning from artifact trust: inspect the bundle, classify the failure, and use the minimum verifiable repair or release-validation path.

## When To Use

- Use for `.app`, `.pkg`, or disk-image distribution artifacts; signing state; entitlements; hardened runtime; nested signatures; Gatekeeper; notarization; stapling; and direct-distribution failures.
- Do not use for ordinary Debug builds, account-side certificate/profile creation, or project signing-setting edits without an artifact diagnosis.

## Single-Path Workflow

1. Apply the Apple docs gate through `explore-apple-swift-docs`. Confirm the distribution channel and current signing/notarization requirement before acting.
2. Identify the exact artifact, distribution channel, main executable, nested frameworks/helpers/extensions, signing identity, and observed user-visible failure.
3. Read `references/artifact-inspection-and-classification.md` and inspect bundle structure, signature details, entitlements, nested code, and Gatekeeper assessment before prescribing a fix.
4. Classify the problem: unsigned/ad hoc signing, wrong identity, entitlement mismatch, hardened-runtime issue, nested-code ordering issue, sandbox issue, Gatekeeper assessment, or notarization/stapling readiness.
5. Keep account-side provisioning with `apple-developer-provisioning-workflow`; keep project signing or entitlement edits with `xcode-build-run-workflow`. Do not hand-edit/re-sign a built artifact as a first response to a project configuration problem.
6. For direct distribution, validate the outermost deliverable, notarization result, and stapling state appropriate to the chosen package shape. Keep local-debug validity distinct from distribution readiness.
7. Report the inspected artifact, evidence, failure class, smallest repair path, and the validation that remains after repair.

## Inputs

- exported artifact path and intended distribution channel
- signing identity/entitlement context and nested-code shape
- observed launch, Gatekeeper, notarization, or upload failure
- current Xcode/macOS version and any prior validation output

## Outputs

- artifact inspection result and precise failure classification
- project, account, or artifact owner for the next repair
- minimum validation sequence and distribution-readiness state

## Guards and Stop Conditions

- Do not call notarization necessary for a normal local Debug run.
- Do not invent entitlements, signing identities, or distribution certificates.
- Do not treat a project setting as verified until the exported artifact was inspected.
- Do not re-sign an artifact casually; re-signing can invalidate nested signatures, profiles, or a prior notarization result.
- Stop when the distribution channel, actual artifact, or signing evidence is missing.

## Fallbacks and Handoffs

- Recommend `diagnose-apple-entitlements` when source, profile, main or nested signed entitlements, and runtime authorization need a five-state comparison before choosing a repair owner.
- Recommend `apple-developer-provisioning-workflow` for documented account-side certificates, profiles, and identifier/capability state.
- Recommend `xcode-build-run-workflow` for entitlement/project-signing changes, archive/export, and build validation.
- Recommend `explore-apple-swift-docs` for current signing, notarization, or distribution policy.

## Customization

Use `references/customization-flow.md`. Distribution validation is artifact- and channel-specific, so this workflow provides no shortcut that can skip signature, Gatekeeper, or notarization evidence.

## References

- `references/artifact-inspection-and-classification.md`
- `references/customization-flow.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the app needs reusable Xcode-project policy alongside distribution work.
- [Packaging Mac software for distribution](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution) documents distribution packaging and notarization context.
