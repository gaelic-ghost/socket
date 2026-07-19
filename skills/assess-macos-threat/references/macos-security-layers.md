# macOS Security Layers

Keep these meanings distinct:

- quarantine/provenance: records downloaded-content origin and first-open context;
- Gatekeeper: evaluates whether downloaded software may launch under current policy;
- notarization: Apple scanned a submitted artifact for known malicious content at submission time;
- XProtect: detects, blocks, and may remediate known or behaviorally suspicious malware;
- code signing: binds identity/integrity and declared entitlements, not benign intent;
- TCC: user/admin-mediated access to protected data and capabilities;
- App Sandbox and containers: constrain participating apps and protect app data;
- SIP and mandatory controls: protect system and data surfaces beyond ordinary root access;
- Endpoint Security: telemetry/control API whose evidence depends on client entitlement and permissions.

Route supported application-facing TCC prompting, status, responsible-code, and Settings behavior to `apple-dev-skills:macos-privacy-permissions-workflow`. Route private TCC constants/schemas, Gatekeeper/XProtect implementation internals, and exact-build policy comparisons to `reverse-engineering-skills:research-macos-security-control`.

An alert/event is evidence of the named control action, not automatically proof of prior execution, persistence, compromise, or complete remediation. Correlate process/file/network state and preserve telemetry coverage.

Use current [Apple Platform Security malware guidance](https://support.apple.com/guide/security/protecting-against-malware-sec469d47bd8/web). Record exact OS build because enforcement and available events change.
