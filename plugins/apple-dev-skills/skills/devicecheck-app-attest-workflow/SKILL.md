---
name: devicecheck-app-attest-workflow
description: Guide DeviceCheck and App Attest adoption in Apple-platform apps using DCDevice, DCAppAttestService, app IDs, entitlements, server challenges, attestation objects, assertions, receipts, fraud-risk metrics, sandbox/production environments, rollout planning, and explicit client/server handoffs. Use when implementing or diagnosing DeviceCheck per-device two-bit state, App Attest app-instance integrity, Apple server API validation, App Attest environment setup, macOS App Attest verification, App Clip key-sharing, supported extension contexts, or fraud-risk integration that must be checked against current Apple documentation.
---

# DeviceCheck App Attest Workflow

## Purpose

Guide DeviceCheck and App Attest implementation decisions without confusing app-side Apple framework calls with server-side trust decisions.

The practical decision is whether the app needs DeviceCheck two-bit device state, App Attest app-instance integrity, both signals, or a different auth/session/sync workflow. The skill keeps Apple docs, Xcode signing state, server challenges, replay protection, rollout constraints, and backend handoffs visible before implementation starts.

## When To Use

- Use this skill when adding or diagnosing `DCDevice`, `generateToken(completionHandler:)`, Apple DeviceCheck query/update/validate endpoints, or the two per-device bits Apple stores for an app.
- Use this skill when adding or diagnosing `DCAppAttestService`, `generateKey(completionHandler:)`, `attestKey(_:clientDataHash:completionHandler:)`, `generateAssertion(_:clientDataHash:completionHandler:)`, or `DCError`.
- Use this skill when the work involves App Attest App ID registration, DeviceCheck capabilities, the `com.apple.developer.devicecheck.appattest-environment` entitlement, sandbox versus production behavior, TestFlight or App Store rollout, Enterprise distribution, Developer ID, or macOS signing validation.
- Use this skill when the app and server need a challenge, attestation, assertion, receipt, public-key, counter, or fraud-risk metric contract.
- Use this skill when replacing custom device identifiers, local-only jailbreak checks, receipt-only abuse checks, or ad hoc risk flags with Apple-supported DeviceCheck or App Attest signals.
- Recommend `swift-openapi-client-workflow` when the primary task is generated API client setup for the app-to-server transport.
- Recommend `xcode-build-run-workflow` when the next step is target setup, entitlements, signing, App ID capability wiring, build, run, simulator, device, or guarded Xcode project mutation.
- Recommend `xcode-testing-workflow` when the next step is repeatable XCTest, XCUITest, simulator/device matrix checks, or test-plan setup.
- Recommend server-side Swift, OpenAPI, RPC, or backend-specific workflows when the primary task is implementing server verification, persistence, JWT generation, API routes, or fraud-risk policy.
- Recommend the broader client auth and sync workflow when the request is really Keychain storage, Sign in with Apple, `ASWebAuthenticationSession`, token refresh, logout, multi-account state, or app sync.

## Single-Path Workflow

1. Classify the integrity request:
   - DeviceCheck two-bit state with `DCDevice`
   - App Attest app-instance integrity with `DCAppAttestService`
   - combined DeviceCheck plus App Attest risk signal
   - App ID, entitlement, signing, or environment setup
   - server verification, receipt, counter, or fraud metric work
   - broader auth, Keychain, token refresh, generated client, or app-sync work
2. Apply the Apple docs gate before recommending shape:
   - read the relevant DeviceCheck, App Attest, entitlement, CryptoKit, code-signing, or platform documentation first
   - state the documented Apple behavior being relied on
   - if Apple docs and current code disagree, stop and surface that conflict
   - if no relevant Apple documentation can be found, say that explicitly before proceeding
3. Choose the supported signal:
   - use DeviceCheck when the server needs Apple-hosted per-device two-bit state for a narrow abuse, promotion, or fraud flag
   - use App Attest when the server needs evidence that a request comes from a legitimate app instance using an attested key
   - use both only when the risk policy has a concrete reason to combine per-device state with app-instance assertions
   - do not use either as a replacement for user authentication, authorization, server-side rate limiting, or normal abuse monitoring
4. Plan the client/server boundary:
   - app checks availability and requests server challenges
   - app generates DeviceCheck tokens, App Attest keys, attestations, or assertions
   - server verifies tokens, attestations, assertions, receipts, counters, app identifiers, environments, and replay protections
   - server owns the risk decision and user-visible fallback behavior
5. Plan storage and lifecycle:
   - persist App Attest key identifiers because the private key is not directly readable and the key ID cannot be recovered later
   - do not persist server challenges for reuse
   - keep development/sandbox and production App Attest records separate
   - expect App Attest keys to survive ordinary app updates but not reinstall, migration, or device restore
   - keep DeviceCheck bit meanings documented server-side
6. Plan rollout and validation:
   - handle unsupported devices gracefully on both client and server
   - model sandbox and production endpoint differences before rollout
   - avoid immediate large-population App Attest onboarding when Apple guidance calls for ramping
   - route Xcode signing, entitlements, build, run, simulator, and device checks to Xcode skills
7. Return one recommendation path with:
   - selected signal
   - documented Apple behavior relied on
   - app calls and storage plan
   - server verification and persistence plan
   - environment and entitlement plan
   - validation and rollout plan
   - explicit handoffs for Xcode, generated clients, backend implementation, broader auth, or docs lookup

## Inputs

- `request`: optional free-text DeviceCheck or App Attest task.
- `signal_goal`: optional emphasis such as `device-state`, `app-integrity`, `combined-risk`, `entitlement-setup`, `server-validation`, or `unknown`.
- `platform_context`: optional emphasis such as `ios`, `macos`, `watchos`, `tvos`, `visionos`, `app-clip`, `extension`, or `mixed-apple`.
- `distribution_context`: optional emphasis such as `development`, `sandbox`, `testflight`, `app-store`, `enterprise`, `developer-id`, or `unknown`.
- `server_context`: optional backend shape such as `swift-server`, `openapi`, `rpc`, `node`, `python`, `existing-api`, or `unknown`.
- Defaults:
  - docs-first guidance always applies
  - prefer one signal until the risk policy justifies combining them
  - keep app-side framework calls and server-side trust decisions separate
  - route Xcode state mutation and backend implementation to the owning workflow

## Outputs

- `status`
  - `success`: the request belongs to this workflow and a DeviceCheck or App Attest recommendation is ready
  - `handoff`: the request belongs to another workflow after DeviceCheck/App Attest-aware classification
  - `blocked`: the request lacks enough app, server, entitlement, environment, or docs evidence for a trustworthy recommendation
- `path_type`
  - `devicecheck`: the recommendation uses `DCDevice` and Apple DeviceCheck server APIs
  - `app-attest`: the recommendation uses `DCAppAttestService` and App Attest server verification
  - `combined`: the recommendation intentionally combines DeviceCheck and App Attest risk signals
  - `handoff`: the recommendation belongs to Xcode, generated client, backend, broader auth, sync, or docs workflow
- `output`
  - selected signal and reason
  - documented Apple behavior relied on
  - app-side framework calls and storage lifecycle
  - server challenge, verification, persistence, and replay-protection plan
  - App ID, entitlement, signing, environment, and rollout notes
  - validation plan and manual-validation gaps
  - recommended workflow handoffs when needed

## Guards and Stop Conditions

- Do not claim DeviceCheck or App Attest proves a device operating system is uncompromised; Apple positions these as risk signals, not absolute fraud prevention.
- Do not pretend the app can validate its own integrity locally. App Attest trust decisions require server-side challenge and verification.
- Do not reuse App Attest challenges or client data blocks. Use unique, single-use server challenges to reduce replay risk.
- Do not reuse one App Attest key across multiple users on the same device.
- Do not discard a key after `serverUnavailable`; retry later with the same key and same `clientDataHash` when Apple documents that behavior.
- Do not mix sandbox and production App Attest keys, receipts, endpoints, or server records.
- Do not store Apple private keys, authentication keys, JWT signing keys, App Attest receipts, challenges, assertions, or device tokens in logs.
- Do not treat DeviceCheck's two bits as user identity, durable account state, or a substitute for server-side authorization.
- Do not hand-edit Xcode project or entitlement state casually; route Xcode-managed changes to `xcode-build-run-workflow`.
- Stop with `blocked` when the task requires Apple Developer account access, server secrets, production rollout approval, or live device evidence that is not available.

## Fallbacks and Handoffs

- Recommend `explore-apple-swift-docs` when the real need is direct Apple documentation lookup for DeviceCheck, App Attest, CryptoKit, entitlements, code signing, or platform availability.
- Recommend `xcode-build-run-workflow` when the next step is App ID capability setup, entitlements, provisioning, signing, build, run, simulator, device, or target membership follow-through.
- Recommend `xcode-testing-workflow` when the next step is repeatable XCTest/XCUITest, sandbox/production test matrices, simulator/device checks, or `.xctestplan` setup.
- Recommend `swift-openapi-client-workflow` when the app-to-server request or generated client contract is the primary implementation work.
- Recommend server-side Swift, OpenAPI, RPC, or backend-specific workflows when the server must verify attestation objects, assertions, DeviceCheck tokens, receipts, JWT authentication, counters, public keys, or fraud-risk policy.
- Recommend the broader client auth and app-sync workflow when the task is Keychain storage, Sign in with Apple, `ASWebAuthenticationSession`, token refresh, logout, multi-account state, offline edits, or sync conflict handling.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode-project policy for a repo that will own DeviceCheck capabilities, entitlements, signing, and target membership.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` exists to preserve the repo-wide customization-file contract, but the first version of this skill defines no runtime-enforced knobs.

Keep the first release focused on DeviceCheck/App Attest classification, docs grounding, and handoffs. If future iterations add deterministic checks for entitlements, server validation fixtures, or rollout policy, document the knobs before runtime behavior depends on them.

## References

### Workflow References

- `references/devicecheck-device-state.md`
- `references/app-attest-client-flow.md`
- `references/app-attest-server-validation.md`
- `references/entitlements-app-id-and-validation.md`
- `references/customization-flow.md`

### Support References

- Recommend `explore-apple-swift-docs` when the user needs current Apple docs before a DeviceCheck or App Attest implementation choice.
- Recommend `xcode-build-run-workflow` when the user needs target, signing, entitlement, provisioning, build, run, or install follow-through.
- Recommend `xcode-testing-workflow` when the user needs repeatable simulator, device, assertion, environment, or server-contract test design.
- Recommend `swift-openapi-client-workflow` when generated app-to-server client work is the main change.
- Recommend `references/snippets/apple-xcode-project-core.md` when the user needs reusable Xcode project guidance for DeviceCheck and App Attest capability work.

### Script Inventory

- `scripts/customization_config.py`
