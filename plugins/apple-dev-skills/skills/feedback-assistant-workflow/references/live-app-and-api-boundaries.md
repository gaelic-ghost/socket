# Live App and API Boundaries

## Observed Mac Surface

On 2026-07-13, the signed-in `com.apple.appleseed.FeedbackAssistant` app opened its Inbox window. The sidebar exposed Recent Activity, Requests, All, News, Inbox, Drafts, and Submitted; the toolbar exposed search, More, and New Feedback. This is a live-app fixture, not a promise that every account has the same mailbox or team access.

Use the app or [Feedback Assistant on the web](https://feedbackassistant.apple.com) for report creation and follow-up. Apple documents `applefeedback://` as a launch URL scheme, not as a report-submission API.

## General API Boundary

No Apple-documented general API for creating, reading, updating, or submitting Feedback Assistant reports was found during this skill's 2026-07-13 research. Do not reverse engineer, invoke, or rely on private Feedback Assistant services. Re-check Apple's documentation when a future task depends on this boundary.

## Transmission Boundary

Diagnostics may contain account, network, location, content, crash, and device data. Always review the exact attachment list with the user before sending data to Apple. A successful submission produces a Feedback Assistant ID that can be used to track the report.
