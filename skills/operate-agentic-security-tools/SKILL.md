---
name: operate-agentic-security-tools
description: Operate security tools through an AI agent with explicit authority and evidence boundaries. Use when an agent may invoke local CLIs, GUI apps, browser automation, MCP servers, remote scanners, sandboxes, vulnerability tools, packet tools, or containment actions and permissions, mounts, network, secrets, approvals, logging, output, and cleanup must be constrained.
---

# Operate Agentic Security Tools

## Overview

Give the agent only the authority needed for the current security step and keep tool output reproducible. Separate discovery, active testing, exploit validation, containment, and remediation into visible decisions.

Read [references/agent-tool-controls.md](references/agent-tool-controls.md) for the preflight record and control checklist.

## Workflow

1. Define the tool's job.
   - State the security question, expected input/output, target, and why this tool is appropriate.
   - Prefer read-only or offline operation when it can answer the question.

2. Discover capability before use.
   - Record source, installed path or remote service, version, supported formats, privileges, network behavior, telemetry, and output location.
   - Treat missing tools or unusable integrations as results; do not invent output.

3. Minimize authority.
   - Limit readable/writable paths, target list, network destinations, credentials, environment variables, device access, and execution duration.
   - Use temporary scoped credentials and disposable environments when credentials are unavoidable.

4. Gate consequential actions.
   - Require an operator decision before active probing, exploit execution, persistence changes, credential access, security-control changes, destructive operations, production writes, or third-party uploads.
   - Display the exact target and likely effect before approval.

5. Preserve evidence.
   - Record commands or UI actions, configuration, timestamps, exit status, raw output, tool errors, and transformations.
   - Validate high-impact findings with an independent observation or smallest safe reproduction.

6. Clean up and verify.
   - Remove temporary mounts, ports, tokens, sessions, files, rules, and isolated environments.
   - Report what remains installed, running, reachable, or retained.

## Guardrails

- Do not grant broad host or cloud access merely to reduce approval prompts.
- Do not let an agent expand active-test scope from discovered targets.
- Do not treat an MCP server, GUI automation layer, or tool plugin as a trust boundary.
- Do not obscure failures behind a synthesized security conclusion.
