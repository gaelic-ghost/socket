# Privacy, Security, and Validation

## Privacy Contract

Write down which handler reads which mail field, why it needs that field, where it is processed, whether it leaves the device, and when it is deleted. Avoid storing message bodies, addresses, headers, attachments, and remote identifiers. Redact diagnostics so they identify a handler and failure reason without exposing message data.

## Security Contract

For message security, document key provenance, identity selection, recipient key discovery, trust decisions, encryption/signature state, algorithm compatibility, revoked or unavailable keys, and user-visible recovery. Do not treat a custom header or an opaque shared preference as proof that a message was secured.

## Validation Matrix

Validate enabled and disabled extension states, each declared capability, malformed messages, unavailable remote content, empty or invalid recipients, delivery rejection, missing or invalid key material, offline behavior, app upgrade, and clean-install signing/embedding. Use a disposable mailbox and non-production identities for fixtures.

## Sources

- [Build Mail App Extensions](https://developer.apple.com/documentation/mailkit/build-mail-app-extensions)
- [MEComposeSessionHandler.allowMessageSendForSession(_:completion:)](https://developer.apple.com/documentation/mailkit/mecomposesessionhandler/allowmessagesendforsession(_:completion:))
- [MEMessageSecurityHandler](https://developer.apple.com/documentation/mailkit/memessagesecurityhandler)
