# App Attest Server Validation

Use this reference when the request crosses into server-side App Attest verification, receipt handling, fraud metrics, or assertion validation.

## Boundary

Apple Dev Skills can describe the server contract and validation checklist, but backend implementation belongs to the relevant server-side Swift, OpenAPI, RPC, or backend-specific workflows when code changes are needed.

The server owns trust. The app collects Apple framework outputs; it does not decide that it is legitimate.

## Challenge Contract

- Generate randomized, unique, single-use challenges.
- Associate each challenge with the account, device record, operation, environment, and expiration time.
- Reject expired, missing, reused, or mismatched challenges.
- Include the challenge in attestation and assertion verification.
- Do not let the client choose or replay challenges.

## Attestation Verification Checklist

Server verification usually needs to:

- decode the attestation object as CBOR
- verify the Apple App Attest certificate chain
- verify the Apple-specific attestation statement format
- recompute the nonce from authenticator data and the challenge hash
- verify the certificate extension nonce
- verify that the key ID matches the attested public key
- verify the RP ID hash for the app's App ID
- verify the counter starts at zero
- verify the App Attest environment through `aaguid`
- verify the credential ID
- verify Apple extension fields such as validation category and bundle version when the current Apple docs require them
- store the public key, key ID, receipt, environment, account, device association, and starting counter

On macOS, Apple documents additional verification details involving the signing identifier and the key access-policy hash. Do not treat iOS-only verification notes as sufficient for macOS.

## Assertion Verification Checklist

For each protected request, the server usually needs to:

- decode the assertion object
- rebuild the client data from the protected request and one-time challenge
- hash the client data
- verify the signature with the stored public key
- verify the RP ID hash
- verify the assertion counter is greater than the previous stored counter
- verify the embedded challenge matches the server-issued challenge
- verify environment, validation category, and bundle version when relevant
- store the updated counter after successful verification
- reject replayed or out-of-order assertions

## Receipt and Fraud Metric Handling

The attestation statement includes a receipt that the server can use for App Attest fraud metric requests.

Server handling should:

- verify receipts before trusting them
- store one key/receipt pair per user-device-environment association
- keep development and production pairs separate
- use the sandbox App Attest data endpoint for sandbox receipts
- use the production App Attest data endpoint for distributed app receipts
- refresh metrics only after the receipt's not-before date and before expiration
- treat the returned metric as a risk signal, not a single automatic allow/deny rule

## Common Server Handoffs

- Use server-side Swift guidance for Vapor, Hummingbird, JWT signing, CBOR/COSE/ASN.1 parsing, route handlers, and persistence models.
- Use OpenAPI or RPC guidance when the app/server challenge, attestation, assertion, or fraud-metric API contract is the main design artifact.
- Use security review workflows when the implementation touches production keys, abuse policy, fraud scoring, or high-impact access control.

## Logging and Secrets

Do not log:

- raw challenges after issuance
- assertion objects
- attestation objects
- receipts
- private server keys
- Apple authentication keys
- generated JWTs
- account identifiers next to raw device integrity artifacts

Prefer structured logs that say which phase failed, which environment was used, and which high-level verification check failed without exposing the artifact.
