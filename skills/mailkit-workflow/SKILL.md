---
name: mailkit-workflow
description: Design macOS MailKit extensions for content blocking, message actions, compose sessions, and message security with explicit privacy, capability, target, and validation boundaries. Use when a macOS app needs to extend Apple Mail.
metadata:
  hermes:
    category: apple-development
    tags: [apple, macos, mailkit, mail, app-extension, privacy, security]
---

# MailKit Workflow

## Purpose

Design macOS MailKit app extensions around Apple Mail’s documented handler model. MailKit supplies an `MEExtension` entry point and four distinct capabilities: content blocking, message actions, compose-session handling, and message security. This skill owns that Mail-specific behavior and its privacy boundary.

It does not own a mail server, IMAP/SMTP transport, account provisioning, general authentication, generic extension mechanics, or Messages/iMessage collaboration.

## When To Use

- Use this skill when a macOS app needs a MailKit extension that blocks remote content, acts on downloaded messages, participates in composition, or secures messages.
- Use this skill when selecting `MEContentBlocker`, `MEMessageActionHandler`, `MEComposeSessionHandler`, or `MEMessageSecurityHandler` and their `MEExtensionCapabilities` declaration.
- Use `app-extension-architecture-workflow` when the extension point or app/extension target architecture is not yet settled.
- Use `file-provider-and-finder-sync-workflow` for remote files and Finder behavior, not message attachments or mail synchronization.
- Use Messaging Collaboration Skills for Messages/iMessage, communication notifications, VoIP, or Push to Talk behavior.
- Recommend `xcode-build-run-workflow`, `xcode-testing-workflow`, and `macos-distribution-workflow` for their respective execution boundaries.

## Single-Path Workflow

1. Classify the MailKit capability:
   - use a content blocker for declarative remote-content rules shown in Mail
   - use message actions for a decision as Mail downloads a message
   - use compose sessions for recipient validation, compose-window UI, delivery suitability, or custom headers
   - use message security for encryption and digital signatures
   - split capabilities only when each one has a concrete Mail behavior and privacy case
2. State the documented MailKit behavior relied on:
   - `MEExtension` supplies handlers for the capabilities declared in `MEExtensionCapabilities`
   - enabled content-blocking extensions continue to apply their rules even when a person asks Mail to load remote content
   - message action decisions run as Mail downloads messages, not as a retroactive bulk-mail automation contract
   - compose-session approval is a delivery gate, not an excuse to silently alter recipient intent
3. Set up the target boundary:
   - keep the containing macOS app responsible for onboarding, settings, account-independent configuration, and user explanation
   - keep the Mail extension responsible for its selected MailKit handlers and short, deterministic decisions
   - declare only the chosen capabilities in the extension’s `Info.plist`; do not advertise handlers that are not implemented
4. Design each handler conservatively:
   - content blocker: generate narrow JSON rules, explain their effect, and provide a test corpus for allowed and blocked content
   - message action: use explicit, explainable rules and avoid irreversible actions unless the user has made the policy clear
   - compose session: validate only what the feature needs, provide focused UI when justified, fail delivery with a concrete user-readable reason, and make custom headers intentional
   - message security: identify key material, trust policy, signing/encryption state, user consent, failure recovery, and interoperable message expectations before implementation
5. Protect mail data:
   - minimize access to message bodies, recipients, headers, attachments, and remote-content identifiers
   - do not log raw message content, addresses, tokens, cryptographic material, or full headers
   - keep any shared configuration separate from message-derived data; use an App Group only when the app and extension have a documented shared-data need
6. Validate in layers:
   - verify the macOS target, extension point, `MEExtensionCapabilities`, signing, embedding, install, and Mail enablement state
   - test representative messages and account states in a non-production mailbox
   - test content-blocker rules, action decisions, compose allow/deny outcomes and UI, or security encryption/signature success and failure paths as applicable
   - prove that disabled, interrupted, malformed, missing-key, and offline conditions produce clear behavior without leaking mail data
7. Return the chosen handler set, documented behavior, Mail/app data boundary, privacy policy, validation matrix, and next handoff.

## Inputs

- `request`: optional Mail integration request.
- `capability`: optional `content-blocker`, `message-action`, `compose-session`, `message-security`, or `unknown`.
- `data_policy`: optional restrictions for message bodies, metadata, shared settings, key material, and logs.
- `distribution`: optional development, notarized, App Store, or unknown path.
- Defaults:
  - macOS MailKit only
  - least-privilege handler set
  - no message-content retention or external transmission without an explicit product decision
  - focused MailKit handler tests before broad delivery claims

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `mailkit_plan`:
  - selected capability or capabilities and documented behavior relied on
  - target, `Info.plist`, handler, and user-control boundary
  - message-data, privacy, logging, key-material, and shared-state plan
  - handler-specific test cases and distribution validation
  - explicit next workflow handoff

## Guards and Stop Conditions

- Do not describe MailKit as a general-purpose mail transport, mailbox sync engine, or arbitrary Apple Mail UI automation API.
- Do not use content blocking to bypass user intent; enabled MailKit content blockers have durable effects in Mail.
- Do not silently alter, archive, flag, sign, encrypt, reject, or add headers to messages without a documented handler contract and clear user-facing policy.
- Do not retain or log raw message data, recipient addresses, headers, attachment contents, secret keys, signatures, or decrypted content by default.
- Do not confuse Message Filter extensions, Messages/iMessage apps, or Safari content blockers with MailKit.
- Stop with `blocked` when the requested feature needs unsupported message access, undocumented Mail control, hidden recipient manipulation, or security/key-management behavior that has not been designed and validated.

## Fallbacks and Handoffs

- Recommend `app-extension-architecture-workflow` for reusable target, lifecycle, entitlement, shared-container, and process-isolation design.
- Recommend `xcode-build-run-workflow` for the Mail extension target, capability configuration, signing, embedding, install, and Mail enablement work.
- Recommend `xcode-testing-workflow` for repeatable handler, message-fixture, and UI validation.
- Recommend `macos-distribution-workflow` for release signing, notarization, Gatekeeper, and artifact evidence.
- Recommend `explore-apple-swift-docs` when current MailKit symbols or capability behavior need source-specific confirmation.
- Recommend `references/snippets/apple-xcode-project-core.md` for reusable containing-app and extension-target project guidance.

## Customization

Use `references/customization-flow.md`.

`scripts/customization_config.py` preserves the common customization-file contract. Mail handler choice, message policy, and security decisions remain project-specific and must not be converted into opaque persistent defaults.

## References

### Workflow References

- `references/mailkit-capabilities-and-handler-boundaries.md`
- `references/privacy-security-and-validation.md`
- `references/customization-flow.md`

### Authoritative Sources

- [MailKit](https://developer.apple.com/documentation/mailkit)
- [MEExtension](https://developer.apple.com/documentation/mailkit/meextension)
- [Build Mail App Extensions](https://developer.apple.com/documentation/mailkit/build-mail-app-extensions)

### Support References

- Recommend `references/snippets/apple-xcode-project-core.md` for reusable Xcode project guidance for MailKit app and extension targets.

### Script Inventory

- `scripts/customization_config.py`
