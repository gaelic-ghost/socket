# Mutation via MCP

Preferred mutation order:

1. Use Xcode MCP mutation tools.
2. Verify each mutation with read/search tools.
3. If a broad older prompt lands on this compatibility surface and the work is really mutation-related, route to `$xcode-build-run-workflow` for the direct `.pbxproj` warning gate.

Never jump directly to raw file edits in Xcode-managed scope without safety gate completion.
