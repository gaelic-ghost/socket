# Workflow Maps

This document describes the maintainer-facing workflow view of the active skills in `apple-dev-skills`, including branches, guards, fallbacks, handoffs, input and output contracts, and the user-facing interface between the user, the agent, and each skill.

## Terminology

- `primary workflow`: the main numbered path for a skill
- `guard`: a condition that must be satisfied before the primary workflow continues
- `fallback`: a supported secondary path when the primary workflow cannot continue
- `handoff`: a transfer to another skill or later stage
- `blocked`: no valid path remains
- `status`: the terminal state reported by the skill
- `path_type`: whether the completed path was `primary` or `fallback`

## Repo Workflow Map

### Workflow Diagram

```mermaid
flowchart TD
    U["User request"] --> A["Agent classifies request"]
    A --> X["apple-xcode-workflow"]
    A --> DD["apple-dash-docsets"]
    A --> B["apple-swift-package-bootstrap"]
    X --> XD["May recommend apple-dash-docsets"]
    X --> XB["May recommend apple-swift-package-bootstrap"]
    DD --> DX["May recommend apple-xcode-workflow"]
    DD --> DB["May recommend apple-swift-package-bootstrap"]
    B --> BX["May recommend apple-xcode-workflow"]
    B --> BD["May recommend apple-dash-docsets"]
```

### Branch and Path Notes

- The repo has no Apple router or orchestrator layer.
- The three active skills are parallel top-level entry points for different situations.
- Cross-skill recommendation is decentralized inside each skill.
- End-user `AGENTS.md` guidance is recommended from each skill's local snippet copy, not from a router.

### Agent ↔ User UX

- Entry:
  - The user asks for Apple, Swift, Dash, or package-bootstrap help.
- Agent behavior:
  - The agent chooses the best matching top-level skill directly and may recommend another top-level skill if the task shifts.
- User-visible response:
  - The user sees direct progress inside one of the three top-level skills, or a direct recommendation to switch to another skill.
- Interaction style:
  - The repo-level UX is a bundle of three parallel top-level skills: one execution skill, one Dash management skill, and one new-package bootstrap skill.

## `apple-xcode-workflow`

### Purpose

Provide the canonical Apple and Swift workflow guidance with one local runtime-policy entrypoint and one agent-side execution path.

### Workflow Diagram

```mermaid
flowchart TD
    I["Operation input"] --> C["Classify operation type"]
    C --> RW["run_workflow.py"]
    RW --> RC["Resolve workspace context and local policy"]
    RC --> MCP["Agent uses MCP tools"]
    MCP --> OK{"MCP success?"}
    OK -->|Yes| OUT1["Success / primary"]
    OK -->|No| RT{"Transient failure?"}
    RT -->|Yes| RETRY["Retry once"]
    RT -->|No| CLI["Run official CLI fallback"]
    RETRY --> RETRYOK{"Retry success?"}
    RETRYOK -->|Yes| OUT1
    RETRYOK -->|No| CLI
    CLI --> CLIOK{"CLI available and successful?"}
    CLIOK -->|Yes| OUT2["Success / fallback"]
    CLIOK -->|No| BL["Blocked"]
```

```mermaid
flowchart LR
    M["operation_type=mutation"] --> G["Apply mutation guard"]
    G --> SAFE{"Guard satisfied?"}
    SAFE -->|Yes| EXEC["Continue execution workflow"]
    SAFE -->|No| BL["Blocked"]
```

```mermaid
flowchart LR
    D["operation_type=docs"] --> P["Use same execution engine"]
    P --> SRC["Prefer Dash local docs"]
    SRC --> MISS{"Dash unavailable or insufficient?"}
    MISS -->|No| DONE["Success / primary or fallback"]
    MISS -->|Yes| WEB["Use official Apple or Swift docs"]
    WEB --> NOTE["Handoff only if user needs Dash install or generate guidance"]
```

### Branch and Path Notes

- `run_workflow.py` is the local runtime entrypoint.
- Mutation is a guard, not a second top-level workflow.
- Docs lookup is an operation profile under the same execution engine.
- Official CLI execution remains the only documented fallback plan when the primary agent-side MCP path cannot complete.

### Inputs

- Required:
  - `operation_type`
- Optional:
  - `workspace_path`
  - `tab_identifier`
  - `mcp_failure_reason`
  - `docs_query`
- Defaults:
  - runtime entrypoint `python3 scripts/run_workflow.py`
  - one retry for transient MCP failure
  - advisory cooldown `21` days
  - docs source order `dash-mcp,dash-local,official-web`
  - mutation operations require the explicit guard in Xcode-managed scope

### Outputs

- `status`
  - `success`
  - `handoff`
  - `blocked`
- `path_type`
  - `primary`
  - `fallback`
- Primary output fields:
  - operation type
  - `guard_result`
  - `docs_route`
  - `fallback_commands`
  - next step or handoff payload

### Agent ↔ User UX

- Entry:
  - The user asks for Apple or Swift execution, diagnostics, docs, toolchain, or mutation work.
- Agent behavior:
  - The agent classifies the operation, runs `run_workflow.py` for local policy and fallback planning, then uses MCP tools or the planned fallback path.
- User-visible response:
  - On success: the user sees the completed path and what ran.
  - On fallback: the user sees that CLI was used and why.
  - On handoff: the user sees the next-step payload or supporting guidance.
  - On blocked: the user sees the exact reason the workflow could not continue.
- Interaction style:
  - Execution engine with guards and a single official fallback path.

### Failure / Fallback / Handoff States

- `success` + `primary`: agent-side MCP path completed
- `success` + `fallback`: official CLI fallback completed
- `handoff`: supporting context passed to a later step or another skill
- `blocked`: mutation guard failed, context missing, or safe fallback unavailable

## `apple-dash-docsets`

### Purpose

Manage Dash docsets through one runtime entrypoint and a straight internal stage flow.

### Workflow Diagram

```mermaid
flowchart TD
    I["Stage input"] --> S{"Stage explicit?"}
    S -->|No| SEARCH["Start at search"]
    S -->|search| SEARCH
    S -->|install| INSTALL
    S -->|generate| GENERATE

    SEARCH --> RT["run_workflow.py"]
    RT --> SEARCHOK{"Search stage completes?"}
    SEARCHOK -->|Yes| OUT1["Success / primary or fallback"]
    SEARCHOK -->|No| HI["Handoff to install"]

    INSTALL --> INSTALLOK{"Install stage completes?"}
    INSTALLOK -->|Yes| OUT2["Success / primary"]
    INSTALLOK -->|No installable match| HG["Handoff to generate"]
    INSTALLOK -->|Blocked| BL["Blocked"]

    GENERATE --> GENOK{"Generation path completes?"}
    GENOK -->|Automation| OUT3["Success / primary"]
    GENOK -->|Manual guidance| OUT4["Success / fallback"]
    GENOK -->|Blocked| BL
```

```mermaid
flowchart LR
    SEARCH["search"] --> MCP["Agent uses Dash MCP"]
    MCP --> OK{"Success?"}
    OK -->|Yes| DONE["Success / primary"]
    OK -->|No| HTTP["HTTP API"]
    HTTP --> HTTPOK{"Success?"}
    HTTPOK -->|Yes| DONE2["Success / fallback"]
    HTTPOK -->|No| URL["URL / Service guidance"]
    URL --> URLOK{"Usable?"}
    URLOK -->|Yes| DONE3["Success / fallback"]
    URLOK -->|No| BL["Blocked"]
```

```mermaid
flowchart LR
    INSTALL["install"] --> MATCH{"Installable catalog match?"}
    MATCH -->|Yes| RUN["Install path"]
    MATCH -->|No| HANDOFF["Handoff to generate"]
    RUN --> OUT["Success / primary"]
    HANDOFF --> NEXT["status=handoff, path_type=primary"]
```

### Branch and Path Notes

- `run_workflow.py` is the local runtime entrypoint for all stages.
- Default progression is `search -> install -> generate`.
- Direct entry to `install` or `generate` remains supported.
- `search` has a fallback ladder.
- `install` does not fall back to generation internally; it hands off forward.
- `generate` is terminal guidance and can itself fall back from automation to manual guidance.

### Inputs

- Required:
  - `query` for `search`
  - `docset_request` for `install` and `generate`
- Optional:
  - `stage`
  - `docset_identifiers`
  - `approval`
- Defaults:
  - runtime entrypoint `python3 scripts/run_workflow.py`
  - start at `search` when no stage is explicit
  - search order `mcp -> http -> url-service`
  - install source priority `built-in,user-contributed,cheatsheet`
  - default search result limit `20`
  - default search snippets `true`

### Outputs

- `status`
  - `success`
  - `handoff`
  - `blocked`
- `path_type`
  - `primary`
  - `fallback`
- Primary output fields:
  - `stage`
  - `access_path` or `source_path`
  - `matches`
  - install result or generation guidance
  - next step

### Agent ↔ User UX

- Entry:
  - The user asks to search Dash, install a missing docset, or get generation guidance.
- Agent behavior:
  - The agent selects a stage, calls `run_workflow.py`, and uses the structured stage result to choose the right Dash access path instead of stitching helper scripts together manually.
- User-visible response:
  - On success: the user sees what stage ran and what path completed it.
  - On fallback: the user sees which secondary path completed the stage.
  - On handoff: the user sees that the next stage is required and why.
  - On blocked: the user sees the missing prerequisite, approval, or path failure.
- Interaction style:
  - Staged guidance with explicit forward handoffs.

### Failure / Fallback / Handoff States

- `success` + `primary`: selected stage completed normally
- `success` + `fallback`: search or generate completed through documented fallback behavior
- `handoff`: `search -> install` or `install -> generate`
- `blocked`: no usable stage path remains

## `apple-swift-package-bootstrap`

### Purpose

Create one deterministic Swift package scaffold path through a runtime wrapper grounded in the bundled bootstrap script.

### Workflow Diagram

```mermaid
flowchart TD
    I["Scaffold inputs"] --> RW["run_workflow.py"]
    RW --> N["Normalize aliases and defaults"]
    N --> RUN["Run bootstrap script"]
    RUN --> OK{"Script success?"}
    OK -->|Yes| V["Verify generated repo"]
    OK -->|No| FAIL["Failed"]
    V --> VOK{"Verification success?"}
    VOK -->|Yes| OUT1["Success / primary"]
    VOK -->|No| FAIL
```

```mermaid
flowchart LR
    MAIN["Primary script path unavailable?"] --> DEC{"Fallback allowed?"}
    DEC -->|Yes| MANUAL["Manual swift package init guidance"]
    DEC -->|No| BL["Blocked"]
    MANUAL --> OUT["Success / fallback"]
```

```mermaid
flowchart LR
    DONE["Scaffold completed"] --> NEXT["Handoff to apple-xcode-workflow"]
    TYPE{"Requested type?"} -->|library| LIB["Normal default"]
    TYPE -->|executable| EXE["Normal CLI default"]
    TYPE -->|tool| TOOL["Advanced explicit passthrough"]
```

### Branch and Path Notes

- `run_workflow.py` is the runtime entrypoint and `bootstrap_swift_package.sh` is the implementation core.
- The primary workflow is always the bundled script.
- Manual scaffold guidance is fallback-only.
- `tool` stays supported, but only as an advanced explicit passthrough.
- Post-bootstrap handoff goes to `apple-xcode-workflow` for build, test, or Apple-platform work.

### Inputs

- Required:
  - `name`
- Optional:
  - `type`
  - `destination`
  - `platform`
  - `version_profile`
  - `skip_validation`
  - `dry_run`
- Defaults:
  - runtime entrypoint `python3 scripts/run_workflow.py`
  - `type=library`
  - `destination=.`
  - `platform=multiplatform`
  - `version_profile=current-minus-one`
  - validation enabled unless skipped

### Outputs

- `status`
  - `success`
  - `blocked`
  - `failed`
- `path_type`
  - `primary`
  - `fallback`
- Primary output fields:
  - resolved package path
  - normalized inputs
  - validation result
  - next step

### Agent ↔ User UX

- Entry:
  - The user asks for a new Swift package scaffold or wants scaffold defaults explained.
- Agent behavior:
  - The agent gathers inputs, calls `run_workflow.py`, and uses the wrapper output instead of parsing shell behavior ad hoc.
- User-visible response:
  - On success: the user sees the created path, normalized options, and validation result.
  - On fallback: the user sees manual scaffold guidance instead of the script path.
  - On handoff: the user sees the next suggested execution skill.
  - On blocked or failed: the user sees the exact prerequisite or execution failure.
- Interaction style:
  - Scaffold automation with one primary script path.

### Failure / Fallback / Handoff States

- `success` + `primary`: bundled script completed and verification passed
- `success` + `fallback`: manual scaffold guidance used
- `blocked`: prerequisites or destination constraints prevent the run
- `failed`: the script started but did not complete successfully
