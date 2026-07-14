---
name: discord-app-workflow
description: Plan, build, and validate Discord apps, bots, commands, interactions, Gateway event handling, and Activities using current Discord documentation.
---

# Discord App Workflow

## Workflow

1. Choose a bot, user-installed app, guild-installed app, or Activity. Do not select Gateway when signed HTTP interactions are sufficient.
2. Register the application and scope the requested permissions, OAuth installation, commands, and intents to the least access needed.
3. For interactions, verify Discord's signature, answer the required initial interaction promptly, and use follow-ups or deferred responses for longer work.
4. For Gateway usage, document intents, privileged-intent approval, reconnect/resume state, sharding threshold, and rate-limit behavior.
5. Model commands, buttons, selects, and modals as explicit user actions with durable component state and authorization checks.
6. Validate in a test guild/account with observed command registration, signature verification, retry/duplicate behavior, and permission denial.

## Handoffs

Use `webhook-and-event-lifecycle` for request handling, `conversation-state-human-handoff` for state, and the target server stack skill for implementation. Consult the [Discord application overview](https://docs.discord.com/developers/quick-start/overview-of-apps) and [Interactions documentation](https://docs.discord.com/developers/platform/interactions) before asserting behavior.
