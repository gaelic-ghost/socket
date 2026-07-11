# App Store Connect Provisioning

## Supported Automation Boundary

The [App Store Connect API provisioning overview](https://developer.apple.com/app-store-connect/api/) documents automation for registered bundle IDs, supported capabilities, certificates, devices, and provisioning profiles. The workflow starts with list/read requests, filters to the selected team and project identifier, then produces an explicit request plan before any change.

The profile resource combines a bundle ID with certificates and, where applicable, devices; Apple documents create, delete, download, and relationship endpoints in [Profiles](https://developer.apple.com/documentation/appstoreconnectapi/profiles). Do not regenerate a profile blindly: first identify the certificate, device list, profile type, and target bundle ID it would replace or affect.

## Account Setup

For provisioning REST endpoints, use a **team API key**, not an individual key. Apple documents that individual API keys cannot access provisioning endpoints in [Creating API Keys](https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api). The Account Holder must first request App Store Connect API access; an Account Holder or Admin can generate a team key and assigns its role. Team keys apply across all apps, so choose the least privileged role that permits the planned operation.

Do not use this App Store Connect key path for Apple Developer Enterprise Program accounts: Apple directs those accounts to the separate Enterprise Program API, and team API keys are unavailable in that program. For portal-only identifier work, Apple documents Account Holder or Admin as the required role for [App ID registration](https://developer.apple.com/help/account/identifiers/register-an-app-id/) and [App Group registration](https://developer.apple.com/help/account/identifiers/register-an-app-group/). Individual enrolments can grant App Store Connect access to additional people, but those people are not Apple Developer Program team members and do not gain Certificates, Identifiers & Profiles access.

Store the one-time-downloaded `.p8` private key locally, along with its key ID and issuer ID. Generate the JWT in memory for the current invocation; it is authorization material, not a project configuration value. Apple advises revocation if a private key is lost or compromised.

Individual enrollment has an additional constraint: people added in App Store Connect receive App Store Connect access but are not members of the Apple Developer Program team, so they do not receive Certificates, Identifiers & Profiles access. See Apple’s [roles reference](https://developer.apple.com/help/account/access/roles/).

## Plan Contract

Before a write, return:

- selected team and expected role/key type;
- matched project bundle ID and App Store Connect resource ID;
- read-only current certificates, devices, capabilities, and profiles;
- exact resource operation and the user-visible consequence;
- validation that will run after the requested change.

For a create, update, revoke, or delete, show the exact resource name and identifier and ask for an operation-specific confirmation. Do not silently substitute a different team or similarly named bundle ID.
