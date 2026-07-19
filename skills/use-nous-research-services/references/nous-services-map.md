# Nous Research Services Map

## Nous Portal

Portal is the subscription, OAuth, inference, and entitlement surface used by Hermes. A fresh `hermes setup --portal` can authenticate Portal, select a model, set Nous as the provider, and offer managed tool routing. Existing installs can add Nous alongside other providers with `hermes model`.

Portal authentication does not prove that every tool is routed through Nous. Verify with `hermes portal info`, `hermes portal tools`, and the per-tool configuration.

## Nous Tool Gateway

The Tool Gateway provides hosted backends on a per-tool basis. Official docs currently describe web search/extract, image generation, text-to-speech, cloud browser automation, and an optional Modal cloud terminal sandbox. Partners, models, entitlements, free pools, add-ons, and pricing can change.

The gateway is mix-and-match: selecting Nous for one tool does not require selecting it for the model or every other tool.

## Nous Chat

Nous Chat is the web chat surface associated with the Portal account and model catalog. It does not run the local Hermes profile, local skills, local memory, local tools, or messaging gateway merely because it shares the account.

## Subscription Proxy

The subscription proxy is a local OpenAI-compatible forwarding service. It attaches Hermes-managed provider credentials to supported upstream requests. It does not execute Hermes skills or the agent tool loop.

Keep it bound to localhost by default. If exposed to a LAN, add a real firewall, VPN, or authenticating reverse proxy; the upstream-facing bearer placeholder is not local access control.

## Hermes Cloud

Hermes Cloud is a Portal-hosted deployment surface announced by Nous Research. It is distinct from:

- a self-hosted Hermes gateway on a VPS;
- Modal or Daytona as terminal backends;
- the Tool Gateway cloud terminal sandbox;
- Nous Portal inference;
- the local dashboard or API server.

The hosted UI and terms can evolve faster than the open-source CLI docs. Inspect current Portal controls before documenting or changing model, server size, region, persistence, networking, billing, lifecycle, backup, or deletion behavior. Treat deployment creation and resizing as billable external changes, and deletion as destructive.

## Data-Flow Questions

For each configured service, identify:

1. where the Hermes agent loop runs;
2. where inference runs;
3. where each tool runs;
4. where credentials are stored;
5. where memory, skills, sessions, and files persist;
6. which account owns billing;
7. which network endpoints are exposed.

Do not summarize a hybrid deployment as simply “local” or “cloud.”

## Authoritative Sources

- [Nous Portal](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal)
- [Run Hermes with Nous Portal](https://hermes-agent.nousresearch.com/docs/guides/run-hermes-with-nous-portal)
- [Nous Tool Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/features/tool-gateway)
- [Providers](https://hermes-agent.nousresearch.com/docs/integrations/providers)
- [Subscription proxy](https://hermes-agent.nousresearch.com/docs/user-guide/features/subscription-proxy)
- [API server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server/)
- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
- [Nous Research Hermes Cloud announcement](https://x.com/NousResearch/status/2074878754485043333)
