---
name: apple-developer-provisioning-workflow
description: Plan and safely automate officially supported Apple Developer provisioning and CloudKit workflows through the App Store Connect REST API, Xcode-aware local discovery, cktool, and CKTool JS. Use when inspecting or changing bundle IDs, capabilities, certificates, devices, provisioning profiles, CloudKit schemas, or sandbox test data while keeping portal-only configuration, credentials, dry runs, and confirmation gates explicit.
---

# Apple Developer Provisioning Workflow

## Purpose

Guide Apple Developer provisioning and CloudKit work without treating the Developer Portal as an undocumented API. The supported automation path is the App Store Connect REST provisioning API for bundle IDs, capabilities, certificates, devices, and profiles; `xcrun cktool` or CKTool JS for existing CloudKit containers; and local Xcode or `xcrun mcpbridge` discovery when a project-aware view improves safety.

The workflow never commits a `.p8` key, CloudKit token, JWT, profile payload, or local signing material. It plans first, reads state before changing it, uses short-lived JWTs only in the invoking process, and requires an explicit confirmation immediately before every create, update, revoke, delete, reset, or schema/data apply operation.

## When To Use

- Use this skill for App Store Connect API provisioning work involving registered bundle IDs, supported capabilities, certificates, devices, and provisioning profiles.
- Use this skill for a plan or dry run that compares an Xcode project’s bundle IDs, entitlements, signing settings, and installed profiles with Apple’s current state.
- Use this skill for existing CloudKit container schema export, schema apply, sandbox reset, or test-data workflows through `xcrun cktool` or the TypeScript-ready CKTool JS packages.
- Use this skill when deciding whether an action remains official REST/CLI automation or must be completed in the Apple Developer Portal.
- Recommend `xcode-build-run-workflow` for target edits, entitlements, signing settings, build, device, or profile-install follow-through.
- Recommend `xcode-coding-intelligence-workflow` for a running Xcode session or external access through `xcrun mcpbridge`.
- Recommend `explore-apple-swift-docs` when current Apple documentation is the primary need.

## Single-Path Workflow

1. Establish the account and credential boundary:
   - confirm an active Apple Developer Program or Enterprise Program membership and the selected team;
   - for provisioning endpoints, require a **team** App Store Connect API key with the least sufficient role; individual API keys cannot use provisioning endpoints;
   - retain the issuer ID, key ID, and downloaded `.p8` private key only in local secret storage such as Keychain or an approved local secret manager; never place them in the repo, project settings, CI logs, shell history, or agent transcript;
   - create a short-lived JWT locally for one invocation and avoid writing it to disk;
   - for CloudKit, separately obtain a CloudKit management token from CloudKit Console and save it through `xcrun cktool save-token --type management` so macOS Keychain owns it.
2. Discover before mutating:
   - inspect the project’s bundle identifiers, entitlements, signing configuration, and existing profiles through Xcode-local tools or `xcrun mcpbridge` when Xcode is open;
   - list the matching App Store Connect bundle IDs, capabilities, certificates, devices, and profiles with read-only REST requests;
   - export the current CloudKit schema and identify the team ID, container ID, and sandbox versus production environment before selecting `cktool` or CKTool JS;
   - return a plan with exact proposed requests, affected IDs, expected profile relationships, and portal-only steps.
3. Classify each requested operation:
   - official REST: registered bundle IDs, supported bundle-ID capabilities, certificates, devices, provisioning profiles, and their documented relationships;
   - official local CloudKit: schema export/apply, sandbox reset, and test-data work on an already registered container via `cktool` or CKTool JS;
   - portal-only: App Group registration or assignment, CloudKit container registration or assignment to an App ID, Service ID registration, and any identifier/capability action absent from the current REST resource set;
   - unsupported or unclear: stop, preserve the plan, and link to the exact portal surface instead of guessing an endpoint.
4. Require confirmation for mutations:
   - show the exact create, update, revoke, delete, reset, schema-apply, or test-data command/request and name every affected team, identifier, certificate, device, profile, container, environment, and destructive consequence;
   - default to dry-run/plan output; do not use a broad "yes" captured earlier in the conversation;
   - re-read server state after a mutation and report the resulting IDs without emitting secrets.
5. Choose the CloudKit adapter deliberately:
   - use `xcrun cktool` for interactive local, one-off, Keychain-backed work;
   - use CKTool JS in a TypeScript/pnpm project when schema or test-data operations belong in typed integration automation. Use `@apple/cktool.database` with `@apple/cktool.target.nodejs`, inject the management token from local secret storage at runtime, and never commit it;
   - treat production schema deployment, schema resets, and data deletion as high-impact operations requiring a separate explicit confirmation and a backup/export plan.
6. Hand off project mutation and validation:
   - make entitlement and signing changes through Xcode-aware workflows rather than hand-editing project state;
   - regenerate or download a profile only after its certificate, device, and bundle-ID inputs are confirmed;
   - validate with the narrowest appropriate build/signing or CloudKit sandbox test after state is updated.

## Inputs

- `request`: desired provisioning or CloudKit outcome.
- `team_context`: Apple Developer team ID, program type, and account role, when available.
- `project_context`: Xcode project/workspace, target, bundle ID, entitlements, and signing mode.
- `operation_mode`: `inspect`, `plan`, `apply`, `portal-only`, or `unknown`; default is `plan`.
- `cloudkit_context`: existing container ID, environment, schema/data intent, and whether `cktool` or a TypeScript integration harness is preferred.
- Defaults:
  - read-only discovery and a concrete plan precede every mutation;
  - secrets stay local and short-lived;
  - an explicit current confirmation is required for mutation;
  - portal-only operations stay portal-only until Apple documents an official API.

## Outputs

- `status`
  - `success`: supported read-only discovery or a confirmed, verified mutation completed.
  - `plan`: the supported requests and portal tasks are ready, but no mutation has occurred.
  - `portal-only`: the requested configuration needs Apple Developer Portal interaction.
  - `blocked`: account role, team key, CloudKit token, project evidence, docs, or confirmation is missing.
- `path_type`
  - `app-store-connect-provisioning`, `xcode-discovery`, `cloudkit-cktool`, `cloudkit-js`, `portal-only`, or `handoff`.
- `output`
  - documented Apple behavior relied on;
  - account/key prerequisites and the local-secret boundary;
  - discovered state and an ordered dry-run plan;
  - exact mutation confirmation prompt when applicable;
  - portal-only tasks and a safe handoff;
  - validation evidence and remaining manual gaps.

## Guards and Stop Conditions

- Do not use an individual API key for provisioning endpoints; Apple documents that individual keys cannot use them.
- Do not commit, paste, log, or transmit `.p8` private keys, App Store Connect JWTs, CloudKit management tokens, user tokens, profile contents, certificate private keys, or Keychain exports.
- Do not create a persistent JWT, store an API key in an entitlement, or expose it to a client app.
- Do not represent App Group registration/assignment, CloudKit container registration/assignment, Service IDs, or undocumented portal configuration as supported REST automation.
- Do not create an App Store app record or upload a build through this provisioning workflow; those remain website/Xcode/Transporter operations as Apple documents.
- Do not reset a CloudKit schema, apply a production schema, delete a certificate/profile/device, revoke a key, or alter test data without an operation-specific confirmation after the plan is shown.
- Do not make Xcode project or entitlement edits without routing through `xcode-build-run-workflow`.
- Stop with `blocked` when the chosen team lacks an eligible team API key, required role, CloudKit management token, a confirmed target/container/environment, or fresh mutation confirmation.

## Fallbacks and Handoffs

- Recommend `xcode-build-run-workflow` for entitlement, signing, target, build, profile-install, simulator, or device validation work.
- Recommend `xcode-coding-intelligence-workflow` for Xcode-hosted inspection or external access through `xcrun mcpbridge`; it owns the running-Xcode and permissions boundary.
- Recommend `explore-apple-swift-docs` for current App Store Connect, Xcode, CloudKit, or entitlement documentation lookup.
- Use the Apple Developer Portal manually for App Groups, CloudKit-container registration or App-ID assignment, Service IDs, and any capability configuration Apple does not expose through the current REST API.
- Recommend `references/snippets/apple-xcode-project-core.md` when a repository needs durable Xcode-project guidance for entitlements, signing, and project-integrity follow-through.

## Customization

Use `references/customization-flow.md`.

This workflow intentionally has no runtime-enforced mutation override. Customization can record a preferred discovery mode and CloudKit adapter, but it cannot bypass plan-first behavior, local-secret handling, portal-only classification, or explicit per-operation confirmation.

## References

### Workflow References

- `references/app-store-connect-provisioning.md`
- `references/cloudkit-automation.md`
- `references/portal-only-configuration.md`
- `references/customization-flow.md`

### Support References

- [App Store Connect API provisioning overview](https://developer.apple.com/app-store-connect/api/) documents the REST surface for bundle IDs, certificates, devices, and profiles.
- [Creating API keys](https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api) documents team versus individual key limits and JWT authorization.
- [Using cktool](https://developer.apple.com/icloud/ck-tool/) documents management-token setup and Keychain-backed local use.
- [CKTool JS](https://developer.apple.com/documentation/cktooljs/) documents the official JavaScript client modules for CloudKit automation.
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode project policy.

### Script Inventory

- `scripts/customization_config.py`
