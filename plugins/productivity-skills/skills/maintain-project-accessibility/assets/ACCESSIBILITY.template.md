# Accessibility

{{ONE_LINE_SUMMARY}}

## Table of Contents

- [Overview](#overview)
- [Standards Baseline](#standards-baseline)
- [Accessibility Architecture](#accessibility-architecture)
- [Engineering Workflow](#engineering-workflow)
- [Known Gaps](#known-gaps)
- [User Support and Reporting](#user-support-and-reporting)
- [Verification and Evidence](#verification-and-evidence)

## Overview

### Status

State the current accessibility posture in one short, plain sentence.

### Scope

Describe which project surfaces this accessibility contract covers.

### Accessibility Goals

Describe the real accessibility outcomes this project is trying to deliver.

## Standards Baseline

### Target Standard

Name the target standard or internal baseline this project is working toward.

### Conformance Language Rules

Explain what language the project may or may not use when describing accessibility status.

### Supported Platforms and Surfaces

List the concrete environments, platforms, or user-facing surfaces this document applies to.

## Accessibility Architecture

### Semantic Structure

Describe how the project preserves headings, landmarks, labels, structure, and other semantic meaning.

### Input and Keyboard Model

Describe how the project handles keyboard access, direct input, and interaction behavior.

### Focus Management

Describe how focus order, focus visibility, and focus recovery are handled.

### Naming and Announcements

Describe how controls, state changes, and dynamic updates are named or announced to assistive technology.

### Color, Contrast, and Motion

Describe the rules for contrast, color meaning, animation, and motion reduction.

### Zoom, Reflow, and Responsive Behavior

Describe how the project handles zoom, text scaling, reflow, and narrow layouts.

### Media, Captions, and Alternatives

Describe the project's expectations for media alternatives such as captions, transcripts, and text equivalents.

## Engineering Workflow

### Design and Implementation Rules

Describe the concrete implementation rules contributors should follow when changing accessibility-relevant surfaces.

### Automated Testing

Document the automated accessibility checks used by this project.

### Manual Testing

Document the manual accessibility checks required for relevant changes.

### Assistive Technology Coverage

Document the assistive technologies, browsers, devices, or operating environments the team actively tests.

### Definition of Done

Describe what must be true before accessibility-relevant work is considered ready for review or merge.

## Known Gaps

### Current Exceptions

List known accessibility limitations, unsupported surfaces, or temporary exceptions.

### Planned Remediation

Describe how known accessibility gaps are tracked or remediated.

### Ownership

Describe who is responsible for keeping this document and its follow-up work current.

## User Support and Reporting

### Feedback Path

Describe how users or maintainers should report accessibility issues or request support.

### Triage Expectations

Describe how accessibility reports should be acknowledged, triaged, or escalated.

## Verification and Evidence

### CI Signals

List the CI or automation signals that support the project's accessibility claims.

### Audit Cadence

Describe how often accessibility review happens and when it is required.

### Review History

Record notable accessibility-review checkpoints, updates, or resets.
