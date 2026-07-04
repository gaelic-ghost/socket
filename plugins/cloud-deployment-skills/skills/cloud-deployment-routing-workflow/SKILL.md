---
name: cloud-deployment-routing-workflow
description: Choose the right cloud deployment path before implementation, routing AWS work through the official AWS Agent Toolkit for AWS when appropriate and keeping provider credentials, regions, and mutation boundaries explicit.
license: PolyForm-Noncommercial-1.0.0
compatibility: Designed for Codex and compatible Agent Skills clients working with cloud deployments, provider CLIs, provider plugins, MCP servers, and repository-owned deployment configuration.
metadata:
  owner: gaelic-ghost
  repo: socket
  category: cloud-deployment-routing
allowed-tools: Read Bash(rg:*) Bash(git:*) Bash(codex:*) Bash(aws:*) Bash(uv:*) Bash(uvx:*)
---

# Cloud Deployment Routing Workflow

## Purpose

Choose the smallest correct cloud deployment path before changing infrastructure, credentials, or production-facing configuration.

The practical decision is whether the agent should use an official provider plugin, a provider MCP server, a provider CLI, a framework-owned deployment workflow, or a Socket-owned provider skill.

## When To Use

- Use this skill when the user wants cloud deployment help and has not chosen a provider-owned workflow.
- Use this skill when a project mentions AWS, Cloudflare, Vercel, Fly.io, Azure, GCP, Terraform, Pulumi, CDK, CloudFormation, SAM, containers, serverless, hosting, DNS, secrets, deployment, or production infrastructure.
- Use this skill before adding provider credentials, changing cloud resources, deploying production services, or wiring new MCP server configuration.
- Use this skill when an official provider plugin may already own the requested work.

## Source Check

Use repo-local deployment files, checked-out provider config, installed provider CLIs, official provider plugins, and official provider documentation before making claims about current deployment behavior:

- [Agent Toolkit for AWS](https://github.com/aws/agent-toolkit-for-aws)
- [AWS Agent Toolkit plugins](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/plugins.html)
- [AWS MCP Server setup](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)

Translate any documentation rule into the concrete repository decision it changes.

## Routing Workflow

1. Inspect the project shape:
   - deployment manifests such as `template.yaml`, `serverless.yml`, `cloudformation.yml`, `cdk.json`, `samconfig.toml`, `wrangler.toml`, `vercel.json`, `fly.toml`, `Dockerfile`, `compose.yaml`, Terraform, or Pulumi files
   - package scripts, Make targets, CI workflows, release docs, and provider-specific README sections
   - existing credentials guidance, environment variables, account aliases, regions, profiles, and secret names
2. Identify the deployment job:
   - provider selection
   - local credential setup
   - documentation lookup
   - infrastructure planning
   - preview or diff
   - dev/staging deploy
   - production deploy
   - failure triage
   - cost, IAM, observability, or rollback review
3. Route AWS work first:
   - Prefer the official AWS Agent Toolkit for AWS for Codex when the task is general AWS discovery, AWS MCP access, AWS CLI or AWS SAM setup, CDK, CloudFormation, serverless, containers, storage, observability, billing, SDK usage, or deployment.
   - Install path for Codex users:

     ```bash
     codex plugin marketplace add aws/agent-toolkit-for-aws
     ```

     Then use `/plugins` in Codex to install `aws-core`.
   - Do not duplicate AWS MCP configuration in Socket while `aws-core` bundles that configuration.
   - Do not copy AWS Agent Toolkit skills into Socket.
4. Route non-AWS work:
   - Use a first-party provider plugin or MCP server when one exists and is current.
   - Use framework-owned Socket skills when the deployment surface is already covered by a stack workflow, such as `server-side-swift:fly-io-deployment-workflow`.
   - Add or use a Socket-owned provider skill only when no official provider-owned agent surface exists or when Socket needs a small provider-neutral decision layer.
5. Confirm mutation boundaries:
   - account or organization
   - project or app
   - region
   - profile or identity
   - environment such as local, dev, staging, or production
   - exact resource mutations
   - expected cost or billing effect
   - rollback or cleanup path
6. Choose validation:
   - read-only documentation or discovery query for planning
   - provider CLI version and auth check for local setup
   - plan, diff, dry-run, validate, package, or synth command before deploy
   - smoke test, logs, metrics, and rollback checks after deploy

## Recommendations

### AWS

Use the official AWS Agent Toolkit for AWS as the default Codex path. It owns AWS MCP setup and the curated AWS skill set, including common deployment, CDK, CloudFormation, serverless, container, storage, observability, billing, and SDK workflows.

Use Socket only for the routing decision, local repo handoff, and any project-specific deployment guardrails that the official AWS plugin does not know.

### Framework-Owned Deployments

When a stack plugin already owns a deployment path, use that plugin for stack-specific implementation details. For example, Fly.io deployment for Vapor or Hummingbird services belongs in `server-side-swift` because that workflow depends on Swift package, Dockerfile, health-check, and runtime conventions.

### Future Provider Skills

Add future provider skills as small routing or implementation slices. Good candidates include Cloudflare, Vercel, Fly.io, Azure, GCP, Terraform, Pulumi, and CDK when an official provider plugin does not already give Codex a better maintained path.

## Output Shape

Return:

1. `Provider`: AWS, Cloudflare, Vercel, Fly.io, Azure, GCP, multi-cloud, or undecided.
2. `Primary surface`: official provider plugin, MCP server, provider CLI, framework-owned skill, Socket provider skill, or user decision needed.
3. `Credential boundary`: account, region, profile, environment, and whether credentials are required for the next step.
4. `Mutation boundary`: read-only, plan/diff, staging deploy, production deploy, cleanup, or blocked.
5. `Validation path`: exact commands or agent checks to run before and after mutation.
6. `Next handoff`: official plugin install, provider docs, stack skill, or provider-specific Socket backlog item.

## Guardrails

- Do not invent provider setup steps when an official provider plugin or current provider docs own the path.
- Do not configure or mutate cloud accounts without confirming account, region, profile, environment, and intended resource changes.
- Do not store credentials, tokens, account IDs, secrets, local profiles, or `.env` files in git.
- Do not present an AWS CLI, AWS SAM CLI, or AWS MCP setup path as Socket-owned while AWS Agent Toolkit owns the official Codex path.
- Do not deploy to production by default. Use planning, validation, and explicit user confirmation before production mutations.
