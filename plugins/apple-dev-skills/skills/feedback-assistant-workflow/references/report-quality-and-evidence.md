# Feedback Report Quality and Evidence

## Report Shape

File one issue per report. Use a concise title that names the symptom and the conditions that matter, then provide:

1. Product, OS, build, hardware, and app/tool version.
2. Minimal reproduction steps that start from a known state.
3. Expected result and actual result.
4. Frequency, first known build, and last known good build when available.
5. A narrowly selected evidence manifest.

Apple recommends filing promptly because the app can collect time-sensitive diagnostics. For a UI issue, include a screenshot or recording. For an app/API issue, include a minimal sample project or focused code example when it can demonstrate the behavior.

## Crash And System Evidence

Use the Feedback Assistant app when practical: Apple documents that it automatically attaches a sysdiagnose for each report. For Mac crashes, kernel panics, hardware bugs, and printing issues, include a Mac System Information Report. Do not assume a larger log is better: keep the report focused, explain why each attachment is relevant, and review it for private data first.

## Sources

- Apple Developer, [Feedback Assistant](https://developer.apple.com/feedback-assistant/)
- Apple Support, [Feedback Assistant User Guide for Mac](https://support.apple.com/guide/feedback-assistant/welcome/mac)
