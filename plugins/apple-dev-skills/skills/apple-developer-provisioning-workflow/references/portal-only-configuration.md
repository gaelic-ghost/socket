# Portal-Only Configuration

## Honest Boundary

The App Store Connect API’s documented provisioning resources cover bundle IDs, capabilities, certificates, devices, and profiles. It does not make every Apple Developer Portal form programmable. A missing resource or relationship in the current official API is a portal task, not an invitation to reverse engineer the website.

Keep these operations explicitly portal-only unless Apple publishes a supported API for the exact action:

- registering an App Group and assigning it to an App ID;
- registering a CloudKit container and assigning it to an App ID;
- registering Service IDs and completing their related configuration;
- portal-only service configuration or capability options that have no documented REST resource.

## Portal Handoff

The plan should name the selected team, exact identifier/container, expected entitlement or service effect, and any follow-on profile regeneration. The user completes the portal step interactively, then the workflow re-runs read-only discovery, verifies the project configuration, and only creates or refreshes the profile after an explicit confirmation.

## Future Portal Driver

An interactive Apple Developer Portal Driver may eventually improve accessible navigation and evidence capture, but it must not bypass Apple authentication, two-factor authentication, account selection, or destructive-change confirmation. Until then, preserve the manual portal step and do not implement browser automation in this workflow.
