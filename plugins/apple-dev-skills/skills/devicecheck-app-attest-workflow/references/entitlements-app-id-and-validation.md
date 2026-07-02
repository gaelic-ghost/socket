# Entitlements, App ID, and Validation

Use this reference when the request involves Apple Developer setup, App ID registration, entitlements, signing, environments, rollout, or Xcode validation for DeviceCheck or App Attest.

## App ID and Capability Setup

DeviceCheck and App Attest require an app ID registered through Apple Developer account surfaces. Before implementation claims are made, verify the bundle identifier, App ID prefix or Team ID, target platform, and distribution context.

When the change touches Xcode project state, provisioning, entitlements, target membership, signing certificates, or capabilities, hand the mutation to `xcode-build-run-workflow`.

## App Attest Environment

Apple documents separate development/sandbox and production behavior for App Attest:

- During development, App Attest uses sandbox behavior by default.
- Production behavior can be requested during development with the App Attest environment entitlement set to `production`.
- Distributed apps operate in production mode.
- Sandbox keys and receipts cannot be used in production.
- Production keys and receipts cannot be used in sandbox.
- Sandbox fraud-metric requests use the development App Attest data endpoint.
- Production fraud-metric requests use the production App Attest data endpoint.

Keep the server's environment records explicit so a sandbox attestation cannot be accepted as production or vice versa.

## macOS Notes

Do not assume iOS verification rules are enough for macOS.

Apple documents macOS-specific App Attest validation details, including use of the signing identifier in the RP ID and verification of the key access-policy hash. A server implementation that supports macOS should have explicit tests and docs for those checks.

Developer ID, App Store, TestFlight, Enterprise, ad hoc, and development signatures may appear differently in validation category checks. Treat validation-category policy as a server risk decision and keep it documented.

## Extensions and App Clips

- App Clips should share the key identifier with the corresponding full app when using the same App Attest key pair.
- Action, extensible SSO, and watchOS extensions are documented as supported for App Attest.
- Other extension types are not supported even if `isSupported` returns true.
- Extension support should be verified in the current Apple docs before implementation.

## Rollout Planning

For large existing apps, do not enable App Attest attestation for every user at once. Apple documents gradual onboarding guidance because `attestKey` contacts Apple servers and can encounter rate limits.

Rollout plans should include:

- feature flag or server-side cohorting
- retry behavior for Apple server unavailability
- rollback or pullback controls
- unsupported-device fallback policy
- observability for attestation and assertion failure reasons
- separation of sandbox, TestFlight, App Store, Enterprise, and Developer ID metrics

## Validation Paths

Use the smallest honest validation:

- static review for skill guidance and docs-only changes
- Xcode build for entitlement and framework import changes
- app run or device/simulator validation when availability, lifecycle, or extension behavior matters
- server unit tests for challenge expiry, replay rejection, counter updates, environment separation, and policy mapping
- integration tests against Apple development endpoints only when credentials and explicit approval are available

Report manual-validation gaps plainly when Apple Developer account access, server credentials, physical device evidence, or production rollout approval is unavailable.
