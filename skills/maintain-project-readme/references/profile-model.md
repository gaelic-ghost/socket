# Profile Model

## Supported Profiles

### `library-package`

- Use for libraries, SDKs, reusable packages, and importable modules.
- Usually detected from package metadata without app/service runtime signals.

### `cli-tool`

- Use for command-line tools with executable entrypoints or package scripts/binaries.
- Usually detected from Python scripts, `package.json` `bin`, Cargo binaries, or Swift executable targets.

### `app-service`

- Use for deployable apps, local servers, web apps, APIs, and runtime-backed products.
- Usually detected from app frameworks, runtime configs, or Docker/service files.

### `monorepo-workspace`

- Use for workspaces with multiple apps/packages/services managed together.
- Usually detected from workspace manifests like `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, or Cargo workspace config.

## Detection Policy

- Prefer repo signals over user phrasing.
- If multiple profiles match, select the most conservative valid profile and report the ambiguity.
- Route skills/plugin repos away from this skill and into the dedicated `maintain-skills-readme` skill in `/Users/galew/Workspace/agent-plugin-skills`.

## Apply-Mode Normalization

- Clear profile match:
  - add the canonical profile-specific section if missing
  - normalize it into canonical section order
  - preserve any existing section content
- Ambiguous profile match:
  - keep reporting the ambiguity
  - do not auto-create a new profile-specific section
