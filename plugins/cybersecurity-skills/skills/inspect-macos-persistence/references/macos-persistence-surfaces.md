# macOS Persistence Surfaces

Prioritize evidence-driven checks:

1. Login Items and background items visible to the user.
2. User, local, and system launch service domains and their plist files.
3. Configuration profiles and managed settings.
4. System extensions, network extensions, endpoint clients, and privileged helpers.
5. Browser extensions and native-messaging hosts.
6. Shell startup files and interpreter-specific startup hooks.
7. Package installer scripts/receipts and app-owned update helpers.
8. Scheduled jobs or legacy mechanisms only when the OS build and evidence justify them.

For every item record label, domain/scope, executable and arguments, trigger, file ownership/mode, signer/hash, load state/PID, install source, timestamps, and related logs/network. A file's presence does not prove it loaded; a running process does not prove reboot persistence.
