# macOS Platform Security Skills Plan

## Intent

Expand Socket's macOS security guidance so an agent can diagnose, implement,
research, and explain the platform controls that commonly get flattened into
one vague permission problem:

- Transparency, Consent, and Control (TCC) privacy decisions
- Accessibility, Automation, Developer Tools, screen capture, input, media,
  personal-data, and filesystem permission classes
- App Sandbox containers, user-selected files, security-scoped bookmarks, App
  Groups, and other supported file-access paths
- capabilities, source entitlements, provisioning authorization, signed
  entitlements, restricted entitlements, and runtime consent
- quarantine, Gatekeeper, notarization, XProtect, Execution Policy, Hardened
  Runtime, System Integrity Protection (SIP), signed system volume protections,
  Data Vaults, and related mandatory access controls
- exact-build technical notes for public APIs, private symbols, runtime evidence,
  and changes between macOS releases

The practical result should be an agent that identifies the real controlling
layer and responsible executable before suggesting a permission change. It
should be able to explain why granting Terminal does not necessarily authorize
Codex, Xcode, a helper, an XPC service, or the built application; why an
entitlement is not user consent; and why a bookmark, Full Disk Access,
Gatekeeper assessment, XProtect detection, App Sandbox denial, and SIP denial
are different facts.

This is a coordinated expansion of existing Socket plugins. It does not create
a new catch-all macOS security plugin, modify the live TCC database, bundle a
privileged helper, install endpoint tooling, or automate changes to system
protections.

## Source Baseline

This plan was checked on 2026-07-19 against current local and Apple-owned
sources. Implementation must repeat the docs check because permission classes,
framework APIs, System Settings wording, and Endpoint Security events are
version-sensitive.

- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)
  separates system integrity, application trust, malware protection, user-data
  controls, and encryption rather than presenting one universal permission
  system.
- [Controlling app access to files in macOS](https://support.apple.com/guide/security/secddd1d86a6/web)
  documents user consent for protected locations, Full Disk Access,
  Accessibility, and Automation.
- [Privacy Preferences Policy Control](https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web)
  documents the managed-device PPPC payload, supported service classes,
  designated-requirement identity, and TCC attribution logging.
- [Protecting user data with App Sandbox](https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox)
  and [Accessing files from the macOS App Sandbox](https://developer.apple.com/documentation/security/accessing-files-from-the-macos-app-sandbox)
  document containers, user-selected access, bookmarks, and the limits imposed
  by other discretionary and mandatory access controls.
- [Entitlements](https://developer.apple.com/documentation/bundleresources/entitlements)
  and [Diagnosing Issues with Entitlements](https://developer.apple.com/documentation/bundleresources/diagnosing-issues-with-entitlements)
  establish that source configuration, provisioning authorization, final
  signed entitlements, and runtime behavior require separate evidence.
- [Configuring the Hardened Runtime](https://developer.apple.com/documentation/xcode/configuring-the-hardened-runtime/)
  documents runtime hardening and narrowly scoped exception entitlements.
- [Gatekeeper and runtime protection in macOS](https://support.apple.com/guide/security/sec5599b66df/web)
  documents download provenance, signing, notarization, first-open approval,
  assessment, and randomized read-only launch behavior.
- [Protecting against malware in macOS](https://support.apple.com/guide/security/sec469d47bd8/web)
  distinguishes prevention, execution blocking, and remediation and documents
  Gatekeeper-bypass and XProtect Endpoint Security events on supported macOS
  releases.
- [System Integrity Protection](https://support.apple.com/guide/security/secb7ea06b49/web)
  documents SIP as a system-wide mandatory policy that is distinct from App
  Sandbox, TCC, and administrative privileges.

Local planning evidence on macOS 26.5.2 build 25F84 with the selected stable
Xcode SDK includes:

- public `EPDeveloperTool.authorizationStatus` and `requestAccess()` in the
  Execution Policy framework for the Developer Tools privacy class
- public `AXIsProcessTrustedWithOptions` for Accessibility trust
- public `AEDeterminePermissionToAutomateTarget` for Apple Events automation
- public `CGPreflightScreenCaptureAccess` and `CGRequestScreenCaptureAccess`
  for screen capture
- framework-specific authorization APIs for camera, microphone, Contacts,
  EventKit, Photos, location, and other protected data
- `tccutil` supporting reset, not a general supported grant or status API
- `syspolicy_check distribution` combining Gatekeeper, XProtect,
  provisioning-profile, and related distribution checks
- `spctl` retaining assessment operations while macOS 15 and later deprecate
  rule-database and global-state mutation operations in favor of supported
  management policy

These observations are a planning baseline, not portable truth. Each workflow
must discover the current OS build, SDK, responsible process, public API, and
tool behavior before making a version-sensitive claim.

## Architecture Decision

Extend `apple-dev-skills`, `reverse-engineering-skills`, and the existing macOS
workflows in `cybersecurity-skills` through explicit handoffs. Do not create a
fourth plugin that claims ownership of all macOS privacy and security systems.

This is a durable building-block change. It unlocks these near-term uses:

- diagnose why an app, command-line tool, agent host, helper, or XPC service is
  missing Accessibility, Automation, Developer Tools, screen-capture, input,
  personal-data, or filesystem access
- implement the documented preflight, request, explanation, denial, settings,
  and retry lifecycle for permission classes that expose public APIs
- persist user-selected file access correctly across relaunches without
  treating bookmarks as blanket storage permission
- trace an entitlement from desired capability through Xcode, the developer
  account and profile, the signed executable, nested code, and observed runtime
  authorization
- distinguish a developer configuration failure from a suspicious-host or
  malware investigation
- create reproducible technical notes about public and private macOS security
  controls without turning private symbols into supported application APIs
- compare behavior across clean macOS guests while keeping SIP-, recoveryOS-,
  hardware-, and physical-Mac-only proof requirements explicit

The simpler extension path was one `macos-security-workflow` skill or a new
`macos-security-skills` plugin. That would mix application implementation,
managed-device policy, malware investigation, binary inspection, private
framework research, and boot-level integrity controls. It would duplicate the
current plugins' legitimate ownership and make triggering less precise. The
focused skills below share an evidence vocabulary while retaining their own
entry conditions and outputs.

No new runtime abstraction is approved in the first implementation. A shared
read-only diagnostic collector may be reconsidered only after repeated manual
captures prove a stable command and output contract that materially reduces
duplication.

## Ownership And Handoffs

| Surface | Primary owner | Responsibility |
| --- | --- | --- |
| App-facing privacy permission diagnosis and implementation | `apple-dev-skills:macos-privacy-permissions-workflow` | Classify the permission, responsible executable, public preflight/request API, usage description, prompt or settings path, reset boundary, and runtime validation. |
| Sandboxed filesystem design and persistent user-selected access | `apple-dev-skills:macos-sandbox-file-access-workflow` | Own containers, open/save panels, bookmarks, standard locations, App Groups, access lifetime, stale resolution, and non-TCC filesystem controls. |
| Capability and entitlement diagnosis | `apple-dev-skills:diagnose-apple-entitlements` | Trace requested capability, tracked project source, account/profile authorization, signed entitlements, nested-code identity, and runtime policy or consent. |
| Account-side bundle IDs, capabilities, certificates, profiles, and CloudKit | `apple-dev-skills:apple-developer-provisioning-workflow` | Retain supported provisioning discovery and mutations after entitlement diagnosis identifies an account-side mismatch. |
| Exported artifacts, Hardened Runtime, Gatekeeper, notarization, and stapling | `apple-dev-skills:macos-distribution-workflow` | Retain distribution-artifact readiness and launch-failure classification. |
| Xcode target, capability, signing, build, install, and run work | Existing Xcode workflows | Apply and validate project changes after a permission or entitlement workflow identifies the owning target and required source change. |
| Exact-build public/private control research | `reverse-engineering-skills:research-macos-security-control` | Own private `kTCCService*` symbols, private entitlements, binaries, frameworks, services, policy implementation, exact-build comparison, and reproducible technical notes. |
| Signed artifact containment inspection | `reverse-engineering-skills:audit-apple-signing-and-containment` | Retain artifact identity, signature, provisioning, entitlement, sandbox, Hardened Runtime, SIP, Data Vault, and declared-versus-observed access evidence. |
| Suspicious prompts, Gatekeeper/XProtect alerts, host activity, hardening, containment, or recovery | Existing `cybersecurity-skills` macOS workflows | Retain threat assessment and defensive decisions; hand ordinary app implementation and deep binary research to their specialist owners. |
| Clean macOS guest selection and preparation | Existing Apple Dev virtualization workflows | Provide an isolated, resettable environment for prompt, identity, signing, quarantine, Gatekeeper, XProtect, and SIP-sensitive validation. |
| Managed-device PPPC policy | Apple deployment documentation plus the owning MDM | Explain payload and identity requirements without pretending a normal app or local CLI can self-grant managed policy. |

## Control-Layer Model

Every workflow must name the controlling layer before suggesting a fix:

1. **Process and code identity**: executable path, bundle identifier,
   designated requirement, Team ID, code-signing state, parent/launcher,
   helper or XPC boundary, and whether the artifact changed between runs.
2. **Discretionary filesystem access**: ownership, POSIX mode, ACLs, path
   resolution, mount state, and ordinary file-operation semantics.
3. **App Sandbox**: app container, App Groups, static sandbox entitlements,
   user-selected extensions, security-scoped bookmarks, inherited helpers, and
   extension process boundaries.
4. **TCC and privacy consent**: protected service class, responsible code,
   prompt or settings behavior, public status/request API, usage description,
   user decision, and managed policy.
5. **Capabilities and entitlements**: requested app service, account-side
   authorization, provisioning profile, final code-signature entitlements,
   restricted/private entitlement status, and runtime enforcement.
6. **Execution and distribution policy**: quarantine/provenance, code signing,
   notarization, Gatekeeper, Execution Policy, Hardened Runtime, library
   validation, nested code, and stapling.
7. **Malware protection**: XProtect detection and remediation evidence,
   security-data versions, Endpoint Security events, and observed behavior.
8. **System integrity and mandatory controls**: SIP, signed system volume,
   Data Vaults, platform-binary policy, system extensions, boot security,
   recoveryOS decisions, and hardware-dependent protections.

An administrator account or root access does not collapse these layers. A
successful operation proves only that the recorded artifact performed that
operation in the recorded environment; it does not prove that every layer was
configured as expected.

## Shared macOS Security Evidence Record

Each new skill should produce or consume a compact common record while keeping
its own domain-specific result:

- question and requested decision
- host hardware, architecture, exact macOS version and build, selected SDK and
  Xcode, device-management state, and relevant security-update state
- application, executable, helper, service, or artifact identity, including
  path, bundle ID, Team ID, designated requirement, signing state, hashes or
  UUIDs when useful, parent/launcher, and transformations
- operation attempted, target resource or process, timestamp, user/session,
  and whether the observation came from a host, guest, or physical Mac
- controlling layer and permission/service class
- declared project capability, source entitlement, profile authorization,
  signed entitlement, usage-description, sandbox, and Hardened Runtime state
  when relevant
- public status/preflight API result, request action, user or managed decision,
  settings state, restart/relaunch requirement, and reset history
- exact error domain, code, message, log subsystem/category, command, and tool
  version rather than a generic `permission denied` summary
- observations, documentation, private implementation evidence, hypotheses,
  conclusions, confidence, disproven explanations, and unresolved questions
  kept distinct
- mutations performed, approvals received, rollback or reset path, validation
  result, and remaining fidelity gaps

Use this as a consistent handoff shape, not a serialized framework, shared
manager, service, or new repository layer.

## Skill 1: `macos-privacy-permissions-workflow`

### Owned job

Diagnose and implement macOS application-facing privacy and Developer Tools
permission behavior. Start from the attempted operation and responsible
executable, then select the documented framework-specific authorization path.

### Required coverage

- Accessibility
- Automation and Apple Events, including the controlling/target application
  pair
- Developer Tools through Execution Policy
- Screen and System Audio Recording
- Input Monitoring
- Camera and microphone
- Contacts, calendars, reminders, Photos, media library, location, Bluetooth,
  local network, and other framework-owned protected data
- Files & Folders and Full Disk Access boundaries
- App Management and other current macOS-only Privacy & Security classes
- MDM PPPC policy versus ordinary local user consent

For each class, maintain a version-checked matrix containing:

- user-visible System Settings name and internal service terminology only when
  needed for logs, resets, or research
- public framework and status, preflight, or request API
- required usage-description key
- required entitlement or capability, if any
- whether the app can trigger a prompt, can only create a Settings entry, must
  direct the person to Settings, or has no public self-service request path
- whether relaunch, helper restart, logout, or another lifecycle transition is
  required after a change
- responsible-code attribution behavior and helper/XPC/launcher implications
- supported `tccutil reset` boundary and a warning that reset is not grant
- MDM support and whether allow, deny, or user approval remains the documented
  management result
- minimum host, guest, or physical-device validation fixture

### Workflow contract

1. Record the operation and target before naming a permission.
2. Resolve the responsible process and stable signing identity.
3. Consult current Apple docs and the local SDK for the permission class.
4. Inspect usage descriptions, entitlements, sandbox state, helper identity,
   and signed result without treating any one as consent.
5. Preflight with the documented public API when available.
6. Request only in direct context of the user action that requires access.
7. Explain why access is needed, what will appear, how denial behaves, and how
   to change the decision later.
8. Treat Full Disk Access and other settings-managed classes as explicit user
   or MDM decisions; do not invent a grant API.
9. Reproduce the exact operation after the required lifecycle transition.
10. Report the responsible executable, permission class, evidence, result, and
    remaining uncertainty.

### Guards

- Do not edit, replace, copy back, or directly query the live TCC database as
  an application workflow.
- Do not use private `TCC.framework` APIs or `kTCCService*` constants in
  shipping guidance; hand private implementation research to Reverse
  Engineering.
- Do not describe `tccutil` as a grant or general status tool.
- Do not repeatedly prompt, reset a denial without an explicit test reason, or
  automate System Settings clicks to defeat user choice.
- Do not grant a broad terminal, agent host, or IDE permission when a narrower
  signed application or helper is the responsible code without explaining the
  resulting authority difference.
- Do not run permission-prompt fixtures on Gale's active Mac without explicit
  approval immediately before the visible action.

## Skill 2: `macos-sandbox-file-access-workflow`

### Owned job

Choose and implement the narrowest documented filesystem access path for a
macOS app or helper while preserving access lifetime, identity, privacy, and
failure evidence.

### Required coverage

- app containers and standard container-relative directories
- App Groups and shared-container identity
- user-selected read-only, read-write, and executable access
- open/save panels, drag and drop, document URLs, and implicit sandbox
  extensions
- application-scoped and document-scoped security-scoped bookmarks
- bookmark creation, storage, resolution, stale detection and recreation,
  read-only scope, balanced start/stop access, and relaunch behavior
- child resources selected through a directory and documented exceptions
- helper, XPC service, app extension, and inherited-sandbox boundaries
- Downloads and media-folder entitlements where current documentation supports
  them
- Full Disk Access and Files & Folders as separate TCC controls
- POSIX permissions, ACLs, symlinks, mounts, file coordination, volumes,
  Data Vaults, SIP, and other controls that can still deny access
- explicit handoffs to File Provider/Finder Sync when remote storage or Finder
  UI is the actual requirement

### Workflow contract

1. Identify the data owner, operation, persistence need, process boundary, and
   distribution channel.
2. Use the container or a standard supported directory when that satisfies the
   feature.
3. Prefer direct user selection for external files and directories.
4. Create a security-scoped bookmark only when access must survive the current
   interaction or process lifetime.
5. Resolve stored bookmark data, detect staleness, recreate stale data, start
   access, perform the narrow operation, and balance successful starts with
   stops.
6. Record the exact layer producing any remaining denial.
7. Validate relaunch, moved/renamed resources, read-only behavior, helper or
   extension access, revoked access, and corrupted bookmark recovery.

### Guards

- Do not treat paths as durable authorization tokens or remote identifiers.
- Do not store a security-scoped URL without its bookmark lifecycle.
- Do not retain access indefinitely for convenience.
- Do not claim a bookmark bypasses TCC, Full Disk Access, Data Vaults, SIP,
  POSIX permissions, ACLs, or another mandatory control.
- Do not use Finder Sync as a file synchronization or access-grant system.
- Do not log sensitive file paths or bookmark payloads without a specific,
  privacy-reviewed diagnostic need.

## Skill 3: `diagnose-apple-entitlements`

### Owned job

Diagnose why an Apple capability or entitlement is missing, rejected,
ineffective, or different between targets and build stages. Determine which
owner must change before handing implementation to Xcode, provisioning,
distribution, or Reverse Engineering.

### Five-state comparison

1. **Desired behavior**: operation, target, platform, OS version, distribution
   channel, and the current Apple documentation that requires or permits it.
2. **Tracked source**: Xcode capability, `.entitlements` file, `Info.plist`
   usage description, build settings, target membership, extension/helper
   configuration, and generated-project source of truth.
3. **Account authorization**: App ID capability, restricted-entitlement
   approval, provisioning profile, certificate/team, environment, device, and
   portal-only or API-supported state.
4. **Signed result**: main executable and every nested helper, extension,
   framework, daemon, XPC service, command-line tool, and profile embedded in
   the actual built or exported artifact.
5. **Runtime result**: sandbox, Hardened Runtime, library validation, TCC/user
   consent, service-mediated authorization, SIP/Data Vault/platform policy,
   exact error, and observed access.

### Required distinctions

- capability versus entitlement versus usage description
- public, restricted, private/undocumented, development-only, environment, and
  exception entitlements
- source entitlement versus profile entitlement versus final signed
  entitlement
- application target versus extension/helper/XPC/daemon target
- Debug versus Release, development versus distribution signing, and original
  versus re-signed artifact
- declarative capability versus user consent or runtime service authorization
- App Sandbox exception versus Hardened Runtime exception
- local build success versus exported artifact or customer-machine behavior

### Guards

- Do not invent entitlement keys, values, availability, approval status, or
  profile support.
- Do not hand-edit generated project or profile artifacts to hide a source
  mismatch.
- Do not casually re-sign an artifact; treat every transformed copy as a new
  artifact and invalidate assumptions about its prior notarization or behavior.
- Do not recommend a private entitlement for an ordinary third-party product.
  Hand research questions to Reverse Engineering and account questions to the
  provisioning workflow.
- Do not call an entitlement effective until the final executable and runtime
  behavior have been checked at the required evidence level.

## Skill 4: `research-macos-security-control`

### Owned job

Research one macOS security or privacy control on an exact build and produce a
reproducible technical note that distinguishes supported public contracts,
private implementation evidence, runtime observations, and hypotheses.

### Research surfaces

- TCC frameworks, services, databases, attribution chains, private
  `kTCCService*` constants, and changes in service vocabulary
- sandbox profiles, containers, extensions, Seatbelt behavior, and mandatory
  access controls
- public and private entitlements, platform-binary context, restricted
  entitlements, provisioning, and code requirements
- Execution Policy, quarantine, provenance, Gatekeeper, assessment, XProtect,
  notarization, and system-policy services
- Hardened Runtime, library validation, task/debugging policy, SIP, signed
  system volume, Data Vaults, system extensions, and boot/recovery policy
- exact-build framework, daemon, XPC, unified-log, Endpoint Security, dyld,
  Mach-O, symbol, string, and behavioral differences

### Workflow contract

1. State the narrow research question and expected decision.
2. Record host or guest build, hardware, security state, artifact identity,
   source provenance, and transformation history.
3. Search Apple docs and public SDK declarations before private implementation.
4. Inspect exact-build binaries, frameworks, services, signatures,
   entitlements, strings, symbols, and logs without changing the original.
5. Form a minimal falsifiable hypothesis and choose the least invasive runtime
   probe able to test it.
6. Use a clean macOS guest or physical Mac when host state, SIP, recoveryOS,
   hardware, or customer fidelity matters.
7. Preserve observations separately from inference; compare exact builds when
   claiming change over time.
8. Produce the technical note and hand ordinary application implementation,
   distribution repair, threat response, or formal security reporting to the
   existing owner.

### Guards

- Do not present private symbols, database schemas, log strings, or observed
  implementation behavior as a stable supported API.
- Do not mutate live TCC or system-policy databases merely to make research
  convenient.
- Do not disable SIP, boot protections, Gatekeeper, XProtect, or other system
  protections without a separate exact research goal, recorded state, minimum
  necessary change, and explicit approval.
- Do not infer one macOS build's private behavior on another build without
  comparison evidence.
- Preserve original artifacts and record every re-sign, patch, extraction, or
  environment change.

## Existing Cybersecurity Workflow Alignment

Do not add another broad Cybersecurity skill. Update the existing macOS
workflows so their handoffs are unambiguous:

- `assess-macos-threat` retains suspicious prompts, applications, packages,
  profiles, extensions, Gatekeeper or XProtect alerts, unexpected access, and
  observed host behavior. It hands ordinary permission implementation to
  `macos-privacy-permissions-workflow` and exact private-control questions to
  `research-macos-security-control`.
- `inspect-macos-runtime-activity` retains process, file, network, privacy,
  unified-log, Endpoint Security, and `eslogger` correlation. It records the
  exact permissions needed to collect evidence and does not interpret lack of
  telemetry as lack of behavior.
- `harden-macos` retains supported user and managed defensive posture without
  teaching developers how to request app permissions.
- `contain-and-recover-macos` retains defensive removal, recovery, and
  verification and does not reset or weaken privacy/security controls merely
  to make a suspicious artifact run.
- `select-analysis-isolation` and `prepare-isolated-analysis-lab` retain the
  SIP-enabled macOS guest as the stable high-fidelity path for control-sensitive
  work, with local failure injection explicitly lower fidelity.

## Resource Topology

Keep every `SKILL.md` procedural and below 500 lines. Put version-sensitive
matrices and detailed evidence in one-level-deep references loaded only when
the task needs them.

Planned Apple Dev surface:

```text
plugins/apple-dev-skills/skills/
├── macos-privacy-permissions-workflow/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── permission-class-matrix.md
│       ├── responsible-code-and-attribution.md
│       ├── prompting-settings-reset-and-mdm.md
│       └── validation-fixtures.md
├── macos-sandbox-file-access-workflow/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── sandbox-and-filesystem-control-map.md
│       ├── security-scoped-bookmark-lifecycle.md
│       ├── helpers-groups-and-process-boundaries.md
│       └── validation-fixtures.md
└── diagnose-apple-entitlements/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── five-state-entitlement-comparison.md
        ├── restricted-and-private-entitlements.md
        ├── artifact-and-nested-code-inspection.md
        └── routing-and-validation.md
```

Planned Reverse Engineering surface:

```text
plugins/reverse-engineering-skills/skills/
└── research-macos-security-control/
    ├── SKILL.md
    ├── agents/openai.yaml
    └── references/
        ├── source-and-evidence-hierarchy.md
        ├── control-research-matrix.md
        ├── exact-build-probe-design.md
        └── technical-note-contract.md
```

Do not add a skill-local README, a duplicated Apple documentation corpus,
machine-local artifacts, copied TCC databases, private binaries, provisioning
profiles, signing identities, or live log captures.

## Script And Runtime Decision

The first implementation remains instruction-only. Use documented tools and
explicit commands inside workflows rather than introducing a collector before
the output contract is proven.

A later read-only diagnostic script is allowed for evaluation only if repeated
fixtures show the same evidence must be gathered across at least three skills.
Before adding it, state the concrete duplication it removes and prove that it:

- accepts explicit artifact, process, or bundle targets
- defaults to non-mutating inspection
- records `sw_vers`, tool versions, signing identity, entitlements, quarantine,
  sandbox, process ancestry, and requested logs without reading secrets or
  dumping broad private data
- never grants or resets TCC, changes Gatekeeper, disables protections, edits
  databases, re-signs artifacts, or opens System Settings
- emits a documented machine-readable record plus human-friendly diagnostics
- is useful outside Gale's machine and contains no local paths

An MCP server, privileged helper, daemon, background monitor, endpoint agent,
or GUI permission manager is an architectural pivot and requires a separate
proposal and explicit approval.

## Implementation Slices

### Slice 1: Public Privacy Permission Foundation

- Scaffold `macos-privacy-permissions-workflow` with the skill creator.
- Build the permission-class matrix from current Apple docs and the selected
  SDK, starting with Accessibility, Automation, Developer Tools, screen
  capture, input, camera/microphone, Files & Folders, and Full Disk Access.
- Add responsible-code attribution, helper/XPC, prompt/settings, denial,
  relaunch, reset, and PPPC boundaries.
- Add focused tests for trigger text, public API names, usage-description
  ownership, `tccutil` reset-only wording, no-private-API guards, and handoffs.
- Forward-test direct app, Terminal-launched CLI, Xcode-launched app, agent host,
  helper, and XPC scenarios without touching the live host's decisions.

Slice 1 exit criteria: an agent identifies the right permission class and
responsible executable, uses a current supported request path when one exists,
and refuses to invent a grant API when it does not.

### Slice 2: Filesystem Access And Entitlement Diagnosis

- Scaffold `macos-sandbox-file-access-workflow` and
  `diagnose-apple-entitlements`.
- Add bookmark lifecycle, container, App Group, helper, TCC, POSIX/ACL, Data
  Vault, SIP, profile, nested-code, Hardened Runtime, and runtime-consent
  references.
- Align `apple-developer-provisioning-workflow`,
  `macos-distribution-workflow`, app-extension guidance, File Provider/Finder
  Sync, Xcode project guidance, and shared Xcode snippets with the new owners.
- Add focused tests for stale bookmark recovery, balanced access, read-only
  scope, relaunch, five-state entitlement comparison, nested helpers, Debug
  versus distribution, private-entitlement handoff, and no legacy shim paths.

Slice 2 exit criteria: an agent can choose persistent file access correctly
and localize an entitlement failure to project source, account/profile, signed
artifact, nested code, or runtime policy without conflating those stages.

### Slice 3: Exact-Build Security-Control Research

- Scaffold `research-macos-security-control` under Reverse Engineering Skills.
- Connect it to artifact inspection, signing/containment audit, dynamic
  analysis, exact-build comparison, evidence notes, and Apple security report
  workflows.
- Add public/private source hierarchy, exact-build probe, technical-note, and
  mutation-record references.
- Align Cybersecurity handoffs for suspicious-host and XProtect/Gatekeeper
  cases without moving defensive ownership.
- Add tests that reject unsupported API claims, unrecorded cross-build
  generalization, casual protection disabling, and transformed-artifact
  confusion.

Slice 3 exit criteria: an agent can research a private or poorly documented
control reproducibly while preserving the line between public contract,
private implementation, runtime observation, and inference.

### Slice 4: Integration, Compatibility, And Forward Testing

- Run scenario-level forward tests in fresh contexts using raw fixtures and no
  leaked expected answers.
- Update Apple Dev, Reverse Engineering, and Cybersecurity plugin descriptions,
  default prompts, keyword inventories, active skill inventories, and root
  README text only when the skill surface actually ships.
- Export portable instruction-only skills through the Hermes tap and update
  grouping/index entries in the same pass.
- Record Claude Code and Cowork compatibility, keeping Codex-specific MCP or
  app metadata out of portable claims.
- Run affected child validation, root metadata validation, Hermes parity,
  Claude/Cowork checks, architecture consistency, and the full relevant tests.
- Review whether repeated use earned a shared read-only collector or standalone
  plugin. Default to no if the evidence remains workflow-specific.

Slice 4 exit criteria: every shipped workflow triggers distinctly, hands off
without loops, survives independent scenario testing, and appears consistently
across supported host inventories.

## Validation Fixtures

Use locally generated, redistributable, or explicitly approved fixtures. Keep
permission decisions and signing identity stable enough to distinguish a code
change from an identity change.

1. A minimal signed macOS application with configurable usage descriptions and
   one protected operation per test mode.
2. A signed controlling app and target app for Automation/Apple Events.
3. Accessibility and screen-capture preflight/request modes that can run in a
   disposable macOS guest.
4. An `EPDeveloperTool` fixture that distinguishes not determined, restricted,
   denied, and authorized without claiming that `requestAccess()` shows UI.
5. The same tool reached directly, from Terminal, from Xcode, from an agent
   host, and through a helper or XPC service to test responsible-code identity.
6. A sandboxed open-panel fixture that persists a read-only or read-write
   security-scoped bookmark, relaunches, balances access, and repairs stale
   data.
7. Moved, renamed, removed, revoked, malformed, and inaccessible bookmark
   resources with exact error reporting.
8. A generated app/helper/extension bundle matrix with source, profile, and
   signed entitlement matches and mismatches.
9. Debug, Release, Developer ID, ad hoc, and intentionally re-signed fixture
   copies treated as separate artifacts.
10. Benign quarantined and non-quarantined artifacts for `syspolicy_check`,
    `spctl`, signing, notarization, and Gatekeeper classification without
    bypassing policy.
11. A clean SIP-enabled macOS guest plus a lower-fidelity local failure-injection
    fixture to prove the reporting distinction.
12. Exact-build technical notes comparing one public API, one private symbol or
    service string, and one runtime observation across two approved macOS
    builds without assuming the difference is causal.

Automated tests should validate guidance contracts and static fixture
artifacts. Visible prompts, System Settings changes, logout/restart behavior,
and protection-state changes require a separate manual or Computer Use session
with explicit approval and a disposable guest whenever practical.

## Forward-Test Prompts

Use fresh worker contexts during implementation. Pass only the completed skill
and raw fixture/request, not this plan's intended diagnosis.

- "My macOS app says Accessibility is enabled, but its helper still cannot
  inspect another app. Diagnose it."
- "Codex can build my tool, but the tool cannot run unsigned development
  binaries. Help me handle Developer Tools access correctly."
- "My app controls Finder with Apple Events, but granting Terminal Automation
  did not fix the built app."
- "Persist this user-selected directory across app relaunches without asking
  for Full Disk Access."
- "The entitlement is present in the `.entitlements` file, but the exported
  helper still gets an authorization failure."
- "Determine whether this denial is App Sandbox, TCC, POSIX, Data Vault, or SIP
  without weakening my Mac."
- "Explain whether this XProtect event means malware executed and whether the
  developer should change the app or the operator should investigate the
  host."
- "Research this `kTCCService` symbol on two macOS builds and write a technical
  note without treating it as public API."

Success requires the agent to choose an owner, gather identity and exact-build
evidence, avoid unsupported grants or bypasses, and state what remains
unproven.

## Documentation And Compatibility

- Add this plan to root `ROADMAP.md` and the Apple Dev child roadmap in the
  planning slice. Do not change README inventory, manifests, marketplace
  entries, default prompts, or exported skill inventories until implementation
  adds a user-visible skill.
- Keep `SKILL.md` frontmatter descriptions concrete enough to distinguish
  permission implementation, filesystem access, entitlement diagnosis, and
  private control research.
- Generate `agents/openai.yaml` deterministically from each final skill.
- Keep detailed matrices in directly linked references and recheck their dated
  claims against local Apple docs, current SDK headers, Apple Platform
  Security, Apple deployment docs, and official web documentation.
- Update the Hermes tap for every portable skill in the same implementation
  slice. Do not present Codex plugin metadata as a Hermes plugin.
- Record whether each skill is instruction-portable to Claude Code and Cowork;
  preserve host-specific tool and Computer Use requirements as explicit
  adapters.
- Do not add an MCP translation unless a later separately approved `.mcp.json`
  surface exists.

## Validation Commands

Run commands strictly serially and from the owning repository root.

Planning slice:

```bash
bash plugins/apple-dev-skills/.github/scripts/validate_repo_docs.sh
uv run scripts/validate_socket_metadata.py
```

Implementation slices add, as applicable:

```bash
cd plugins/apple-dev-skills && uv run pytest
cd plugins/reverse-engineering-skills && uv run scripts/validate_repo_metadata.py
cd plugins/cybersecurity-skills && uv run scripts/validate_repo_metadata.py
uv run scripts/validate_socket_metadata.py
```

Also run the repository's current Hermes, Claude/Cowork, architecture, and
release-ready validation gates before a publish or release request. Preserve
full-suite execution for the final integrated slice while using targeted tests
between coherent commits.

## Branch And Commit Plan

Use one implementation branch-backed worktree unless a slice must be isolated
for review. Keep Git operations serial and push each coherent checkpoint.

1. `docs: plan macOS platform security skills`
   - this maintainer plan
   - root and Apple Dev roadmap entries
2. `apple: add macOS privacy permission workflow`
   - Slice 1 skill, references, metadata, tests, and handoffs
3. `apple: add sandbox file and entitlement workflows`
   - Slice 2 skills, references, tests, and existing-owner alignment
4. `forensics: add macOS security control research`
   - Slice 3 Reverse Engineering skill, references, tests, and Cybersecurity
     handoffs
5. `plugin: align macOS security discovery surfaces`
   - Slice 4 metadata, inventories, portability exports, docs, integrated tests,
     and forward-test remediation

Do not start version bump, PR, merge, tag, release, marketplace upgrade, or
branch cleanup work unless Gale asks for that lifecycle step.

## Standalone Plugin Reconsideration Gate

Reconsider `macos-security-skills` only after the implementation and real use
show all of the following:

- at least three workflows are routinely needed without Apple Dev, Reverse
  Engineering, or Cybersecurity owning the surrounding task
- users experience installation or triggering friction from the split that
  explicit handoffs and marketplace catalog installation cannot solve
- a common evidence/runtime surface has a stable, reviewed contract and is not
  merely duplicated prose
- moving the skills would reduce ownership ambiguity rather than introduce a
  fourth copy of signing, TCC, Gatekeeper, XProtect, or host-response guidance
- Codex, Hermes, Claude, and other supported-host packaging implications are
  designed explicitly

If those conditions are not met, keep the skills in their current specialist
plugins. Socket already gives users one catalog from which to install the
owners together.

## Planning Slice Boundary

This planning slice changes only this maintainer plan, root `ROADMAP.md`, and
the Apple Dev child roadmap. It does not add skills, tests, scripts, fixtures,
plugin manifests, marketplace metadata, README inventory text, portability
exports, version bumps, or runtime behavior.

Implementation is ready to begin when this plan is reviewed and the planning
branch is preserved. Slice 1 is the required starting point because responsible
code identity and public permission APIs establish the evidence vocabulary
that the file-access, entitlement, research, and cybersecurity handoffs consume.
