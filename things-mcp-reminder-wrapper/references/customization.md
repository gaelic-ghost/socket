# Customization

## Recommended default

- `timezone`: `America/New_York`
- `defaultReminderTime`: `09:30`
- `duplicatePolicy`: `update-first`
- `onUpdateWithoutToken`: `block-and-report`
- `requireAbsoluteDateInConfirmation`: `true`

## Behavior impact

- `update-first` minimizes accidental duplicate tasks.
- `ask-first` is useful when titles are reused frequently.
- `always-create` should only be used when duplicates are intentionally allowed.
- `block-and-report` avoids hidden mutation failures when token access is missing.
