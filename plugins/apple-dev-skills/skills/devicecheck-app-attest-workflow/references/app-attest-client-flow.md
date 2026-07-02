# App Attest Client Flow

Use this reference when the request is about `DCAppAttestService`, app-side key lifecycle, challenge hashing, attestation, assertions, or app fallback behavior.

## Availability

Start by checking `DCAppAttestService.shared.isSupported`.

If App Attest is unsupported, the app and server both need a fallback. The fallback can allow access with lower trust, require additional server-side risk checks, or block high-risk actions, but that policy belongs on the server.

Apple documents that Action, extensible SSO, and watchOS extensions are supported, while other extension types are not supported even if `isSupported` returns true.

## Key Creation

- Call `generateKey(completionHandler:)` to generate one App Attest key per user account per device when possible.
- Persist the returned key identifier in durable app storage.
- Do not try to read or export the private key; the framework keeps it protected.
- Do not reuse one key for multiple remote users on the same device.
- Use the same key pair between an App Clip and its corresponding full app when applicable, storing the identifier in a shared container.
- Expect keys to survive normal app updates but not app reinstall, device migration, or restore from backup.

## Attestation

The app should ask the server for a unique, single-use challenge before attestation.

Client flow:

1. Get a challenge from the server.
2. Hash the challenge with SHA256 to form `clientDataHash`.
3. Call `attestKey(_:clientDataHash:completionHandler:)` with the key ID and hash.
4. Send the attestation object and key ID to the server.
5. Persist the key ID for future assertions after the server accepts the attestation.

If `attestKey` fails with `serverUnavailable`, retry later using the same key and the same `clientDataHash`. For other key-related failures, discard the key identifier and create a new key when retrying.

## Assertions

After successful server verification, the app can generate assertions for sensitive requests.

Client flow:

1. Ask the server for a unique, single-use challenge.
2. Build client data that includes the challenge and the request being protected.
3. Hash the client data with SHA256.
4. Call `generateAssertion(_:clientDataHash:completionHandler:)`.
5. Send the assertion object and client data to the server with the protected request.

Assertions should be used at meaningful risk points, such as premium content, account-sensitive changes, fraud-sensitive redemption, or other server-defined sensitive operations.

## App-Side Storage

Store:

- key ID
- account association needed to select the right key
- attestation state accepted by the server
- environment marker when development and production flows may coexist during testing

Do not store:

- private keys
- reusable challenges
- Apple server authentication keys
- raw assertion objects as proof without server verification
- sensitive server risk decisions in app-local state

## Operator-Facing Errors

Make errors say what failed and where:

- App Attest unsupported on this device or extension type.
- App Attest key generation failed before attestation.
- App Attest attestation could not reach Apple; retry later with the same key and challenge hash.
- Server rejected the attestation object for this key ID.
- Server rejected the assertion for this request challenge.
- Stored key ID is missing, stale, or tied to a different account/environment.
