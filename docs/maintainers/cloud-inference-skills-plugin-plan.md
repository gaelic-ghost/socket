# Cloud Inference Skills Plugin Plan

## Purpose

The `cloud-inference-skills` plugin helps agents choose and operate cloud AI inference, training, conversion, and GPU infrastructure workflows without turning `cloud-deployment-skills`, `python-skills`, Hugging Face, AWS, or Runpod guidance into one overloaded surface.

## Ownership

- `cloud-inference-skills` owns provider selection, official-tool routing, credential and cost boundaries, inference readiness, model artifact handling, and cross-provider handoffs.
- `cloud-deployment-skills` owns ordinary cloud application deployment routing, production infrastructure mutation boundaries, and non-model deployment handoffs.
- Stack plugins own application implementation details once the inference provider lane is chosen.
- Official provider plugins, MCP servers, CLIs, SDKs, and docs own provider-specific setup where they are current and available.

## First Slice

Create:

```text
plugins/cloud-inference-skills/
├── .codex-plugin/plugin.json
├── .mcp.json
├── AGENTS.md
├── assets/cloud-inference-icon.svg
└── skills/
    └── cloud-inference-routing-workflow/
        └── SKILL.md
```

The first skill should prefer Gale's familiar surfaces when they fit:

- Runpod for quick GPU Pods, Serverless endpoints, Flash, flexible experiments, templates, and MCP-backed resource management.
- Hugging Face for model and dataset repos, conversion artifacts, Inference Endpoints, Spaces, jobs, and Hub-native workflows.
- AWS for existing-account infrastructure, IAM, S3, CloudWatch, Lambda, SageMaker, Bedrock, ECS, EKS, and Batch.
- Vast.ai for cheap flexible GPU boxes where cleanup and artifact transfer are explicit.
- CoreWeave for cluster-shaped GPU infrastructure, Kubernetes, storage, networking, and production-grade GPU services.

## MCP Boundary

Bundle Runpod's official MCP configuration because it provides direct agent value for resource management and documentation lookup:

- `runpod`: stdio server via `npx -y @runpod/mcp-server@latest`, requiring `RUNPOD_API_KEY` from the Codex MCP environment.
- `runpod-docs`: unauthenticated remote docs MCP at `https://docs.runpod.io/mcp`.

Keep Runpod's upstream agent skills under the exported `skills/` tree, tracked by `skills-lock.json`, with `.agents/skills/` as a symlink discovery mirror. Refresh the upstream skills with Runpod's official package rather than hand-editing the copied skill files:

```bash
npx skills add runpod/skills
```

Do not duplicate Hugging Face or AWS setup while their first-party Codex plugins and CLIs already cover those surfaces.

## Later Slices

- Add provider-specific follow-up skills only after repeated real tasks show a narrow contract that official provider tools do not already cover.
- Consider a `cloud-inference-cost-review` workflow if GPU spend, idle resources, attached storage, and cleanup checks become frequent enough to justify a dedicated pass.
- Consider a `model-artifact-transfer-workflow` only if cross-provider weight, dataset, checkpoint, and cache movement becomes a repeated source of mistakes.

## Checklist

- [x] Create `plugins/cloud-inference-skills/` with `.codex-plugin/plugin.json`, `.mcp.json`, `AGENTS.md`, an icon asset, authored `skills/` source, and exported upstream Runpod skills.
- [x] Add `cloud-inference-skills:cloud-inference-routing-workflow`.
- [x] Bundle Runpod's official MCP server config without committing API keys.
- [x] Install Runpod's upstream `companion-clis`, `flash`, and `runpodctl` skills with `npx skills add runpod/skills`.
- [x] Wire `cloud-inference-skills` into the root Socket marketplace as an installable child plugin.
- [x] Update root README, CONTRIBUTING, and ROADMAP so users and maintainers understand the new plugin surface.
- [x] Run root metadata validation with `uv run scripts/validate_socket_metadata.py`.
