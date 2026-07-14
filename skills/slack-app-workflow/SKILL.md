---
name: slack-app-workflow
description: Plan, build, and validate Slack workspace apps with OAuth, Events API, interactivity, slash commands, modals, and Socket Mode.
---

# Slack App Workflow

## Workflow

1. Choose a workspace app, distribution model, event delivery route, and a narrow OAuth scope inventory before code.
2. Use Events API plus a public receiver when the service owns inbound HTTPS; use Socket Mode only when its operational model fits the deployment.
3. Verify Slack request signatures, acknowledge events and interactive payloads promptly, and use the response URL or Web API only within their documented lifecycle.
4. Treat workspace, enterprise, channel, user, and installation identities as distinct. Check authorization before acting on a command, shortcut, modal submission, or message event.
5. Make interactive state explicit and short-lived; never place secrets or unverified authority in action values.
6. Validate OAuth reinstall, scope changes, signature failures, retry headers, modal errors, and a workspace-admin removal path.

## Handoffs

Start with [Slack apps](https://api.slack.com/docs/apps) and [Bolt](https://api.slack.com/bolt). Use `webhook-and-event-lifecycle` and the selected server stack skill for implementation.
