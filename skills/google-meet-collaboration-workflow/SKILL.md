---
name: google-meet-collaboration-workflow
description: Plan and validate Google Meet add-ons, conference REST integrations, event subscriptions, artifacts, and preview media API work.
---

# Google Meet Collaboration Workflow

## Workflow

1. Choose the smallest correct surface: web add-on for in-meeting shared collaboration, REST API for meeting spaces and post-conference artifacts, Workspace Events for subscriptions, or the Media API only for an explicitly accepted Developer Preview evaluation.
2. Define Workspace identity, OAuth scopes, organizer and participant data access, add-on deployment, and data retention before implementation.
3. For an add-on, design shared state and participant controls as collaboration features rather than as an unattended meeting bot.
4. For REST/event work, separate meeting-space management from artifact processing and avoid using conference data for user performance evaluation.
5. For Media API evaluation, record preview status, consent, media handling, cost, and rollback conditions. Do not present preview behavior as production stable.
6. Validate in a test Workspace and meeting: installation, participant join, shared state, event subscription, artifact availability, authorization failure, and removal.

## Source And Handoffs

Start with the [Google Meet SDK and API overview](https://developers.google.com/workspace/meet/overview). Hand web implementation to the web workflow and backend work to the chosen server skill.
