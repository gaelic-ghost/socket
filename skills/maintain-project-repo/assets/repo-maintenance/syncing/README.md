# Repo-Maintenance Syncing Steps

Small helper surface for deterministic repo-maintenance sync hooks.

## Overview

This directory holds repo-specific shell hooks that the shared repo-maintenance sync entrypoint can discover and run.

### Motivation

It exists so a repository can keep local sync follow-up steps in one predictable place without forking the shared sync entrypoint itself.

## Setup

Add repo-specific executable `.sh` files here only when the repository needs deterministic shared-sync follow-up steps.

## Usage

The top-level `scripts/repo-maintenance/sync-shared.sh` entrypoint discovers and runs every `*.sh` file in this directory in lexical order.

## Development

Keep each hook small, deterministic, and specific to the owning repository's guidance or packaging sync needs.

## Verification

Run the owning repository's shared sync entrypoint and confirm the expected repo-specific hooks execute in lexical order.

## License

Covered by the parent repository license.
