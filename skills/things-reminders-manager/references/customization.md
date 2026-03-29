# Customization

## Recommended default

- `timezone`: `America/New_York`
- `defaultReminderTime`: `09:30`
- `duplicatePolicy`: `update-first`
- `onUpdateWithoutToken`: `block-and-report`
- `requireAbsoluteDateInConfirmation`: `true`

## Workflow impact

- `timezone` controls how relative dates are normalized into absolute confirmations.
- `defaultReminderTime` supplies the time component when the request gives a date but no explicit time.
- `update-first` minimizes accidental duplicate tasks by preferring updates on a single clear match.
- `ask-first` pauses when a plausible duplicate exists and asks the user to choose.
- `always-create` should only be used when duplicates are intentionally allowed.
- `block-and-report` stops the workflow when update auth is missing.
- `ask-to-create-duplicate` keeps the workflow moving by asking whether a new task should be created instead.
- `requireAbsoluteDateInConfirmation=true` makes the final confirmation include the absolute date/time and timezone.
