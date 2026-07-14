---
name: teams-agent-workflow
description: Plan, build, and validate Microsoft Teams bots and agents with Teams SDK or Microsoft 365 Agents SDK, Microsoft Entra, Adaptive Cards, and tenant deployment boundaries.
---

# Teams Agent Workflow

## Workflow

1. Choose Teams SDK for a Teams-first app or Microsoft 365 Agents SDK for a multi-channel agent runtime; document the reason and current supported language.
2. Define tenant, Microsoft Entra identity, app registration, manifest, installation, and administrator-consent needs before implementation.
3. Treat message activities, Adaptive Card actions, task modules, and agent tool calls as separate authorized input surfaces.
4. Verify inbound activity authenticity using the selected Microsoft runtime, preserve conversation and tenant context, and make outbound/proactive messaging consent-aware.
5. Provide a clear human escalation and error experience inside Teams rather than leaking runtime failures to users.
6. Validate sideloaded development behavior, tenant install, identity failure, card-submit authorization, proactive-send preconditions, and production deployment review.

## Handoffs

Use the current [Teams bot overview](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/overview) and the documented SDK comparison before implementation. Hand service code to the selected TypeScript, Python, .NET, Java, or Swift server workflow.
