---
name: use-nous-research-services
description: Use and troubleshoot Nous Research services with Hermes Agent, including Nous Portal inference, Tool Gateway backends, Nous Chat, subscription proxy, and Hermes Cloud hosted deployment.
metadata:
  hermes:
    category: agent-portability
    tags: [nous, portal, tool-gateway, cloud, inference]
---

# Use Nous Research Services

Identify the Nous product before changing authentication or routing.

## Product Map

| Product | Job |
| --- | --- |
| Nous Portal | OAuth-authenticated subscription and inference provider for Hermes and Nous services |
| Nous Tool Gateway | Per-tool hosted backends selected inside Hermes |
| Nous Chat | Web chat using the Portal account and model catalog |
| Subscription proxy | Local OpenAI-compatible proxy that lets other apps use Hermes-managed subscription credentials |
| Hermes Cloud | Portal-hosted Hermes deployment surface; inspect the live Portal and current official docs before claiming plans, regions, sizes, persistence, or lifecycle behavior |

Do not call the messaging gateway or TUI gateway “Nous Gateway.”

## Configure Portal Deliberately

- For a fresh Hermes setup, use `hermes setup --portal` when the user wants both Portal inference and the managed tool onboarding path.
- For an existing install, use `hermes model` to add Nous without erasing other providers.
- Use `/model` only to switch among already configured choices inside a session.
- Use `hermes portal info` and `hermes portal tools` to inspect auth and routing.
- Treat the refresh token in the Hermes auth store as a secret.
- Keep Portal inference selection separate from per-tool Tool Gateway selection.

## Configure Tool Gateway Per Tool

Use `hermes tools` to choose Nous-hosted backends individually. A user may mix Nous-hosted web or image tools with their own browser, TTS, or other provider. Verify the active route instead of inferring it from Portal login alone.

Current documented categories include web search/extract, image generation, text-to-speech, cloud browser automation, and an optional cloud terminal sandbox. Availability, free pools, add-ons, partners, models, and pricing can change; read the live Portal or official docs for current entitlement claims.

## Use the Subscription Proxy Carefully

The proxy is a local credential-forwarding service for OpenAI-compatible clients. It is not the Hermes API server:

- subscription proxy: forwards supported provider endpoints using Hermes-managed OAuth;
- Hermes API server: runs the agent loop and its tools behind an OpenAI-compatible interface.

Keep the proxy on localhost unless the user has explicitly designed network authentication. Do not treat an arbitrary client bearer as meaningful protection when the proxy accepts placeholder bearer values and attaches the real upstream credential.

## Handle Hermes Cloud as a Live Hosted Surface

Hermes Cloud is newer and more likely to change than the open-source CLI contract. Before creating, resizing, stopping, deleting, or billing a deployment:

1. Inspect the current official Portal UI or current official documentation.
2. Record the available model, server size, persistence, region, pricing, and lifecycle choices shown now.
3. Distinguish the hosted Hermes instance from a self-hosted VM, Modal terminal backend, Daytona backend, or cloud terminal tool.
4. Ask before any billable deployment or destructive lifecycle action.
5. Verify access, profile state, gateway reachability, persistence, and shutdown behavior after changes.

Do not infer undocumented cloud controls from announcements or screenshots.

## Verification

Return the active provider, selected model, each affected tool route, entitlement evidence, local secret location class, and whether any hosted resource or billing state changed.

Read [references/nous-services-map.md](references/nous-services-map.md) for the detailed distinctions, commands, risks, and authoritative sources.
