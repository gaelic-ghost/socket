## Milestone 1: Bootstrap standalone plugin repo and import it into `socket`

Scope:

- Turn this directory into a real standalone plugin source repo and make it ready for subtree import into `~/Workspace/gaelic-ghost/socket/`.

Tickets:

- Add first-class `.codex-plugin/plugin.json` packaging at the source-repo root.
- Remove the abandoned repo-local marketplace experiment and nested bundled copy of `agent-plugin-skills`.
- Initialize Git history for this child repo.
- Import the repo into `socket/plugins/speak-to-user-skills` as a subtree.
- Add a `socket` marketplace entry only after the repo has real plugin packaging and a deliberate role in the curated catalog.

Exit criteria:

- The repository is a real standalone plugin repo with source-of-truth packaging at the root.
- The repo no longer relies on a nested plugin copy or repo-local marketplace wiring for bootstrap.
- `socket` can import the repo cleanly as a subtree when its first real skill content is ready.
