---
name: feedback-assistant-workflow
description: Prepare, stage, and safely submit high-signal Apple Feedback Assistant bug reports, crash reports, enhancement requests, and Foundation Models feedback attachments. Use when Codex needs to gather reproducible evidence for Apple software, SDKs, developer tools, hardware, documentation, beta releases, or system-model behavior; operate the Feedback Assistant app or website; or turn a Foundation Models session into a reviewable feedback attachment.
---

# Feedback Assistant Workflow

## Purpose

Prepare one actionable Apple report at a time. Own report quality, evidence selection, privacy review, and the Feedback Assistant handoff; do not replace the specialist workflow that diagnoses the underlying problem.

## Required Evidence

1. Classify the report as a bug, crash, regression, enhancement, documentation issue, or Foundation Models behavior issue. Route security and privacy vulnerabilities to Apple's security reporting program instead of ordinary Feedback Assistant.
2. State one concise title, environment, minimal reproduction, expected result, actual result, frequency, and regression range when known. Keep unrelated issues in separate reports.
3. Build an attachment manifest before opening the submit path. Include source, collection time, purpose, and privacy review for each log, sample project, System Information Report, recording, screenshot, or `.json` feedback attachment.
4. Hand off diagnosis to the owning workflow when needed: `ios-runtime-forensics-workflow` for runtime evidence, `xcode-debugger-mcp-workflow` for a debugging session, `xcode-device-hub-workflow` for connected-device evidence, and `explore-apple-swift-docs` for API routing.

## Feedback Assistant App And Web Workflow

1. Prefer the Feedback Assistant app on Mac, iPhone, or iPad when timely diagnostics matter. Use the website only when the evidence was captured manually or the app is unavailable.
2. On this Mac, inspect `com.apple.appleseed.FeedbackAssistant`. Its signed-in main window exposes Inbox, Drafts, Submitted, Requests, team mailboxes when available, search, and New Feedback.
3. Select the narrowest topic and product area. Verify the report describes one issue before drafting or staging it.
4. Keep a staged report in Drafts until its prose and attachment manifest have been reviewed. Record the Feedback Assistant ID only after a report has been submitted.
5. If Apple requests more information, preserve the original report's scope and attach only the requested, reviewed evidence.

## Submission And Privacy Gate

- Never accept license terms, create a report, attach a file, send a message, or submit feedback unless the user asked for that specific action.
- Before attaching potentially sensitive evidence or typing it into the app or website, show the exact files or data, identify Apple as the recipient, explain the diagnostic purpose, and obtain confirmation at that point.
- Immediately before submission, restate the title, destination, report type, and complete attachment manifest, then obtain confirmation. Submission represents the user to Apple and can transmit diagnostics, identifiers, prompts, transcripts, crash data, and other personal or confidential information.
- Do not copy seed-program material, private logs, report text, IDs, or attachments into a repository, issue tracker, shared note, or chat unless the user explicitly asks for that separate disclosure.
- Do not use undocumented Feedback Assistant protocols, automate a private API, or claim a public report-submission API exists. Apple's documented general surfaces are the app, website, and `applefeedback://` URL scheme.

## Foundation Models Attachments

Use `LanguageModelSession.logFeedbackAttachment` only for Foundation Models behavior. It serializes a structured JSON attachment containing session transcript material and feedback metadata; it does not submit a report. Read `references/foundation-models-feedback-attachments.md`, review the resulting content, save it deliberately, and attach it through Feedback Assistant only after the privacy and submission gates above.

## Outputs

- report classification and selected product/topic
- reproducibility statement and environment ledger
- report draft with expected and actual results
- attachment manifest with review status
- state: `prepared`, `staged`, `submitted`, or `blocked`
- Feedback Assistant ID and follow-up owner only when present in the live app

## References

- `references/report-quality-and-evidence.md`
- `references/live-app-and-api-boundaries.md`
- `references/foundation-models-feedback-attachments.md`
- `references/customization-flow.md`
