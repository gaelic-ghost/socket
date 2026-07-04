# AGENTS.md

This file is the Cloud Inference Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general git, docs, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `cloud-inference-skills` is a monorepo-owned Socket child and the canonical source of truth for shipped cloud AI inference, training, conversion, and GPU infrastructure routing skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Keep this plugin focused on provider selection, official-tool routing, inference readiness, GPU cost boundaries, model artifact handling, and cross-provider handoffs.
- Keep application implementation in the owning stack plugins such as `python-skills`, `server-side-swift`, `web-dev-skills`, `rust-skills`, `server-side-jvm`, and `cloud-deployment-skills`.

## Local Rules

- Match the `socket` shared semantic version exactly; use the Socket root release workflow for version inventory and bumps.
- Prefer official provider plugins, MCP servers, CLIs, SDKs, and docs before adding Socket-authored setup guidance.
- Treat Runpod, Hugging Face, and AWS as preferred familiar surfaces when they fit the requested inference or training job.
- For Runpod work, use the bundled Runpod MCP config when resource management or docs lookup benefits from MCP, and treat the `.agents/skills/companion-clis`, `.agents/skills/flash`, and `.agents/skills/runpodctl` directories as an upstream installed Runpod skill mirror tracked by `skills-lock.json`.
- Do not hand-edit the upstream Runpod skill mirror. Refresh it with `npx skills update` or reinstall with `npx skills add runpod/skills` from this plugin root, then review the diff and security notes before committing.
- For Hugging Face work, prefer the installed Hugging Face Codex plugin and official `huggingface_hub` CLI before adding Socket-owned API or repo-management guidance.
- For AWS work, prefer the official AWS Agent Toolkit and AWS CLI or SDK surfaces before adding Socket-owned AWS guidance. Treat AWS Lambda inference as a fit only for small, latency-tolerant CPU or accelerator-backed workloads; route GPU or large-model serving to SageMaker, Bedrock, ECS/EKS, Batch, or another provider unless current AWS docs and project constraints support Lambda.
- For Vast.ai and CoreWeave work, keep the first pass routing-oriented unless the task has concrete account, image, scheduler, storage, networking, and teardown requirements.
- Treat provider credentials, account configuration, API mutation, billing, model weights, private datasets, generated artifacts, and production endpoints as high-impact operations. Verify the account, region, resource, image, model license boundary, expected cost, and cleanup path before taking action.
- Do not commit API keys, cloud profiles, `.env` files, model weights, private datasets, generated model artifacts, cloud state, or local cache paths.
- Use repo-local files, checked-out provider config, provider CLIs, provider MCP servers, and official provider documentation before making claims about current inference behavior.
