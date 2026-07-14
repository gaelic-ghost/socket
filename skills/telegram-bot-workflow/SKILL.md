---
name: telegram-bot-workflow
description: Plan, build, and validate Telegram Bot API integrations, webhooks or polling, inline interactions, and Mini Apps.
---

# Telegram Bot Workflow

## Workflow

1. Choose Bot API interaction, inline mode, group behavior, or Mini App. Use MTProto/TDLib only when building a Telegram client rather than a bot.
2. Register through BotFather and keep the token in the selected secret store; never commit it.
3. Decide between webhook delivery and polling based on the deployed runtime, public endpoint, and local-development needs. Do not run both against the same update stream.
4. Account for the initiation boundary: bots cannot begin a private chat before a user starts one or adds the bot to a group.
5. Use update IDs for idempotency, acknowledge callback queries promptly, and design keyboards or Mini App actions with authorization and expiry checks.
6. Test private chat, group privacy mode, callback handling, duplicate updates, bot restart, and command discovery.

## Handoffs

Use [Telegram's Bot API](https://core.telegram.org/bots/api) and [Bots introduction](https://core.telegram.org/bots) as primary sources. Hand HTTP service work to the chosen server stack skill.
