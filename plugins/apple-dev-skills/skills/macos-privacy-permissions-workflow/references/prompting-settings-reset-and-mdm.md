# Prompting, Settings, Reset, And MDM

## Request lifecycle

1. Preflight or read the framework status without prompting when the API supports it.
2. Request from a direct user action only when the status and public contract allow a request.
3. Explain the concrete operation and target before system UI appears.
4. Preserve denied, restricted/managed, limited, and authorized as distinct states.
5. Provide a non-coercive denial path and the current Privacy & Security location when a later change is possible.
6. Apply the documented relaunch, helper restart, logout, or retry boundary, then reproduce the original operation.

Never loop requests, hide the responsible app behind a generic host, or automate Settings to defeat consent.

## Reset boundary

`tccutil` is a supported reset surface, not a general grant or status tool. Before a reset, record the service/class, bundle identity, reason, current reproduction, expected next prompt, and rollback/test cleanup. Use only the syntax supported by `man tccutil` on the current OS. A reset removes a decision; it does not authorize access.

Do not manipulate a live TCC database, copy an edited database back, or use SQL output as an app-facing support contract. Use private schemas only in an approved exact-build Reverse Engineering task.

## MDM and PPPC

PPPC identifies code using the documented bundle/code requirement fields and supports only the service classes and authorization values Apple documents for the current OS. A payload may allow, deny, or require user approval depending on the class; do not assume MDM can silently allow every permission. Record supervision/enrollment state, payload scope, designated requirement, authorization value, conflict/precedence evidence, and the device's applied-profile state.

Use [Apple's PPPC payload documentation](https://support.apple.com/guide/deployment/privacy-preferences-policy-control-payload-dep38df53c2a/web) as the source of truth for current services and allowed authorization values.
