# DeviceCheck Device State

Use this reference when the request is about `DCDevice`, Apple-hosted per-device state, or the DeviceCheck query, update, and validate server endpoints.

## Decision Boundary

Use DeviceCheck when a server needs a narrow Apple-backed signal for a device, such as whether a device has already used a promotion or has been flagged by the service's own fraud policy.

Do not use DeviceCheck as account identity, user authentication, authorization, subscription state, local device fingerprinting, or a replacement for server-side abuse controls.

## App Responsibilities

- Import `DeviceCheck`.
- Check `DCDevice.current.isSupported` before calling `generateToken(completionHandler:)`.
- Generate a token only when the server needs to query, update, or validate the two bits.
- Send the token to the server over the app's existing authenticated transport when account context matters.
- Treat token generation errors as concrete operator-facing failures, including whether DeviceCheck is unsupported, token generation failed, or server verification failed.

## Server Responsibilities

- Obtain the DeviceCheck authentication key from Apple Developer account setup.
- Generate an ES256 JWT for Apple server API requests.
- Use the development DeviceCheck base URL only for development traffic.
- Use the production DeviceCheck base URL for production traffic.
- Implement query and update semantics for the two bits with clear business meaning.
- Store the meaning, timestamp, and policy attached to each bit in server-side docs or code, because Apple stores only the bit values and reports last-modified dates.
- Decide when a device's bits should be reset, such as account recovery, device resale, fraud review, or promotion policy expiry.

## Common Shapes

- Promotion eligibility: one bit records whether a device has used a trial, coupon, or bonus.
- Abuse flag: one bit records whether the service has decided to treat the device as high risk.
- Validation-only flow: the server validates that a token came from the app on an Apple device without changing bit state.

## Failure Modes

- DeviceCheck is not available on the device.
- The app lacks a registered App ID or the needed Apple Developer setup.
- The server JWT is malformed, expired, signed with the wrong key, or sent to the wrong environment.
- The server mixes business meanings for the two bits over time.
- The app treats the two bits as a user account property and surprises legitimate users who share, sell, replace, or restore devices.

## Validation Notes

- Unit-test server bit-policy mapping separately from Apple HTTP calls.
- Integration-test Apple endpoint calls only with development credentials and development endpoints unless production rollout is explicitly approved.
- Do not log device tokens, JWTs, Apple authentication keys, account identifiers, or raw server responses that include sensitive identifiers.
