# Customization Guide

Use this reference when you need to change the defaults shipped by `uv-pytest-unit-testing`.

## High-Impact Knobs

- baseline `tool.pytest.ini_options` content
- coverage behavior and optional dependency installation
- package-targeted run expectations for workspaces
- test path and marker conventions
- CI-oriented command examples

## Audit Checklist After Changes

- dry-run and real bootstrap flows still match the docs
- root-project and `--package` command examples still work
- the troubleshooting order still reflects the real intended workflow
- repo-level validation still passes after doc and metadata updates
