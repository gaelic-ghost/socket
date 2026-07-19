# Model Lab Skills Guidance

## Scope

- This plugin owns reproducible model experiment design, dataset preparation, fine-tuning, checkpoint comparison, model-internals interventions, behavioral evaluation, and runtime benchmarking.
- Route cloud provider selection, endpoint deployment, GPU procurement, and teardown to `cloud-inference-skills`.
- Route Python project structure and package maintenance to `python-skills`.
- Route app-facing Swift, Xcode, Core ML integration, and Apple UI work to `apple-dev-skills`.
- Route agent-skill and prompt-package evaluation to `productivity-skills`, and host portability to `agent-portability-skills`.
- Route authorized security testing of a real deployed system to `cybersecurity-skills`; keep model-only robustness experiments here.

## Evidence Rules

- Pin model revisions, dataset revisions, package versions, templates, seeds, and generation settings when the underlying tool permits it.
- Separate an experiment hypothesis from an observed result. Never present a planned run, dry run, or configuration validation as model-quality evidence.
- Preserve raw measurements and per-case outcomes. Aggregate scores must remain traceable to their inputs.
- Compare checkpoints on the same prompts, decoding configuration, evaluator version, and runtime conditions unless the difference is the controlled variable.
- Treat benchmark, paper-reproduction, prototype, and production-ready tooling as different evidence classes.
- Record licenses and redistribution constraints as provenance fields, without turning private local research into an unrequested licensing audit.

## Safety And Operations

- Jailbreak and refusal-ablation workflows are authorized research workflows, not permission to target third-party production systems or people.
- Use synthetic, public, or explicitly approved sensitive data. Do not place secrets, private prompts, or personal data in logs or published artifacts.
- State compute budgets and stop conditions before launching expensive runs. Do not provision paid remote resources without explicit user authorization.
- Prefer a small smoke run before a full training or evaluation run.

## Portability

- Skills are instruction-first and portable across Codex, Claude Code, Cowork, and Hermes-capable hosts.
- Shell and Python examples must not depend on a Codex-only tool name or machine-local path.
- Keep host adapters outside the model workflow itself.
