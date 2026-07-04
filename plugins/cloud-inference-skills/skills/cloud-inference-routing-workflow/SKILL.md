---
name: cloud-inference-routing-workflow
description: Choose the right cloud AI inference, model training, model conversion, or GPU infrastructure path before implementation. Use when Codex works with Runpod, Hugging Face, AWS, AWS Lambda inference, Vast.ai, CoreWeave, GPU Pods, Serverless GPU endpoints, model weights, vLLM, TGI, SGLang, custom containers, LoRA/adapters, dataset upload, model conversion, cheap GPU rentals, or managed inference endpoints.
---

# Cloud Inference Routing Workflow

## Purpose

Choose the smallest correct cloud AI inference path before changing provider resources, spending GPU budget, moving model weights, or deploying endpoints.

The practical decision is whether the agent should use an official provider plugin, provider MCP server, provider CLI, SDK, managed inference endpoint, rented GPU instance, cluster platform, or a stack-owned implementation workflow.

## Source Check

Use repo-local model code, Dockerfiles, provider configs, checked-out scripts, installed provider plugins, installed provider CLIs, bundled MCP servers, and official provider documentation before making claims about current behavior.

Preferred official sources:

- Runpod docs and bundled MCP servers for Runpod Pods, Serverless, Flash, templates, volumes, registries, and docs lookup.
- Hugging Face plugin and `huggingface_hub` CLI for Hub repos, models, datasets, Spaces, Inference Endpoints, jobs, and papers.
- AWS Agent Toolkit, AWS CLI, AWS SDKs, and AWS docs for Lambda, SageMaker, Bedrock, ECS, EKS, Batch, IAM, billing, and observability.
- Vast.ai docs and CLI for low-cost rented GPU instances.
- CoreWeave docs for Kubernetes-backed GPU infrastructure, clusters, storage, networking, and observability.

Translate documentation into the concrete project decision it changes.

## Routing Workflow

1. Inspect the workload:
   - task: inference endpoint, batch inference, fine-tuning, full training, eval, model conversion, quantization, benchmark, notebook, or one-off GPU shell
   - model family, parameter count, precision, context length, adapters, tokenizer, and required runtime
   - expected VRAM, CPU RAM, disk, network, container image, driver, CUDA, and startup time
   - latency, throughput, concurrency, cold-start tolerance, uptime, privacy, and cleanup needs
   - artifact flow: model weights, private datasets, outputs, logs, checkpoints, and caches
2. Choose the provider lane:
   - quick managed inference
   - quick custom endpoint
   - cheap flexible GPU box
   - training or conversion workspace
   - Kubernetes or production cluster
   - existing provider familiarity
3. Prefer familiar first-party paths when they fit:
   - Runpod for fast GPU Pods, Serverless endpoints, Flash, cheap/flexible experiments, templates, and resource management through MCP.
   - Hugging Face for model and dataset repos, conversion/publishing workflows, Inference Endpoints, Spaces, jobs, and Hub-native collaboration.
   - AWS when the project already uses AWS accounts, IAM, S3, CloudWatch, Lambda, SageMaker, Bedrock, ECS, EKS, or Batch.
4. Route to official tools:
   - Use `runpod` MCP for Runpod resource mutations and `runpod-docs` MCP for docs lookup when available.
   - Use the project-scoped upstream Runpod skill mirror under `.agents/skills` for Runpod `flash`, `runpodctl`, and companion CLI details. Refresh that mirror with `npx skills update` or `npx skills add runpod/skills` instead of hand-editing it.
   - Use the Hugging Face Codex plugin and Hugging Face CLI for Hub, model, dataset, Space, endpoint, or job work when available.
   - Use the AWS Agent Toolkit and AWS CLI or SDKs for AWS inference work when available.
   - Use provider CLIs or docs for Vast.ai and CoreWeave until a provider-owned agent surface is available or a concrete repeated Socket workflow justifies a new slice.
5. Confirm boundaries before mutation:
   - provider account, project, region, org, namespace, and budget
   - API key or profile source
   - model and dataset license or private-use boundary
   - exact resources to create, update, stop, delete, or scale
   - expected hourly cost, storage cost, bandwidth cost, idle behavior, and teardown path
6. Choose validation:
   - read-only docs, list, or pricing query for planning
   - local smoke test or CPU fallback before GPU spend
   - minimal GPU probe before full training or endpoint deployment
   - endpoint health, latency, throughput, logs, and cost check after deployment
   - cleanup verification for stopped Pods, terminated instances, deleted endpoints, detached volumes, and lingering storage

## Provider Fit

### Runpod

Use Runpod first when Gale wants quick and easy GPU access, cheap/flexible infrastructure, Serverless endpoints, GPU Pods, Flash, templates, network volumes, or direct resource management from an agent.

Use `runpod-docs` MCP for docs questions. Use `runpod` MCP for resource operations after confirming `RUNPOD_API_KEY`, account, resource name, GPU type, cost, and cleanup.

Use the installed upstream Runpod skills for details:

- `.agents/skills/flash` for `runpod-flash` SDK and CLI workflows.
- `.agents/skills/runpodctl` for Runpod CLI workflows.
- `.agents/skills/companion-clis` for Hugging Face, GitHub, Docker, and AWS CLI support commonly needed around Runpod deployments.

### Hugging Face

Use Hugging Face first when the work is model or dataset centered: Hub repos, checkpoints, safetensors, GGUF or Core ML conversion artifacts, datasets, evals, Spaces, Inference Endpoints, or sharing/publishing.

Prefer the installed Hugging Face Codex plugin and official CLI. Do not reimplement Hub auth, repo management, or endpoint setup in Socket unless a small routing note removes real ambiguity.

### AWS And Lambda

Use AWS first when the project already depends on AWS IAM, S3, CloudWatch, Lambda, SageMaker, Bedrock, ECS, EKS, or Batch.

Treat Lambda inference as a narrow fit: small models, lightweight CPU inference, short-lived request handlers, or calls out to Bedrock/SageMaker/hosted endpoints. For large GPU models, training, conversions, or long warmup services, route toward SageMaker, Bedrock, ECS/EKS GPU infrastructure, Batch, or another GPU provider rather than assuming Lambda is the right runtime.

### Vast.ai

Use Vast.ai when cost and flexibility matter more than managed endpoint ergonomics, especially for one-off training, conversion, experimentation, benchmarks, or shell access on rented GPUs.

Require stronger cleanup and artifact handling: rented instances, volumes, SSH keys, exposed ports, docker images, and checkpoint transfers are the work.

### CoreWeave

Use CoreWeave when the job is cluster-shaped: Kubernetes, production GPU services, larger training, persistent storage, network policy, observability, or enterprise-grade GPU infrastructure.

Do not route a quick experiment to CoreWeave unless the project already has CoreWeave cluster access or the user explicitly wants that platform.

## Output Shape

Return:

1. `Workload`: inference endpoint, batch job, training, conversion, eval, benchmark, or exploration.
2. `Provider`: Runpod, Hugging Face, AWS, Vast.ai, CoreWeave, multi-provider, or undecided.
3. `Primary surface`: official plugin, MCP server, provider CLI, SDK, stack skill, or user decision needed.
4. `Credential boundary`: API key, profile, org, account, region, and whether credentials are required for the next step.
5. `Cost boundary`: expected GPU, storage, bandwidth, idle, and teardown concerns.
6. `Mutation boundary`: read-only, local-only, create endpoint, create instance, train, scale, stop, delete, or blocked.
7. `Validation path`: exact commands, MCP checks, or provider-console checks before and after mutation.
8. `Next handoff`: provider plugin, provider docs, stack skill, Runpod MCP, Hugging Face plugin, AWS Agent Toolkit, or Socket backlog item.

## Guardrails

- Do not move model weights, upload datasets, create endpoints, create GPU instances, scale resources, or delete resources without confirming account, credential, cost, and cleanup boundaries.
- Do not commit API keys, cloud profiles, `.env` files, model weights, private datasets, generated model artifacts, or local cache paths.
- Do not duplicate Hugging Face or AWS plugin capabilities in Socket while those first-party plugins are installed and fit the task.
- Do not treat an MCP server as better than an HTTP API, CLI, or official plugin unless it improves agent safety, discovery, or resource control for the requested work.
- Do not claim training, inference quality, latency, throughput, hardware availability, or provider pricing without live evidence from the provider, a command, or a current docs check.
