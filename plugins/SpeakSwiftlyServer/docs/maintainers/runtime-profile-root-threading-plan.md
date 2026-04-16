# Runtime Profile Root Threading Plan

## Purpose

This note records the release-facing plan for one explicit runtime profile-root override across the
embedded, standalone executable, and LaunchAgent startup paths.

The concrete goal is simple:

- an app embedding `SpeakSwiftlyServer` can pass one custom runtime profile root URL
- the server uses that same root for its persisted runtime configuration snapshot
- the underlying `SpeakSwiftly` runtime uses that same root for stored profiles, generated
  artifacts, and text-profile persistence

## Problem Statement

Before this pass, the lower layers already understood the `SPEAKSWIFTLY_PROFILE_ROOT`
environment override, but the package did not expose one clean end-to-end app-facing contract.

The main gaps were:

1. `EmbeddedServerSession.Options` could override the localhost port, but not the runtime profile
   root.
2. `RuntimeConfigurationStore` could honor `SPEAKSWIFTLY_PROFILE_ROOT`, but the embedded startup
   path did not thread the embedded session's startup environment all the way into
   `ServerHost.live(...)`.
3. `SpeakSwiftly.liftoff(configuration:)` still resolved its profile-root override from the process
   environment rather than from an explicit startup parameter, so the server needed one contained
   bridge instead of assuming the runtime would see the same startup environment automatically.
4. The standalone executable only documented the env override indirectly through the LaunchAgent
   path, even though direct `serve` runs are another operator-facing startup surface.

## Decisions

### 1. Keep One Shared Override Key

The package keeps `SPEAKSWIFTLY_PROFILE_ROOT` as the shared override key across surfaces instead of
inventing a second server-only environment variable.

That keeps the server and `SpeakSwiftly` aligned on one operator-facing concept and avoids
translation layers between package-local and library-local startup policy.

### 2. Add A Typed Embedded API

`EmbeddedServerSession.Options` grows `runtimeProfileRootURL: URL?`.

This is the public app-facing entry point for sandboxed app hosts, app-owned Application Support
paths, or App Group container roots. App code should not have to mutate process-global environment
state just to choose the runtime profile root.

### 3. Keep LaunchAgent Support Explicit

The LaunchAgent path already has `--profile-root`, and it should remain the canonical per-user
background-service override for the installed service.

That surface already emits `SPEAKSWIFTLY_PROFILE_ROOT` into the installed property list and does
not need a second override model.

### 4. Add A Matching Standalone `serve` Surface

The direct executable path should also accept `--profile-root`, so foreground operator runs and
embedded app runs are not more awkward than LaunchAgent installs.

The standalone executable continues to support the environment override too, but the explicit
command-line flag is the clearer operator-facing path.

### 5. Do Not Broaden YAML In This Pass

This pass intentionally does **not** add a YAML key such as `app.runtimeProfileRoot`.

Reason:

- the runtime profile root is startup ownership policy, not ordinary live-reload config
- the environment and typed startup APIs already cover the real near-term use cases
- adding a YAML key would widen restart semantics and config-surface policy in the same release

If YAML-backed persistence-root configuration becomes important later, treat that as a separate
decision after the startup surfaces settle.

## Implementation Shape

### Startup Environment Ownership

The package should treat the startup environment passed into embedded or standalone startup as the
source of truth for the bridged runtime profile root.

That means:

- embedded startup computes one effective environment from the caller environment plus typed
  `Options`
- standalone startup computes one effective environment from process environment plus `serve`
  options
- LaunchAgent startup keeps emitting the same override into the child process environment

### Runtime Bridge

`SpeakSwiftly.liftoff(configuration:)` currently reads `SPEAKSWIFTLY_PROFILE_ROOT` from the process
 environment during startup.

For this repository, the correct short-term shape is one contained startup launcher helper that:

1. serializes startup launches that need environment bridging
2. temporarily applies the bridged `SPEAKSWIFTLY_PROFILE_ROOT` override
3. calls `SpeakSwiftly.liftoff(configuration:)`
4. restores the original process environment afterward

This is a local implementation detail, not a new public package abstraction.

## Detailed Checklist

- [x] Add `runtimeProfileRootURL` to `EmbeddedServerSession.Options`.
- [x] Apply that option to the embedded startup environment before config loading.
- [x] Pass the resolved startup environment into `ServerHost.live(...)` instead of relying on
      ambient process globals there.
- [x] Construct `RuntimeConfigurationStore` from that startup environment.
- [x] Add one contained runtime launcher helper that bridges `SPEAKSWIFTLY_PROFILE_ROOT` into
      `SpeakSwiftly.liftoff(configuration:)` during startup and then restores the previous process
      environment.
- [x] Add a standalone `serve --profile-root <path>` surface.
- [x] Preserve the existing LaunchAgent `--profile-root <path>` surface and document it alongside
      the other startup paths.
- [x] Update README, API docs, and DocC embedding/operator articles so the persistence-root model is
      explicit.
- [x] Add or update tests for embedded option shaping and `serve` command parsing.

## Follow-Up After This Pass

The longer-term cleanup belongs upstream in `SpeakSwiftly`.

The ideal future shape is for `SpeakSwiftly.liftoff(...)` to accept an explicit startup persistence
location, or for `SpeakSwiftly.Configuration` to carry that startup storage override directly,
instead of relying on a process-environment bridge.

Until that upstream shape exists, keep the bridge isolated in one startup helper here and do not
copy that environment-mutation pattern into unrelated code paths.
