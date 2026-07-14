# MailKit Capabilities and Handler Boundaries

MailKit’s `MEExtension` provides handlers for the capabilities declared in the extension’s `MEExtensionCapabilities` array.

| Capability | Handler role | Boundary |
| --- | --- | --- |
| `MEContentBlocker` | Supplies JSON rules for remote content shown in Mail. | Declarative blocking only; it is not arbitrary message inspection. |
| `MEMessageActionHandler` | Chooses actions as Mail downloads messages. | Make decisions explicit and explainable. |
| `MEComposeSessionHandler` | Validates recipients, supports compose UI, allows delivery, and adds headers. | Preserve sender intent and give concrete delivery feedback. |
| `MEMessageSecurityHandler` | Encrypts and digitally signs messages. | Requires an explicit key, trust, consent, and recovery design. |

Mail applies content-blocking rules from enabled extensions even when a person chooses to load remote content. Treat those rules as a durable privacy and product-policy decision.

## Sources

- [MailKit](https://developer.apple.com/documentation/mailkit)
- [MEContentBlocker](https://developer.apple.com/documentation/mailkit/mecontentblocker)
- [MEMessageActionHandler](https://developer.apple.com/documentation/mailkit/memessageactionhandler)
- [MEComposeSessionHandler](https://developer.apple.com/documentation/mailkit/mecomposesessionhandler)
- [MEMessageSecurityHandler](https://developer.apple.com/documentation/mailkit/memessagesecurityhandler)
