# Safari MCP Setup And Privacy

## Preflight

Safari MCP is introduced in Safari Technology Preview 247. Confirm the installed preview version and that the driver is available before relying on a live session.

Enable Safari Settings > Advanced > Show features for web developers, then Safari Settings > Developer > Enable remote automation and external agents. Some Safari Technology Preview builds label the final control **Allow remote automation**; `safaridriver` reports that exact label when the permission is missing.

With the user's explicit approval, Codex can register the local server:

```zsh
codex mcp add safari-mcp-stp -- \
  "/Applications/Safari Technology Preview.app/Contents/MacOS/safaridriver" --mcp
```

Registration changes the user's MCP configuration. Do not perform it as an implicit prerequisite, and do not commit the registration into project configuration.

## Tool Scope

Safari MCP provides tab navigation, page content, JavaScript evaluation, console messages, network request inspection, screenshots, viewport and media emulation, dialogs, and DOM interactions. Start with read-only tools; use interaction tools only inside the agreed scope.

## Data Boundary

Safari MCP runs locally and makes no network calls of its own. Page content, screenshots, and console data are passed to the connected agent, so collect only what the stated task needs. Avoid authenticated production pages when a local fixture can prove the same behavior.

Safari MCP does not access Safari AutoFill or unrelated browser activity. That does not make every page safe to inspect: page content and responses may still include user data, tokens, or other sensitive information.

## Failure Reporting

Report the concrete missing prerequisite: preview app, `safaridriver`, Safari setting, MCP registration, tab, target origin, or page state. Do not replace live Safari proof with a generic browser test without saying that Safari evidence remains missing.
