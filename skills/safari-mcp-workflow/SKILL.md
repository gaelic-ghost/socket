---
name: safari-mcp-workflow
description: Inspect a scoped live site in Safari through Safari Technology Preview's local MCP server. Use for Safari-specific DOM, console, network, screenshot, accessibility, performance, interaction, responsive, or print-media evidence.
metadata:
  hermes:
    category: apple-development
    tags: [apple, safari, webkit, mcp, browser, validation]
---

# Safari MCP Workflow

## Purpose

Use Safari MCP for evidence from a live Safari Technology Preview tab. It owns browser-runtime observation and authorized interaction, not Safari extension architecture, app-to-Safari control, Web Inspector extension design, or cross-browser certification.

## When To Use

- Use for Safari-specific rendering, DOM, console, network, screenshot, interaction, accessibility, performance, responsive, or print-media investigation.
- Use when a local web app needs Safari evidence before a fix is proposed or accepted.
- Use `safari-extension-control-workflow` for Safari Web Extension, Safari App Extension, SafariServices, or Web Inspector extension architecture.
- Use `xcode-testing-workflow` for XCTest, XCUITest, simulator, or Xcode-run validation.
- Use `explore-apple-swift-docs` for Apple documentation lookup that does not need a live tab.

## Single-Path Workflow

1. Scope the target before connecting: name the origin, tab, requested state, permitted interactions, and any sensitive data boundary. Do not inspect unrelated tabs.
2. Preflight Safari Technology Preview 247 or later, its `safaridriver` executable, and Safari's **Enable remote automation and external agents** setting (shown as **Allow remote automation** in some builds). Read `references/setup-and-privacy.md`.
3. Register Safari MCP only with explicit approval. Use the documented local `safaridriver --mcp` command; do not bundle a server, silently alter global MCP configuration, or claim a connection before listing its tools.
4. Establish page state with tab, URL, loading, and `get_page_content` evidence before evaluating JavaScript or taking a screenshot. Use its node `uid` values when an interaction must target a specific element. Then collect the smallest useful combination of console, network, DOM, JavaScript, and screenshot evidence.
5. Perform only the authorized interaction sequence; batch related reversible steps through `page_interactions` with a stated purpose and the relevant node `uid` when that makes the recorded sequence clearer. Do not submit forms, purchase, delete, change account state, or reveal secrets without a fresh user confirmation immediately before the effect.
6. For accessibility, inspect semantic markup, labels, ARIA, keyboard reachability, and relevant visual contrast evidence. Report findings as focused checks, not a compliance certification.
7. For performance, use bounded page metrics and network timings. State whether the evidence is a one-run observation, not a benchmark or regression guarantee.
8. Re-check the requested outcome after each change with independent evidence. Read `references/evidence-and-validation.md` for the reporting contract.
9. Return the target, Safari Technology Preview version, observed evidence, authorized actions, unresolved uncertainty, and one focused handoff.

## Inputs

- `target`: required origin, URL, or already selected tab.
- `goal`: required bug, behavior, accessibility, performance, or visual expectation.
- `interaction_scope`: optional `read-only`, `reversible`, or an explicitly named state-changing action.
- `data_boundary`: optional authenticated, private, payment, or other sensitive-page restriction.
- `viewport`: optional CSS-pixel viewport or media type.
- Defaults: use read-only inspection, one scoped tab, minimal data collection, and Safari-specific claims only.

## Outputs

- `status`: `success`, `handoff`, or `blocked`.
- `evidence`: selected tab/URL, Safari Technology Preview version, tool results, screenshots when useful, and observed-versus-expected behavior.
- `actions`: every interaction performed and whether it changed state.
- `next_step`: one concrete fix, retest, or workflow handoff.

## Guards and Stop Conditions

- Do not expose or log credentials, cookies, tokens, AutoFill data, private text, or unrelated browsing activity.
- Do not treat Safari MCP as a Safari extension API, an arbitrary native-control surface, or cross-browser proof.
- Do not present a screenshot alone as behavioral proof; pair it with DOM, state, console, network, or interaction evidence as appropriate.
- Stop with `blocked` when Safari Technology Preview, the driver, the required Safari setting, or an authorized target is unavailable.
- Stop and ask immediately before any irreversible or account-, payment-, privacy-, or publication-affecting action.

## Fallbacks and Handoffs

- Recommend `safari-extension-control-workflow` for Safari integration and extension decisions.
- Recommend `xcode-testing-workflow` for Xcode-owned tests and UI automation.
- Recommend `apple-ui-accessibility-workflow` for Apple native UI accessibility work.
- Recommend `explore-apple-swift-docs` for current Apple or WebKit documentation.

## Customization

Use `references/customization-flow.md`. The first version has no runtime-enforced settings: origin, interaction, and privacy boundaries must be chosen for each live session.

## References

### Workflow References

- `references/setup-and-privacy.md`
- `references/evidence-and-validation.md`
- `references/customization-flow.md`

### Authoritative Sources

- [Introducing the Safari MCP server for web developers](https://webkit.org/blog/18136/introducing-the-safari-mcp-server-for-web-developers/)
- [Safari Technology Preview](https://developer.apple.com/safari/technology-preview/)

### Script Inventory

- `scripts/customization_config.py`
