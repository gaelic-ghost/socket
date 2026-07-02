# DeviceCheck and App Attest Skill Record

This record captures the shipped Apple Dev Skills expansion for the DeviceCheck framework, including per-device DeviceCheck state and App Attest app-instance validation.

## Status

Implemented. The first implementation shipped one focused workflow skill, `devicecheck-app-attest-workflow`, rather than separate `device-identification` and `app-attest` skills.

## Ownership

This skill belongs in `plugins/apple-dev-skills` because it depends on Apple framework behavior, app IDs, entitlements, Xcode signing state, Apple Developer account setup, local Apple documentation, and Apple server APIs.

The skill should stay separate from the broader client auth and sync milestone. DeviceCheck and App Attest are risk and integrity signals for a server-backed app, not a general credential-storage or session-management workflow.

The server verification side should be explicit but bounded. Apple Dev Skills can guide the client/server contract, challenge shape, App Attest object flow, and validation checklist, but server implementation should hand off to server-side Swift, OpenAPI, or RPC workflows when the backend code or API contract is the primary change.

## Documented Apple Behavior To Rely On

Apple documentation describes DeviceCheck as a framework plus Apple server APIs for reducing fraudulent use by managing device state and asserting app integrity.

Device identification uses `DCDevice` in the app to generate an ephemeral token. The server uses that token with a JWT-backed Apple server request to query, update, or validate two per-device bits stored by Apple. The app must check `DCDevice.current.isSupported`, and the app must have an Apple Developer registered App ID.

App Attest uses `DCAppAttestService` to generate a Secure Enclave-backed key, ask Apple to attest that key, and later generate assertions for sensitive server requests. The app must check `DCAppAttestService.shared.isSupported`, the app must have a registered App ID, and server-side challenge handling is required to prevent replay attacks.

App Attest has important rollout and environment constraints:

- Sandbox and production keys and receipts are separate.
- Distributed apps operate in production mode.
- Large existing user bases should ramp attestation gradually because attestation contacts Apple servers and can be rate limited.
- Attestation failures with `serverUnavailable` should retry later using the same key and `clientDataHash`.
- App Attest does not prove that a device operating system is uncompromised; it supplies one signal for a broader fraud-risk decision.
- On macOS, App Attest verification has macOS-specific signing identifier and key access-policy checks.

## Implemented Skill

### `devicecheck-app-attest-workflow`

Use for DeviceCheck and App Attest decisions in Apple-platform apps, including `DCDevice`, per-device two-bit state, `DCAppAttestService`, App Attest key lifecycle, server challenge design, attestation and assertion request shapes, app IDs, entitlements, sandbox versus production environments, rollout/rate-limit planning, and client/server handoffs.

This skill helps an agent:

- classify whether the request is DeviceCheck two-bit device state, App Attest app-instance integrity, or a broader auth/session/sync concern
- apply the Apple docs gate before making current framework, entitlement, platform, or server-endpoint claims
- preserve the client/server boundary instead of pretending the app can validate itself
- keep key identifiers persistent but avoid storing secrets or treating attestation objects as app-side proof
- distinguish development, sandbox, TestFlight, App Store, Enterprise, Developer ID, and macOS signing behavior where Apple docs require it
- plan server challenges, replay protection, assertion counters, public-key storage, receipt storage, and risk metrics without making Apple Dev Skills own a backend implementation
- route Xcode signing, entitlements, App ID capability, build, run, simulator, device, and test follow-through to `xcode-build-run-workflow` or `xcode-testing-workflow`
- route generated client APIs to `swift-openapi-client-workflow`
- route backend validation implementation to the relevant server-side Swift or API-contract workflow when available

## Shipped Skill Shape

The shipped first version is guidance and routing, not a deterministic validator. App Attest server verification includes CBOR, COSE, ASN.1, certificate-chain, receipt, environment, signing-category, and counter checks, which are too stack-specific for a tiny first slice.

Shipped first payload:

- `SKILL.md` with the core workflow, docs gate, classification, handoffs, and guardrails.
- `agents/openai.yaml` metadata generated from the skill body.
- `references/devicecheck-device-state.md` for `DCDevice`, two-bit state, JWT, query/update/validate endpoints, privacy, and reset semantics.
- `references/app-attest-client-flow.md` for `DCAppAttestService`, key ID persistence, challenge hashing, attestation, assertions, `DCError`, and retry behavior.
- `references/app-attest-server-validation.md` for server-side validation checklist, receipt/risk metric handling, sandbox versus production, replay protection, counters, and macOS-specific validation notes.
- `references/entitlements-app-id-and-validation.md` for App ID, DeviceCheck capability, App Attest environment entitlement, provisioning, Xcode handoffs, simulator/device expectations, and rollout gates.

Avoid scripts in the first slice unless a concrete backend stack needs one. If a later project repeatedly needs App Attest verification in Swift, add a separate deterministic reference implementation or test helper after the server-side owner is clear.

## Implementation Slices

1. Planning and docs evidence:
   - [x] Add this plan and roadmap milestone.
   - [x] Keep the plan grounded in Xcode and Dash documentation lookups.
   - [x] Decide the one-skill shape unless implementation evidence shows the workflow becomes too large.
2. Skill scaffold:
   - [x] Initialize `devicecheck-app-attest-workflow` under `plugins/apple-dev-skills/skills/`.
   - [x] Add references and generated `agents/openai.yaml`.
   - [x] Keep `SKILL.md` concise and move detailed validation checklists into references.
3. Metadata and inventory:
   - [x] Update `plugins/apple-dev-skills/.codex-plugin/plugin.json`.
   - [x] Update `plugins/apple-dev-skills/README.md` active skill inventory and prompt list.
   - [x] Update `plugins/apple-dev-skills/ROADMAP.md` status and ticket completion.
4. Tests and validation:
   - [x] Add targeted tests for frontmatter, routing boundaries, docs-gate language, server-handoff language, and metadata inventory.
   - [x] Run `bash .github/scripts/validate_repo_docs.sh` from `plugins/apple-dev-skills`.
   - [x] Run `uv run pytest` from `plugins/apple-dev-skills` when tests change.
   - [x] Run `uv run scripts/validate_socket_metadata.py` from the Socket root after metadata changes.

## Future Questions

- The first implementation uses `devicecheck-app-attest-workflow`; a broader `apple-app-integrity-workflow` can still be considered later if another Apple integrity signal needs a shared owner.
- Should server-validation guidance stay purely checklist-based at first, or should the initial skill include stack-specific examples for Swift server apps?
- Should DeviceCheck two-bit state and App Attest stay permanently in one skill, or should DeviceCheck split out later if two-bit state becomes common outside App Attest integrity flows?
- Should the first implementation include migration guidance for apps that already use custom device identifiers, receipt validation, or server-side abuse flags?
