# Owner Routing

`maintain-plugin-repo` is a repo-level maintainer orchestrator.

It should keep these ownership boundaries explicit:

- `validate-plugin-install-surfaces`
  - canonical owner of audit-only packaging, marketplace, discovery-mirror, bundled-skill-tree, and README install-surface validation
- `maintain-plugin-docs`
  - canonical owner of README and ROADMAP maintenance
- `install-plugin-to-socket`
  - canonical owner of bounded local Codex install, update, uninstall, verify, repair, enable, disable, and promote workflows

Version 1 routing rules:

- always run the validator first
- always run the docs audit
- only run install-surface repair when the maintainer explicitly provided:
  - `--source-plugin-root`
  - `--apply-install-repairs`
- treat missing install inputs as deferred work instead of guessing
- do not perform direct manifest surgery or source edits outside what the routed owner scripts already support
