# Mutation Risk Policy for Xcode-Managed Projects

## Safe direct-edit states

Treat direct source and project-adjacent filesystem edits as safe when either of these is true:
- Xcode is closed
- Xcode is open, but the current project or workspace being edited is not open in Xcode

These safe states also allow normal CLI workflows such as `xcodebuild`, `swift`, and `xcrun`.

## Direct `.pbxproj` warning path

Direct `.pbxproj` edits are the only mutation path that still requires an explicit warning.

Before directly editing `.pbxproj`:
- warn the user that project-file corruption or membership drift is possible
- prefer Xcode MCP mutation tools or user-performed Xcode UI changes first when they are practical
- require explicit user approval before continuing with the direct `.pbxproj` edit

Do not apply this warning path to ordinary source edits, asset edits, package work, or other direct filesystem changes that do not touch `.pbxproj`.
