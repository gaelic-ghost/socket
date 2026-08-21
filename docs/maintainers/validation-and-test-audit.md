# Socket Validation and Test Audit

## Decision Standard

This audit covers every validation gate and collected test in Socket as of
v10.0.1. A check remains only when it protects at least one current, shipped
contract:

- executable behavior or error handling;
- marketplace, plugin, skill, or consumer compatibility;
- a destructive-action, credential, privacy, security, or release boundary;
- source ownership, routing, or discovery that changes agent behavior; or
- generated payload integrity.

A check is not justified when it only records completed history, proves that a
retired thing remains absent, repeats another live gate without isolating its
behavior, or copies source tests into a generated payload. No absence regression
test is required when a surface is permanently removed.

Every retained test function is covered below by its owning file and exact test
count. The retained full profile collects 432 tests.

## Live Validation Gates

The repository has one CI entrypoint: `.github/workflows/validate-socket.yml`.
It runs the full profile on macOS because several shipped workflows and path
contracts are Apple-platform specific. The nested Apple and Python workflow
files were removed because GitHub does not load workflows below the repository
root and the root full profile already owns their checks.

| Gate | Decision | Current contract |
| --- | --- | --- |
| Root marketplace metadata | Keep | Rejects malformed marketplace entries, missing local payloads, unsafe custom-agent permissions, invalid MCP transport, and broken interface assets. |
| Shared skill metadata | Keep | Enforces skill-directory identity and OpenAI interface shape across every authored plugin skill. |
| Root tests (160) | Keep | Exercises root release, export, compatibility, installer, safety, validator, and cross-plugin ownership behavior listed below. |
| Root mypy | Keep | Checks the typed root maintainer and release programs before they can mutate repository or release state. |
| Root Ruff | Keep | Rejects Python defects in the root scripts and their tests. |
| Hermes compatibility | Keep | Proves the generated skill tap, groupings, metadata limits, and translated MCP configuration are installable by Hermes. |
| Claude compatibility | Keep | Proves marketplace classification agrees with Claude/Cowork support and rejects unsupported local MCP claims. |
| Agent Engineering tests (12) | Keep | Protects the executable automation/evaluation workflow schemas, routing, and safety boundaries. |
| Agent Portability tests (13) | Keep | Protects protocol routing plus the two executable repository bootstrap/synchronization tools. |
| Agent Portability Ruff | Keep | Lints the shipped portability scripts, including files outside their focused tests. |
| Agent Portability mypy | Keep | Type-checks the shipped portability scripts and their structured payloads. |
| Apple docs/layout validator | Keep, pruned | Protects the active 58-skill inventory, discovery symlink, required skill structure, shared-snippet synchronization, docs-source order, repository-skill delegation, and skill-creator contract. Historical roadmap prose and retired-path assertions were removed. |
| Apple tests (227) | Keep | Exercises executable Apple workflow planners/configuration tools and safety-critical guidance contracts listed below. |
| Professional Skills tests (5) | Keep | Protects the Dice search workflow's request shaping, URL construction, filtering, and output behavior. |
| Python metadata | Keep | Validates the current Python plugin manifest, skill metadata, links, and agent interfaces. |
| Python tests (11) | Keep | Exercises all three scaffold generators and current agent/service/testing guidance contracts. |
| Python Ruff | Keep | Lints the shipped Python plugin scripts and tests. |
| Python mypy | Keep | Type-checks the shipped Python plugin scripts and structured inputs. |
| Cybersecurity metadata | Keep | Validates the current cybersecurity manifest, skill metadata, links, and agent interfaces. |
| Cybersecurity tests (2) | Keep | Protects routing between macOS threat work, platform controls, isolation, recovery, and reverse engineering. |
| Reverse Engineering metadata | Keep | Validates the current reverse-engineering manifest, skill metadata, links, and agent interfaces. |
| Reverse Engineering tests (2) | Keep | Protects public/private/runtime evidence separation and bounded-probe handoffs. |

## Retained Root Tests

| File | Tests | Justification |
| --- | ---: | --- |
| `tests/test_audit_skill_surfaces.py` | 7 | Exercises the shipped audit report in JSON/Markdown/file modes and enforces direct SwiftData guidance where a weak query-only answer changes implementation advice. |
| `tests/test_audit_xcode_plugin_compatibility.py` | 3 | Exercises plugin classification/reporting and proves every live marketplace entry is classified for Xcode compatibility. |
| `tests/test_check_acp_registry.py` | 3 | Exercises exact registry matching, schema loading, and the non-error missing-agent result used by the ACP workflow. |
| `tests/test_cleanup_legacy_socket_installs.py` | 5 | Protects deletion target selection, backup-before-remove behavior, cache exclusion, and reporting of foreign configuration. |
| `tests/test_cybersecurity_skill_contracts.py` | 14 | Protects authorization, isolation, evidence retention, non-binary verdicts, recovery, containment, detection fixtures, and specialist routing. |
| `tests/test_deployment_build_safety_contracts.py` | 3 | Protects clean GitHub builds, single-session build ownership, immutable deployment artifacts, and native-local/cloud-build separation. |
| `tests/test_macos_platform_security_forward_scenarios.py` | 1 | Parameterizes eight concrete TCC, sandbox, entitlement, threat, and private-evidence decisions that prevent unsafe platform advice. |
| `tests/test_macos_virtualization_forward_scenarios.py` | 1 | Parameterizes eight concrete VM/container/isolation decisions that prevent invalid macOS evidence claims. |
| `tests/test_macos_virtualization_skill_contracts.py` | 1 | Ensures every virtualization owner remains discoverable in both the Hermes export and public grouping. |
| `tests/test_model_lab_skill_contracts.py` | 9 | Protects current inventory/routing, authorization controls, experiment validation, paired comparison correctness, provenance stability, and version alignment. |
| `tests/test_release_version.py` | 4 | Exercises target discovery, aligned SemVer calculation, split-version rejection, and atomic manifest/lockfile updates. |
| `tests/test_release_workflow.py` | 10 | Exercises PR/check gating, branch ownership/accounting, version ordering, publication checks, evidence generation, and the single release CLI. |
| `tests/test_repository_maintenance_workflow.py` | 29 | Exercises generated validation/release assets, mandatory documentation creation and refresh, non-mutating reports, owner dispatch, bootstrap integration, workspace dispatch, delayed GitHub state, prerelease metadata, notes selection, branch accounting, triggers, and preservation of repo-owned extensions. |
| `tests/test_spi_add_package.py` | 10 | Exercises canonical URL/form construction, live form validation, package readiness, tag/toolchain checks, and the explicit prohibition on unauthorized alternate submission writes. |
| `tests/test_swiftasb_skills_install.py` | 2 | Performs a real temporary Codex marketplace install and verifies the published .NET skill inventory. |
| `tests/test_unified_swift_workspace_contracts.py` | 7 | Protects positive package/workspace context, component ownership, target layout, native-local/cloud deployment, immutable artifacts, and Soto lifecycle policy. |
| `tests/test_validate_claude_compatibility.py` | 3 | Exercises acceptance and the two unsupported-classification failures enforced by the live Claude gate. |
| `tests/test_validate_hermes_compatibility.py` | 9 | Exercises exact export comparison, grouping, metadata size, MCP translation, placeholder documentation, and stale/missing payload failures. |
| `tests/test_validate_socket.py` | 8 | Protects profile composition, non-duplication, macOS CI routing, dry-run behavior, and shared skill metadata acceptance/rejection. |
| `tests/test_validate_socket_metadata.py` | 18 | Exercises every supported marketplace source/MCP/interface/agent shape and the corresponding unsafe or malformed rejection paths. |

## Retained Apple Tests

These files test the shipped guidance itself because guidance is the plugin's
runtime product: removing a required safety, ownership, or handoff statement
changes what an agent will do.

| File | Tests | Justification |
| --- | ---: | --- |
| `test_app_extension_workflows.py` | 4 | Process/product boundaries, MailKit privacy, File Provider/Finder ownership, and discoverability. |
| `test_appkit_app_architecture_workflow.py` | 4 | AppKit/SwiftUI ownership, restoration, observation, menu/status surfaces, and handoffs. |
| `test_apple_developer_provisioning_workflow.py` | 5 | Portal/API limits, credential and mutation confirmation, CloudKit token safety, discovery, and customization behavior. |
| `test_apple_ui_accessibility_workflow.py` | 4 | Framework breadth, accessibility handoffs, verification limits, and semantic tree examples. |
| `test_arkit_spatial_face_body_workflows.py` | 5 | Tracking capability boundaries, authentication limits, privacy/device evidence, metadata, and handoffs. |
| `test_author_swift_docc_docs.py` | 5 | Executable task inference, docs lookup/generation handoffs, defer policy, and blocked ambiguity. |
| `test_camera_capture_depth_workflow.py` | 4 | Capture lifecycle, capability/pressure handling, calibrated depth synchronization, metadata, and handoffs. |
| `test_core_animation_typography_workflows.py` | 3 | Layer ownership, Dynamic Type/font licensing, handoffs, metadata, and discovery. |
| `test_customization_cli.py` | 2 | Apply/effective/reset behavior and invalid override rejection. |
| `test_customization_template_paths.py` | 6 | Canonical template location, partial merge semantics, and YAML/schema rejection paths. |
| `test_design_animation_symbol_workflows.py` | 3 | Rendering/motion/accessibility boundaries plus metadata and discovery. |
| `test_devicecheck_app_attest_workflow.py` | 5 | DeviceCheck/App Attest separation, server trust, entitlement/docs limits, handoffs, and discovery. |
| `test_explore_apple_swift_docs_workflow.py` | 13 | Source-order routing, user preference, open-source fallback, approval-gated Dash installation, and structured generation. |
| `test_format_swift_sources_export.py` | 3 | SwiftFormat option inference, deterministic export, and plist input loading. |
| `test_imaging_foundation_workflows.py` | 4 | Core Image/representation ownership, conversion evidence, metadata, and customization. |
| `test_macos_platform_security_workflows.py` | 5 | TCC, sandbox authorization lifetime, entitlement evidence, discovery, and metadata. |
| `test_macos_virtualization_workflows.py` | 5 | Shape selection, guest/state identity, evidence boundaries, metadata, and customization. |
| `test_media_audio_workflows.py` | 4 | Framework/type ownership, repair guidance, references, discovery, and validation inventory. |
| `test_media_expansion_audit.py` | 4 | Complete media workflow structure, non-overlapping framework owners, privacy/device evidence, and public inventory. |
| `test_milestone24_system_ui_workflows.py` | 5 | Current App Intents, Liquid Glass, telemetry/distribution, Help Viewer, and Feedback Assistant boundaries; the filename is historical but assertions protect live guidance. |
| `test_photos_library_editing_workflow.py` | 4 | Picker/authorization, typed asset delivery, transactional editing, metadata, customization, and handoffs. |
| `test_safari_extension_control_workflow.py` | 5 | Extension-shape ownership, bounded controls, messaging privacy, and handoffs. |
| `test_safari_mcp_workflow.py` | 3 | Runtime-versus-architecture ownership, scoped evidence, registration, and data boundaries. |
| `test_structure_swift_sources_file_headers.py` | 4 | Header reporting, license preservation, deterministic replacement, and inventory schema. |
| `test_structure_swift_sources_todo_fixme_ledgers.py` | 3 | TODO/FIXME parsing, apply behavior, link rendering, stable IDs, and CLI JSON. |
| `test_structure_swift_sources_workflow.py` | 6 | Task inference, owner handoffs, runtime customization, and SwiftUI file-structure rules. |
| `test_swift_cleanup_skill_boundaries.py` | 2 | Keeps DocC work with its owning workflow from both cleanup entrypoints. |
| `test_swift_package_build_run_workflow.py` | 8 | Build planning, nested roots, resources/Metal routing, Xcode coexistence, handoffs, and blocked ambiguity. |
| `test_swift_package_extension_workflow.py` | 5 | Trait/macro/plugin planning, toolchain floor, Xcode coexistence, references, and routing. |
| `test_swift_package_testing_workflow.py` | 9 | Test planning/context, build/extension handoffs, coverage, accessibility/model scheduling, and blocked ambiguity. |
| `test_swiftui_app_architecture_workflow.py` | 6 | Scene/focus architecture, component ownership, preview rules, and handoffs. |
| `test_swiftui_component_audit_workflow.py` | 1 | Enforces declarative component ownership rather than external view-model indirection. |
| `test_tipkit_workflow.py` | 4 | Setup/presentation ownership, eligibility/test lifecycle, docs/handoffs, and discovery. |
| `test_tvos_workflows.py` | 4 | Focus/input, playback ownership, accessibility/device evidence, handoffs, and discovery. |
| `test_video_codec_processing_workflow.py` | 5 | Codec lifecycle, pixel/color/HDR fidelity, diagnostics, type ownership, metadata, and handoffs. |
| `test_vision_recognition_workflows.py` | 4 | Vision/Core ML ownership, provenance/evaluation, coordinate/confidence rules, metadata, and handoffs. |
| `test_xcode_build_run_workflow.py` | 9 | Build routing, workspace inference, customization, pbxproj mutation policy, XcodeGen ownership, and dependency recovery. |
| `test_xcode_coding_intelligence_workflow.py` | 8 | Setup/execution ownership, dated beta claims, system paths, MCP/ACP capability boundaries, and permissions. |
| `test_xcode_device_window_telemetry_debugger_workflows.py` | 4 | Device, window, telemetry, debugger, AgentDeck, privacy, and beta-loader ownership boundaries. |
| `test_xcode_localization_workflow.py` | 3 | String Catalog workflow, human-review/provenance limits, metadata, and discovery. |
| `test_xcode_testing_workflow.py` | 11 | Test routing, plans/context, mutation policy, accessibility/device evidence, XcodeGen, coverage, and model scheduling. |
| `test_xcode_toolchain_selection_guidance.py` | 3 | Explicit Xcode selection authority and stable/beta application boundaries. |
| `test_xcode_workspace_workflows.py` | 23 | Executable create/adopt/add/align behavior, canonical layout, pre-write blockers, evidence-preserving adoption, target/service routing, and workspace visibility. |

## Retained Other Child Tests

| File | Tests | Justification |
| --- | ---: | --- |
| Agent Engineering `test_design_agent_automation_workflow.py` | 7 | Protects automation workflow shape, triggers, approvals, tools, validation, and generated output. |
| Agent Engineering `test_design_agent_eval_workflow.py` | 5 | Protects evaluation scope, dataset/metric controls, execution routing, and report artifacts. |
| Agent Portability `test_bootstrap_skills_plugin_repo.py` | 4 | Exercises repository bootstrap output, idempotence, validation, and safe refusal behavior. |
| Agent Portability `test_sync_skills_repo_guidance.py` | 6 | Exercises guidance synchronization, preservation, validation commands, and error paths. |
| Agent Portability `test_agent_protocol_workflows.py` | 3 | Protects A2A/ACP role, security, and routing distinctions. |
| Cybersecurity `test_macos_security_handoffs.py` | 2 | Protects macOS platform-control and reverse-engineering handoffs. |
| Professional `test_dice_job_search_workflow.py` | 5 | Exercises the shipped search workflow's request, filtering, URL, and result contracts. |
| Python `test_build_python_agent_service_skill.py` | 3 | Protects local-first framework choice, exact model/approval disclosure, uv use, and bounded tool access. |
| Python `test_plugin_smoke.py` | 8 | Protects manifest/discovery, host-provided FastMCP docs, current workflow inventory, shared bootstrap ownership, and three scaffold generators. |
| Reverse Engineering `test_research_macos_security_control.py` | 2 | Protects evidence hierarchy, bounded probes, and owner handoffs. |

## Validation Assets That Are Not Socket Gates

These remain because they are executable parts of shipped skills, not duplicate
Socket CI:

- `plugins/model-lab-skills/.../validate_experiment_manifest.py` validates user
  experiment manifests and is exercised by the model-lab tests.
- `plugins/repository-skills/.../validate-all.sh`, its component dispatcher, and
  the generic/Apple GitHub workflow templates are installed into other
  repositories by `maintain-project-repo`; the repository-maintenance tests
  exercise their generation and behavior.
- The corresponding root `skills/` copies are required runtime files in the
  Hermes export. Source `tests/` directories are deliberately excluded because
  they are maintainer-only and were redundant in the exported payload.

## Removed Checks

| Removed item | Reason |
| --- | --- |
| Three branch-added tests for `maintain-project-api` absence and centralized child caches/tooling | The user prohibited new tests and permanent-absence regression tests. |
| `test_retired_standalone_and_sync_skills_are_absent` | Only froze retired paths. |
| `test_retired_server_local_environment_templates_are_absent` | Only froze deleted templates. |
| `test_release_version_module_has_no_release_choreography_entrypoint` | Only proved removed attributes stayed absent. |
| Duplicate unified-workspace profile inventory test | The repository-maintenance suite already tests the actual accepted profile API and installer behavior. |
| `tests/test_root_agents_guidance.py` | Only synchronized historical prose about a removed local mirror and asserted its absence. |
| `plugins/apple-dev-skills/tests/test_customization_consolidation_review.py` (4 tests) | Locked a historical review document, exact counts, and completed roadmap milestones instead of live behavior. |
| Apple `test_roadmap_marks_milestone_complete` | Only locked a completed milestone. |
| Apple docs-validator pytest wrapper | Re-ran the same shell validator immediately after the full profile had already run it. |
| Python metadata pytest wrapper | Re-ran the same metadata validator immediately after the full profile had already run it. |
| Roadmap milestone assertions inside nine retained Apple discovery tests | Milestone completion is history; the useful metadata/discovery assertions remain. |
| Retired-name/path assertions in Python and unified-workspace tests | Current positive inventory and context behavior remain; deletion history is not a contract. |
| Historical/retired-path blocks in the Apple docs validator | They checked roadmap prose or permanent absence rather than current layout and ownership. |
| Nested Apple and Python workflow YAML files | Inert in this monorepo and duplicates of the root full profile. |
| Python `.github/scripts/validate_repo_docs.sh` | One-line forwarding wrapper to the directly invoked metadata validator. |
| Exported `skills/*/tests` copies (2 directories, 10 duplicate definitions) | Not collected by Socket and not needed by Hermes consumers; authored source tests remain and still run. |

The collected full-suite count changed from 447 to 432: 12 pre-existing
unjustified tests and the 3 newly added tests were removed. No test was added.
