# CloudKit Automation

## Existing Container Boundary

`cktool` and CKTool JS automate schema and data workflows for an existing CloudKit container. They do not make Apple Developer Portal registration or app-ID assignment automatable. Confirm the team ID, container ID, development (Sandbox) or production environment, and intended schema/data operation before invoking either official surface.

## cktool

Apple distributes [`cktool`](https://developer.apple.com/icloud/ck-tool/) with Xcode. It is stateless for CloudKit API calls and stores management and user tokens securely in macOS Keychain. Generate a management token in CloudKit Console’s account Settings, save it once with:

```zsh
xcrun cktool save-token --type management
```

Use it for a read-first sequence: inspect help, export the current schema, review the artifact outside versioned secrets, and only then plan a schema apply or sandbox reset. `reset-schema` reverts the development schema to the production definition, so it is destructive and requires a fresh confirmation.

## CKTool JS

[CKTool JS](https://developer.apple.com/documentation/cktooljs/) is Apple’s official JavaScript client alternative to `cktool`, intended for local development and integration tests. In a TypeScript project, use pnpm and add the official packages:

```zsh
pnpm add @apple/cktool.database @apple/cktool.target.nodejs
```

At runtime, create the Node configuration and pass a management token from local secret storage to `PromisesApi`; never put the token in source, a lockfile, fixture, committed `.env`, or browser bundle. Apple documents that CKTool JS supports sandbox schema application, test-data population, reset to production schema, and integration-test scripts. User-data access additionally needs a user token; do not treat a management token as user authorization.

## Validation Contract

- Export and review schema before a schema-affecting operation.
- Default integration automation to sandbox/development and isolated test records.
- Require an explicit operation-specific confirmation for production work, reset, schema apply, or data mutation.
- Report container/environment and changed schema/data identifiers, but never tokens or record content that contains sensitive user data.
