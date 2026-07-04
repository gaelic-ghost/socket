# Cloud Deployment Skills Plugin Plan

## Purpose

Add a thin Socket-owned cloud deployment routing plugin without duplicating first-party provider agent tooling.

The first practical use case is AWS. AWS now publishes the official [`aws/agent-toolkit-for-aws`](https://github.com/aws/agent-toolkit-for-aws) Codex marketplace, and its `aws-core` plugin bundles AWS MCP Server configuration plus curated AWS skills. Socket should route users there instead of carrying copied AWS CLI, AWS SAM CLI, or AWS MCP setup guidance.

## Ownership

- `cloud-deployment-skills` owns provider selection, official-tool routing, credential and mutation boundary checks, and cross-provider deployment handoffs.
- AWS owns the AWS Agent Toolkit, AWS MCP Server configuration, and AWS skill content.
- Stack plugins keep framework-specific deployment details, such as Server-Side Swift Fly.io deploy workflows.

## First Slice

- Add `plugins/cloud-deployment-skills/`.
- Add one skill: `cloud-deployment-routing-workflow`.
- Wire the plugin into the root Socket marketplace.
- Update root README and ROADMAP so the install surface is visible and the AWS delegation decision is durable.
- Keep the plugin guidance-only. Do not bundle `.mcp.json` for AWS.

## Future Slices

- Add Cloudflare deployment routing if Socket needs guidance beyond existing Cloudflare docs and tooling.
- Add Vercel deployment routing if web project handoffs need a first-party Socket decision layer.
- Add Fly.io provider-neutral routing only if the existing Server-Side Swift workflow is too narrow for non-Swift projects.
- Add Terraform, Pulumi, CDK, Azure, or GCP slices only after concrete project use proves that official provider docs or plugins are not enough.

## Validation

- Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.
- Run `git diff --check`.
- For release, follow the standard Socket release mode because this is a monorepo-owned child plugin with no subtree synchronization requirement.
