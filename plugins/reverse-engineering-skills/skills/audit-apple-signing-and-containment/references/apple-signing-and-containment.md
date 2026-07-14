# Apple Signing And Containment Reference

## Separate These Layers

- Code signature: integrity and designated identity over code and sealed resources.
- Provisioning profile: development or distribution authorization and a capability envelope for applicable platforms.
- Signed entitlements: claims embedded in the executable signature.
- Notarization: Apple service assessment and ticket/stapling context; not equivalent to App Store review or runtime permission.
- Hardened runtime and library validation: process restrictions influenced by signing and entitlements.
- App Sandbox: process containment profile and extension model.
- SIP and platform policy: system-wide mandatory protections.
- TCC, Data Vaults, and service authorization: access decisions not proven by a signed entitlement alone.

## Narrow Inspection Commands

```bash
codesign -dvvv --entitlements :- <bundle-or-binary>
codesign --verify --deep --strict --verbose=4 <bundle>
codesign -dr - <bundle-or-binary>
security cms -D -i <embedded.mobileprovision>
spctl --assess --type execute --verbose=4 <bundle>
```

Avoid `--deep` when signing. During verification, record that recursive verification can summarize nested failures without replacing a deliberate nested-code inventory.

## Comparison Questions

- Does the executable hash and UUID match the preserved artifact?
- Is the signature original, ad hoc, development, distribution, or transformed?
- Do the profile application identifier and Team ID align with the signed entitlements?
- Are debugger or development entitlements present?
- Are nested frameworks, helpers, and extensions consistently signed?
- Is a runtime result actually constrained by user consent, service mediation, SIP, TCC, sandbox extensions, or a different process?

## Authoritative Sources

- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)
- [Code signing process in macOS](https://support.apple.com/guide/security/sec3ad8e6e53/web)
- [Code signing process in iOS and iPadOS](https://support.apple.com/guide/security/sec7c917bf14/web)
- [App security in iOS and iPadOS](https://support.apple.com/guide/security/sec15bfe098e/web)
- [System Integrity Protection](https://support.apple.com/guide/security/secb7ea06b49/web)
- [Apple Security source distribution](https://github.com/apple-oss-distributions/Security)

Treat Platform Security as architecture guidance and confirm build-specific behavior through current release documentation and reproducible runtime evidence.
