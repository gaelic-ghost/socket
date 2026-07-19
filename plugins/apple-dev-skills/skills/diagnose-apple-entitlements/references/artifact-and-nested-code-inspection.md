# Artifact And Nested-Code Inspection

## Preserve identity

Hash or otherwise identify the exact app/package, record its source/export configuration and transformations, and inspect without re-signing. Treat Debug, Release, archive, export, copied, patched, and re-signed variants as different artifacts.

## Inspect every responsible executable

Enumerate the main executable, app extensions, XPC services, login/background helpers, privileged helpers, command-line tools/daemons, frameworks with executable code, and embedded provisioning profiles. Record bundle ID, Team ID, designated requirement, signer/flags, and entitlements for each relevant target.

```bash
codesign --display --verbose=4 /path/to/App.app
codesign --display --entitlements :- /path/to/App.app
codesign --verify --deep --strict --verbose=2 /path/to/App.app
security cms -D -i /path/to/embedded.provisionprofile
```

Locate nested code explicitly and run the relevant inspection against each executable. `codesign --deep` verification is not a substitute for comparing nested entitlements and responsible-code identity.

## Compare

Compare source entitlements, profile entitlements, final signed entitlements, identifier/team/environment values, sandbox/Hardened Runtime state, and runtime process identity. Do not expose certificate/profile secrets in reports. Rebuild/export from corrected source; do not hand-edit an artifact and present the result as a project fix.
