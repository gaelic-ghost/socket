---
name: macos-privacy-permissions-workflow
description: Diagnose macOS privacy permissions from the operation and responsible executable. Use for Accessibility, Automation, Developer Tools, recording or input, protected data, Full Disk Access, PPPC, prompts, Settings, resets, and helpers.
---

# macOS Privacy Permissions Workflow

## Purpose

Identify the protected operation, responsible executable, and current public authorization contract before changing code or asking the person to change Privacy & Security settings. Keep project declarations, user consent, managed policy, and runtime success as separate evidence.

## When To Use

- Use for macOS privacy authorization failures, permission prompts, Settings entries, `tccutil reset`, PPPC policy, and responsible-code attribution.
- Use for Accessibility, Automation, Developer Tools, screen/system-audio recording, Input Monitoring, camera, microphone, personal data, Files and Folders, Full Disk Access, App Management, and other current macOS privacy classes.
- Do not use private TCC APIs or database details as an application implementation contract.

## Single-Path Workflow

1. Record the exact attempted operation, target resource or process, timestamp, user/session, error domain/code/message, and whether the evidence came from the host, a guest, or a physical Mac.
2. Resolve the responsible code: executable path, bundle identifier, Team ID, designated requirement, signing state, parent/launcher, helper or XPC boundary, and whether the artifact changed. Read `references/responsible-code-and-attribution.md`.
3. Apply the Apple docs gate through `explore-apple-swift-docs`. Record the host macOS version/build and selected SDK/Xcode, then verify the current framework API and settings name. Do not promote an internal service string to a public API.
4. Select the class in `references/permission-class-matrix.md`. Inspect the relevant usage description, entitlement/capability, sandbox state, helper identity, and final signed artifact without treating any declaration as consent.
5. Preflight or read status using the class's documented public API when one exists. Preserve `.notDetermined`, restricted or managed, denied, limited, and authorized states instead of collapsing them to Boolean access.
6. Request only from the user action that needs access and only when the public API supports requesting. Explain the operation, system UI, denial behavior, later Settings path, and any relaunch/helper restart/logout requirement.
7. For Settings-managed classes such as Full Disk Access, describe the user or MDM decision and the narrow responsible executable. Never invent a self-grant API or grant a broad terminal, IDE, or agent host without explaining its broader authority.
8. Read `references/prompting-settings-reset-and-mdm.md` before resetting or managing state. Treat `tccutil reset` as test-state removal, never grant or general status inspection.
9. Reproduce the original operation after the required lifecycle transition. Record the status/preflight result, actual operation result, responsible executable, mutations and approvals, reset/rollback path, and remaining uncertainty.
10. Use the minimum fixture in `references/validation-fixtures.md`. Obtain explicit approval immediately before any visible prompt, System Settings change, logout, or live-host permission mutation.

## Inputs

- attempted operation, target, exact error, and expected user-visible behavior
- app/tool/helper path, bundle identity, signer, launcher, and build transformation history
- macOS build, SDK/Xcode, management state, sandbox state, usage descriptions, and signed entitlements
- current status/preflight output, Settings state, prior prompts/resets, and reproduction environment

## Outputs

- responsible-code identity and controlling privacy class
- public status/request contract and required project declarations
- prompt, Settings, MDM, reset, lifecycle, and denial behavior
- reproduced operation result, exact evidence, confidence, and unresolved fidelity gaps

## Guards and Stop Conditions

- Do not edit, replace, copy back, or directly query a live TCC database as an app workflow.
- Do not use private `TCC.framework` APIs or `kTCCService*` constants in shipping guidance.
- Do not automate System Settings clicks to defeat user choice, repeatedly prompt, or reset a denial without an explicit test reason.
- Do not confuse a usage description, entitlement, sandbox exception, profile payload, or Settings entry with user consent.
- Stop before producing visible permission UI or mutating Gale's active Mac until Gale explicitly approves that exact action.
- Stop when the responsible executable or original protected operation cannot be identified; report the missing evidence instead of guessing a permission.

## Fallbacks and Handoffs

- Use `macos-sandbox-file-access-workflow` when user-selected file access, bookmarks, containers, or App Groups are the actual requirement.
- Use `diagnose-apple-entitlements` when source, profile, signed entitlement, and runtime state disagree.
- Use `apple-developer-provisioning-workflow` for account-side capability and profile changes; use Xcode workflows for project edits and builds.
- Use `research-macos-security-control` for private TCC symbols, database schemas, daemon behavior, or exact-build implementation research.
- Use Cybersecurity Skills for suspicious prompts, unexplained grants, Gatekeeper/XProtect alerts, or host compromise questions.

## Customization

Use `references/customization-flow.md`. The workflow has no runtime knobs; permission behavior must remain tied to the recorded identity, OS build, public API, and user or managed decision.

## References

- `references/permission-class-matrix.md`
- `references/responsible-code-and-attribution.md`
- `references/prompting-settings-reset-and-mdm.md`
- `references/validation-fixtures.md`
- Recommend `references/snippets/apple-xcode-project-core.md` when the diagnosis leads to an Xcode project change.
- [Controlling app access to files in macOS](https://support.apple.com/guide/security/secddd1d86a6/web)
- [Privacy Preferences Policy Control payload](https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web)
