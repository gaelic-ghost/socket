# AGENTS.md

This file is the Cybersecurity Skills child-repo override for work done from `socket`. Follow the root `socket` guidance for general Git, documentation, release, branch, dependency-provenance, and maintainer workflow rules.

## Scope

- `cybersecurity-skills` is a monorepo-owned Socket child and the canonical source of truth for defensive cybersecurity workflow skills.
- Root [`skills/`](./skills/) is the authored workflow surface.
- The repo root is the Codex plugin root through [`.codex-plugin/plugin.json`](./.codex-plugin/plugin.json).
- Keep the first-party payload guidance-only. Do not bundle scanners, malware or exploit samples, privileged helpers, daemons, hooks, MCP servers, VM/container images, tool databases, or remote-service credentials without a separately approved architecture decision.

## Evidence And Safety Rules

- Preserve original artifacts and volatile evidence before transformation when practical. Record hashes, versions, timestamps, commands, tool versions, and transformations that support a conclusion.
- Separate observed facts, external intelligence, hypotheses, conclusions, confidence, and unresolved questions.
- Treat signatures, notarization, reputation, severity scores, vulnerability databases, and scanner output as evidence inputs rather than safety or exploitability verdicts.
- Default suspicious-content work to local, non-executing inspection. Require explicit approval before sending private artifacts, URLs, logs, or identifiers to third-party services.
- Choose containers, VMs, remote sandboxes, or spare devices from the actual threat model. Do not present a Linux container as a sufficient macOS malware-analysis environment.
- Keep shared folders, clipboards, host sockets, signing identities, browser profiles, SSH agents, cloud credentials, and unrestricted networking absent from disposable analysis environments unless the task requires and records them.
- Require explicit target authorization and a written scope record before active security testing. Stop on target drift, third-party impact, instability, unexpected sensitive data, or techniques outside the approved rules of engagement.
- Keep containment, eradication, recovery, credential response, notification, hardening, and verification as distinct decisions.
- Give non-specialists direct, calm advice that distinguishes immediate action, remaining uncertainty, and longer-term protection without minimizing or inflating the evidence.

## Ownership Boundaries

- Use `reverse-engineering-skills` for binary internals, decompilation, disassembly, symbols, and exact binary comparison after this plugin establishes the security question and artifact identity.
- Use Codex Security for repository-wide or diff-based source vulnerability scanning when installed. Do not duplicate its full scan pipeline here.
- Use `apple-dev-skills` for ordinary Apple app, Endpoint Security, Virtualization, signing, or Xcode implementation after this plugin defines the defensive requirement.
- Use `network-protocol-skills` for protocol construction and repair; keep authorized test scope and observed security behavior here.
- Hand stack-specific remediation to the owning language or framework plugin while retaining the finding, evidence, and acceptance criteria.

## Validation

- Keep `SKILL.md` procedural and concise, with tool matrices, schemas, version-sensitive facts, and larger examples in directly linked `references/`.
- Keep every skill portable unless a concrete host-specific tool contract requires otherwise. Update the Hermes export and grouping in the same pass as any portable skill change.
- Run `uv run scripts/validate_repo_metadata.py` from this child root and `uv run scripts/validate_socket_metadata.py` from the Socket root before review.
