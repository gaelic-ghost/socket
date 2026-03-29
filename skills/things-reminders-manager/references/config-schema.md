# Config Schema

## Root

- `schemaVersion`: integer, currently `1`
- `isCustomized`: boolean
- `profile`: string
- `settings`: map

## settings

- `timezone`: IANA timezone string used when normalizing relative date/time requests
- `defaultReminderTime`: `HH:MM` 24-hour string used when the request omits a time
- `duplicatePolicy`: one of:
  - `update-first`
  - `ask-first`
  - `always-create`
- `onUpdateWithoutToken`: one of:
  - `block-and-report`
  - `ask-to-create-duplicate`
- `requireAbsoluteDateInConfirmation`: boolean controlling whether the final confirmation must include absolute date/time plus timezone
