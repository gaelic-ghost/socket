# JavaScript / TypeScript Checks

## Detection

Treat repository as JS/TS when `package.json` exists.
TypeScript signal:
- `tsconfig.json` exists.

## Canonical Package Manager

Infer from lockfiles (priority order):
1. `pnpm-lock.yaml` -> `pnpm`
2. `package-lock.json` -> `npm`
3. `yarn.lock` -> `yarn`
4. none -> unknown (do not auto-fix manager-specific commands)

## Alignment Expectations

- Docs command examples should primarily use the canonical manager.
- Typical expected command families:
  - install: `pnpm install` / `npm install` / `yarn install`
  - run: `pnpm <script>` or `pnpm run <script>` / `npm run <script>` / `yarn <script>`

## Safe Fix Scope

- Replace explicit wrong manager invocations in docs where command intent is obvious.
- Avoid rewrites when lockfile evidence is missing or mixed.
