# Config Schema

## Root

- `schemaVersion`: integer, currently `1`
- `isCustomized`: boolean
- `profile`: string
- `settings`: map

## settings

- `timezone`: IANA timezone string
- `defaultReminderTime`: `HH:MM` 24-hour string
- `duplicatePolicy`: one of:
  - `update-first`
  - `ask-first`
  - `always-create`
- `onUpdateWithoutToken`: one of:
  - `block-and-report`
  - `ask-to-create-duplicate`
- `requireAbsoluteDateInConfirmation`: boolean
