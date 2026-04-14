# Contributing to {{PROJECT_NAME}}

Use this guide when preparing changes so the project stays understandable, runnable, and reviewable for the next contributor.

## Table of Contents

## Overview

### Who This Guide Is For

Explain who should use this guide and what kinds of contributions it is meant to support.

### Before You Start

Call out the most important prerequisites before someone begins work, such as reading nearby docs, checking open work, or understanding repo constraints.

## Contribution Workflow

### Choosing Work

Explain how contributors should choose or confirm work before they begin.

### Making Changes

Explain the normal path for making changes in this repository, including how to keep work bounded and coherent.

### Asking For Review

Explain when a change is ready for review and what contributors should double-check first.

## Local Setup

### Runtime Config

Document the concrete local configuration contributors need, including files, secrets, environment variables, or local services.

### Runtime Behavior

Explain what needs to be running locally and how contributors can tell the project is actually working.

## Development Expectations

### Naming Conventions

Describe the terminology, casing, and naming patterns contributors should match when extending the project.

### Accessibility Expectations

Contributors must keep changes aligned with the project's accessibility contract in [`ACCESSIBILITY.md`](./ACCESSIBILITY.md).

If a change affects UI semantics, input behavior, focus flow, labels, announcements, motion, contrast, zoom behavior, content structure, or assistive-technology compatibility, verify the affected surface against the documented accessibility standards before asking for review.

If a change introduces a new accessibility limitation, exception, or remediation plan, update `ACCESSIBILITY.md` in the same pass unless maintainers have explicitly agreed on a different tracking path.

### Verification

Prefer grounded validation commands with fenced code blocks and language info strings when examples help.

## Pull Request Expectations

Explain what a good pull request should contain so reviewers get the right context quickly.

## Communication

Explain how contributors should surface questions, design uncertainty, or larger-scope changes before they drift.

## License and Contribution Terms

State any practical contribution terms here. If there is nothing unusual, point contributors to the project license directly.
