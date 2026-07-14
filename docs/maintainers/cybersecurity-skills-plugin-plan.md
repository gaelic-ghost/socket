# Cybersecurity Skills Plugin Plan

## Intent

`cybersecurity-skills` helps an agent turn an ambiguous security concern into an evidence-backed assessment, a safe next action, and an explanation that a non-specialist can understand. Its center is the real-world question "is this actually dangerous, how does it work, and what should I do now?" rather than a scanner inventory or a collection of exploit recipes.

The plugin covers suspicious artifacts and messages, malware analysis, macOS endpoint investigation, safe isolation, vulnerability validation, authorized security testing, incident containment and recovery, detection content, and practical defensive advice. It should work for a friend asking about a strange installer, a developer validating a vulnerability report, or an operator investigating suspicious host behavior without pretending those are the same workflow.

The first release is a guidance-only Socket child plugin. It does not bundle scanners, malware samples, exploit code, a privileged helper, a background daemon, hooks, an MCP server, VM images, container images, or cloud-analysis credentials. That shape unlocks immediate use of trusted local and external tools while keeping permissions, sample handling, and network access visible to the operator.

## Architecture Decision

Create `cybersecurity-skills` as a dedicated plugin. Do not expand `reverse-engineering-skills` into the broader owner.

This is a durable building-block change. It creates one owner for the security decision lifecycle across artifacts, hosts, services, identities, and incidents. It removes repeated confidence, evidence, isolation, scope, containment, and communication logic from future specialist skills. Afterward, malware, macOS, vulnerability, pentest, and incident workflows can share the same assessment record and hand off deep binary work without duplicating reverse-engineering guidance.

The simpler extension path was to add malware and defensive skills to `reverse-engineering-skills`. That path was rejected because reverse engineering correctly owns compiled artifacts, disassembly, decompilation, symbols, and binary behavior. It should not also own account compromise, network exposure, incident response, endpoint recovery, authorized test scope, or advice for non-specialists.

## Packaging Direction

Package the plugin as a monorepo-owned Socket child at `plugins/cybersecurity-skills/`. Its root should own:

- `.codex-plugin/plugin.json`
- `AGENTS.md`
- authored `skills/`
- narrow validation under `scripts/` when root validation cannot prove the skill inventory
- branded icon assets

Add the root marketplace entry as `NOT_AVAILABLE` while the child is only a placeholder. Switch it to `AVAILABLE` only after the first usable skill slice, plugin metadata, root documentation, Hermes export decision, and validation all agree.

Use `Developer Tools` as the marketplace category. Keep the authored plugin name `cybersecurity-skills` and the skill namespace `cybersecurity`.

## Ownership And Handoffs

| Surface | Primary owner | Cybersecurity responsibility |
| --- | --- | --- |
| Ambiguous security concern, suspicious content, host activity, incident, or authorized test | `cybersecurity-skills` | Route the work, preserve evidence, select isolation, calibrate confidence, and own the defensive recommendation. |
| Binary internals, decompilation, disassembly, symbols, Mach-O internals, or exact binary comparison | `reverse-engineering-skills` | Establish the security question and artifact identity, then hand off deep binary analysis and consume its evidence. |
| Repository-wide or diff-based source vulnerability discovery, attack-path analysis, and finding fixes | Codex Security when installed | Route code-scanning work to the dedicated security scanner and incorporate validated findings into exposure, response, or reporting workflows. |
| Ordinary Apple app development, signing, Xcode, Endpoint Security API implementation, or Virtualization framework implementation | `apple-dev-skills` | Own the security investigation or lab requirement, then hand implementation to Apple development workflows. |
| Protocol implementation or ordinary network-stack engineering | `network-protocol-skills` | Own security test scope and observed behavior; hand protocol construction or repair to the protocol owner. |
| Language- or stack-specific remediation | Owning Socket stack plugin | Preserve the finding and acceptance criteria, then hand the implementation to the relevant language or framework workflow. |
| GitHub repository settings and project security documents | `productivity-skills` | Provide the security requirement or finding; use the repository-maintenance owners for settings and policy-file changes. |

Do not copy Codex Security's repository scan phases into this plugin. The new plugin should remain useful when Codex Security is unavailable, but its fallback is bounded manual validation of a supplied concern, not a second full repository scanner.

## Common Security Record

Every investigative workflow should be able to produce or extend one shared record with these fields:

- question, affected person or system, and requested decision
- artifact, host, account, service, or target identity
- authorization and active-test scope when applicable
- acquisition source, timestamps, hashes, versions, OS build, hardware, and relevant tool versions
- preservation status and transformations performed
- observed facts, external intelligence, hypotheses, and disproven hypotheses kept separate
- indicators and behaviors with source and confidence
- threat classification, confidence, impact, and remaining uncertainty
- immediate containment advice, recovery advice, and longer-term hardening kept separate
- plain-language explanation suitable for the affected person
- reproducible commands, outputs, screenshots, or logs when they are safe to retain

Use calibrated conclusions rather than a binary scanner verdict:

- confirmed malicious
- likely malicious
- suspicious but unresolved
- likely benign or expected
- confirmed benign for the tested question
- insufficient evidence

A conclusion must say what evidence would change it. A clean reputation lookup, valid signature, successful notarization, or zero scanner findings is never proof that an artifact or system is safe.

## Safety And Analysis Boundaries

### Local-First Intake

- Start with metadata, hashes, signatures, archive listings, text extraction, and other non-executing checks.
- Preserve the original input and inspect a working copy.
- Do not upload a file, URL, document, log, token, customer artifact, or private binary to a third-party reputation or sandbox service without explicit approval after explaining what will leave the machine.
- Treat URLs, QR codes, documents, archives, profiles, packages, scripts, browser extensions, and chat/email content as potentially active inputs even when they are not native executables.

### Isolation Selection

- Use a disposable container for untrusted Linux user-space tooling only when the threat model does not require a macOS guest, kernel boundary, device access, or privileged execution.
- Prefer a disposable VM for untrusted execution, dynamic behavior, installers, services, or content that needs a full operating system.
- Use a macOS VM or disposable physical Mac for macOS-specific payloads; a Linux container cannot reproduce macOS code signing, TCC, LaunchServices, Endpoint Security, XProtect, Gatekeeper, or native persistence behavior.
- Default shared folders, clipboard sharing, host sockets, credentials, developer signing identities, cloud tokens, browser profiles, and SSH agents to absent.
- Default network access to off, simulated, or narrowly mediated. Record DNS, routes, packet capture, and any allowed destinations when network behavior matters.
- Revert or destroy disposable environments after exporting only the intended evidence.

### Agentic Tool Operation

- Discover the installed tool, version, permissions, data flow, and output location before using it.
- Give an agent only the files, network reachability, credentials, and host capabilities required for the current step.
- Separate read-only discovery, active probing, exploit validation, containment, and remediation into visible operator decisions.
- Keep destructive, persistence-changing, credential-touching, protection-disabling, or production-impacting actions approval-gated.
- Treat tool output as evidence to validate, not as an authoritative conclusion.
- Preserve command lines and machine-readable output where practical so another analyst can reproduce the result.

### Authorized Testing

- Require an explicit scope record before active probing: owner, targets, excluded targets, dates, source addresses, accounts, allowed techniques, rate limits, data handling, stop conditions, and notification contacts.
- Stop when target identity changes, a third party enters the path, production stability degrades, sensitive data is exposed beyond the minimum proof, or a test would require destructive impact, persistence, lateral movement, credential harvesting, or denial of service not already authorized.
- Prefer the smallest proof that establishes exploitability and impact. Preserve a non-destructive reproduction whenever possible.

### Containment And Recovery

- Distinguish evidence preservation from immediate harm reduction; state plainly when urgent containment may destroy volatile evidence.
- Do not casually disable Gatekeeper, XProtect, SIP, TCC, App Sandbox, endpoint protection, or automatic security updates to make analysis easier.
- Do not claim a host is clean merely because a suspicious process stopped or one artifact was removed.
- Keep containment, eradication, recovery, credential reset, notification, and hardening as separate decisions with their own verification.

## Phase 0: Plugin Foundation

- Scaffold `plugins/cybersecurity-skills/` with a valid manifest, local `AGENTS.md`, `skills/`, and assets.
- Add the root marketplace placeholder and update the root plugin inventory.
- Define the common security record, isolation decision matrix, active-test scope record, threat-confidence vocabulary, and report shapes as directly linked references.
- Add child validation that proves folder/frontmatter names, `agents/openai.yaml`, reference targets, machine-local path safety, and the expected skill inventory if no shared validator already covers those checks.
- Record the Codex and Hermes decision for every skill and update generated Hermes exports only for portable guidance.

## Phase 1: Shared Defensive Foundation

- `cybersecurity:route-security-work`: classify suspicious content, malware analysis, endpoint investigation, vulnerability validation, authorized testing, incident response, detection, or specialist handoff before tools run.
- `cybersecurity:preserve-security-evidence`: create the shared record, preserve originals, capture volatile-versus-durable evidence, hash artifacts, and document transformations and custody without pretending to provide legal-forensics certification.
- `cybersecurity:assess-and-explain-threat`: separate observations, hypotheses, reputation, behaviors, impact, confidence, and uncertainty; give immediate and long-term advice in language a non-specialist can act on.
- `cybersecurity:select-analysis-isolation`: choose among local read-only inspection, disposable container, Linux VM, macOS VM, remote sandbox, or spare physical device based on the actual threat model.
- `cybersecurity:operate-agentic-security-tools`: constrain agent permissions, mounts, network, secrets, approvals, logging, and cleanup for local CLIs, GUIs, MCP tools, browser tools, and remote analysis services.

Phase 1 exit criteria: an ambiguous concern can be routed, preserved, isolated, assessed, and explained before a specialist workflow is selected.

## Phase 2: Suspicious Content And Malware Analysis

- `cybersecurity:triage-suspicious-content`: inspect files, archives, installers, packages, scripts, documents, profiles, extensions, URLs, QR codes, and messages without executing active content.
- `cybersecurity:check-artifact-reputation`: use hashes, signer/provenance information, vendor sources, threat intelligence, and optionally approved third-party services while recording privacy and sample-upload boundaries.
- `cybersecurity:perform-static-malware-analysis`: inspect metadata, strings, imports, embedded content, configuration, signatures, rules, and likely capabilities; hand binary internals to `reverse-engineering-skills`.
- `cybersecurity:perform-dynamic-malware-analysis`: prepare a disposable environment, establish a baseline, observe process/file/network/persistence behavior, collect evidence, and tear the environment down.
- `cybersecurity:analyze-suspicious-script-or-document`: decode and inspect shell, AppleScript, JavaScript, Python, Office/PDF content, shortcuts, configuration profiles, and staged payload chains without triggering them.
- `cybersecurity:author-yara-x-rules`: write, test, scope, document, and regression-check YARA-X rules against positive and negative fixtures while avoiding brittle family claims.
- `cybersecurity:map-malware-behavior`: map observed behavior to current MITRE ATT&CK techniques without treating ATT&CK labels as proof of actor, campaign, or malware-family identity.

Phase 2 exit criteria: a suspicious artifact can move from safe intake through static or isolated dynamic analysis to a confidence-calibrated explanation and reusable detection evidence.

## Phase 3: macOS Defense And Investigation

- `cybersecurity:assess-macos-threat`: collect exact macOS build, hardware, user context, security-update state, Gatekeeper/quarantine/signing/notarization evidence, XProtect events, and relevant TCC or system-policy context.
- `cybersecurity:inspect-macos-persistence`: inspect login items, launch agents and daemons, system extensions, configuration profiles, shell startup files, browser extensions, scheduled behavior, and other current persistence surfaces without deleting evidence.
- `cybersecurity:inspect-macos-runtime-activity`: correlate processes, ancestry, open files, network connections, unified logs, Endpoint Security or `eslogger` evidence, and user actions with clear permission limits.
- `cybersecurity:use-objective-see-tools`: use the installed Objective-See tools as thin adapters, record the exact tool/version and permissions, and keep domain conclusions in the owning investigation skill.
- `cybersecurity:contain-and-recover-macos`: choose network isolation, process containment, account and credential actions, persistence removal, rebuild/restore, and verification steps proportionate to the evidence.
- `cybersecurity:harden-macos`: improve update posture, FileVault, firewalling, sharing and remote access, browser/extensions, login items, permissions, backups, and user habits without promising perfect prevention.

Phase 3 exit criteria: an affected Mac can be investigated and contained without weakening platform protections or confusing signature, notarization, quarantine, runtime access, and observed behavior.

## Phase 4: Vulnerability Research And Authorized Testing

- `cybersecurity:scope-authorized-security-test`: create the active-test scope record, define rules of engagement, select safe techniques, and identify approvals and stop conditions.
- `cybersecurity:triage-vulnerability-report`: normalize scanner output, advisories, bug reports, CVEs, PoCs, or researcher notes; identify affected assets and missing evidence; route source review to Codex Security when appropriate.
- `cybersecurity:validate-vulnerability`: reproduce the smallest safe proof, distinguish vulnerable code from reachable/exploitable behavior, challenge scanner assumptions, and retain negative results.
- `cybersecurity:assess-exposure-and-impact`: combine affected versions, deployed configuration, reachable attack surface, privileges, data, mitigations, exploit maturity, vendor guidance, CISA KEV status, and business context instead of ranking by CVSS alone.
- `cybersecurity:test-web-and-api-security`: use current OWASP testing guidance, browser/proxy evidence, API schemas, and bounded automated checks against an explicitly authorized target.
- `cybersecurity:test-network-services`: inventory and validate exposed services with bounded discovery and protocol-aware checks; hand protocol implementation questions to `network-protocol-skills`.
- `cybersecurity:report-security-assessment`: produce reproducible findings with evidence, impact, confidence, remediation, retest steps, and a non-specialist executive explanation.

Phase 4 exit criteria: a supplied or discovered vulnerability can be validated and prioritized without treating a CVE, severity score, scanner match, or exploit template as proof of exposure.

## Phase 5: Incident Response, Hunting, And Detection

- `cybersecurity:triage-security-incident`: establish what happened, affected scope, urgency, evidence sources, communication owner, and immediate harm-reduction decisions using the current NIST incident-response lifecycle.
- `cybersecurity:contain-security-incident`: select host, identity, service, network, or application containment while documenting business impact and volatile-evidence tradeoffs.
- `cybersecurity:recover-security-incident`: plan eradication, restore or rebuild, credential rotation, monitoring, validation, return to service, and follow-up hardening.
- `cybersecurity:hunt-security-indicators`: search scoped hosts, logs, files, identities, and network records for supplied indicators or behaviors while recording coverage gaps and false-positive controls.
- `cybersecurity:author-detection-content`: turn validated behavior into YARA-X, Sigma, osquery, or platform-native detection logic with provenance, fixtures, expected telemetry, and regression tests.

Phase 5 exit criteria: an incident can move from initial report through containment and verified recovery, and validated behaviors can become reusable detections without overstating coverage.

## Tool And Integration Strategy

Keep tools behind capability discovery and thin adapters. Do not make installation of every candidate tool a plugin prerequisite.

### First-Party macOS surfaces

- `file`, `shasum`, `xattr`, `codesign`, `spctl`, `pkgutil`, `plutil`, `otool`, `lsof`, `nettop`, unified logging, and `eslogger`
- Gatekeeper, notarization, XProtect, quarantine, TCC, SIP, App Sandbox, FileVault, and the application firewall as distinct evidence and protection layers
- Apple Virtualization framework and macOS guests for full-system isolation
- Apple's `container` tool for disposable Linux workloads, with exact-version and network/mount capability checks

### Malware and endpoint candidates

- YARA-X for local pattern matching and detection rules
- Objective-See tools for macOS persistence, process, file, network, signing, and blocking workflows
- osquery for reproducible host-state and event queries when its permissions and Endpoint Security support are present
- ClamAV only as one signature engine, never as a safety verdict
- VirusTotal or another remote reputation/sandbox service only after explicit data-egress approval

### Vulnerability and authorized-test candidates

- Codex Security for repository and diff scanning when available
- OSV-Scanner for dependency and image advisory matching, with package identity and reachability validation
- OWASP ZAP or an operator-approved intercepting proxy for web/API evidence
- Nuclei for narrowly selected, reviewed templates against authorized targets; never default to broad template execution
- Nmap, Wireshark, and mitmproxy when their exact target, capture, and network boundaries are explicit

Tool-specific skills should be added only when a tool has a distinct repeated workflow that cannot stay concise in a domain skill. The first planned exception is the Objective-See adapter because its separate macOS apps share an operator workflow but produce different evidence.

## Realistic Forward Tests

Forward-test with redistributable, locally generated, or explicitly approved fixtures. Include blocked and uncertain outcomes as first-class results.

1. A fake signed macOS app bundle with benign but suspicious-looking network and persistence strings.
2. A notarized benign utility whose behavior still warrants a privacy warning.
3. An unsigned script chain inside an archive that downloads a harmless local test payload.
4. A document or shortcut containing obfuscated but non-executed commands.
5. A YARA-X rule with positive fixtures, near-miss negatives, packed/noisy content, and a regression corpus.
6. A disposable Linux container with restricted mounts and networking, plus a test proving that the chosen isolation is insufficient for a macOS payload.
7. A disposable macOS VM with no personal accounts, shared clipboard, host folders, developer identities, or cloud credentials.
8. A deliberately vulnerable local web/API fixture exercised under a written scope record with passive, active, and stop-condition cases.
9. A scanner-reported dependency vulnerability that is present but unreachable, and one that is reachable despite a lower raw severity score.
10. A simulated macOS incident with persistence, process, file, network, and log evidence, including a false-positive lookalike.
11. A non-specialist advice test where the agent must give immediate steps without panic, certainty inflation, or jargon.

## Documentation And Validation

- Keep `SKILL.md` procedural and concise. Put tool matrices, output schemas, current platform behavior, and larger examples in directly linked `references/`.
- Give each frontmatter description concrete inputs and user requests that should trigger it.
- Generate matching `agents/openai.yaml` metadata from the final skill content.
- Use official vendor documentation, current tool help, checked-out source, and observed local behavior before community summaries.
- Date version-sensitive platform, threat-intelligence, scanner, and beta claims. Require live confirmation when they affect a conclusion.
- Do not embed malware, exploit payloads, private samples, VM images, tool databases, cloud keys, machine-local paths, or copied proprietary intelligence in the plugin.
- Validate every skill with the skill-authoring validator and run `uv run scripts/validate_socket_metadata.py` after marketplace or manifest changes.
- Export portable skills through the Hermes tap in the same pass and update `skills.sh.json`; document any host-specific tool or Computer Use workflow instead of pretending the Codex manifest is portable.
- Add a checked-in Hermes `mcp_servers` translation only if a later approved `.mcp.json` exists. A guidance-only first release needs no MCP translation or native Hermes plugin.
- Update root README inventory text, `ROADMAP.md`, architecture metadata, marketplace metadata, and version surfaces together when the plugin becomes installable.

## Source Baseline

Recheck these sources during implementation; the list was verified on 2026-07-14.

- [Apple Platform Security: Protecting against malware in macOS](https://support.apple.com/guide/security/protecting-against-malware-sec469d47bd8/web)
- [Apple Virtualization framework](https://developer.apple.com/documentation/virtualization)
- [Apple container technical overview](https://github.com/apple/container/blob/main/docs/technical-overview.md)
- [YARA-X documentation](https://virustotal.github.io/yara-x/docs/)
- [Objective-See tools](https://objective-see.org/tools.html)
- [osquery documentation](https://osquery.readthedocs.io/)
- [MITRE ATT&CK macOS matrix](https://attack.mitre.org/matrices/enterprise/macos/)
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP ZAP documentation](https://www.zaproxy.org/docs/)
- [FIRST CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [OSV-Scanner documentation](https://google.github.io/osv-scanner/)
- [ProjectDiscovery Nuclei documentation](https://docs.projectdiscovery.io/tools/nuclei/overview)

## Release Decision

The first installable release implements all five planned phases. It delivers the complete suspicious-content-to-macOS-defense path, authorized vulnerability-validation and bounded web/API and network-testing guidance, incident response, hunting, and reusable detection-content workflows on the same evidence, confidence, isolation, scope, and reporting records.

Treat the first installable `cybersecurity-skills` release as a Socket minor version. Any privileged runtime, bundled scanner, MCP server, remote sandbox integration, or autonomous active-testing surface requires a separate explicit architecture and release decision.
