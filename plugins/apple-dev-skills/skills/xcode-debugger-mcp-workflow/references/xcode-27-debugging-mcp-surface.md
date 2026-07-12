# Xcode 27 Debugging MCP Surface

## Documented Server Shapes

Xcode 27 Beta 2 release notes state that LLDB ships with `lldb-mcp` and direct readers to the LLDB MCP documentation. The same Xcode release notes say the Xcode MCP server can manipulate active run state and interact with the debugger console. Those are different server surfaces.

- Xcode MCP route: start `xcrun mcpbridge` as an MCP client's STDIO server. It connects to a running Xcode process and exposes the tools associated with that Xcode session.
- LLDB MCP route: start `lldb` and run `protocol-server start MCP listen://localhost:<port>` to host LLDB's MCP socket. An MCP client normally starts `lldb-mcp`; that helper bridges client STDIO to the socket, discovers a running LLDB MCP server, or launches its own background `lldb` when no server is available.

The public LLDB MCP contract documents one `lldb_command` tool, accepting a debugger ID and command string, plus debugger and target resources. It does not document a mechanism for choosing an Xcode-managed active debugger session. Treat the standalone route as a separately owned LLDB workflow unless actual tool output proves otherwise.

Sources:

- [Xcode 27 Beta 2 release notes](https://developer.apple.com/documentation/xcode-release-notes/xcode-27-release-notes)
- [LLDB Model Context Protocol documentation](https://lldb.llvm.org/use/mcp.html)

## Local Xcode 27 Beta 3 Result

On 2026-07-12, the selected `/Applications/Xcode-beta.app` toolchain was Xcode 27.0 build `27A5218g`. `xcrun mcpbridge --help` started and documented STDIO bridging, `MCP_XCODE_PID`, and `MCP_XCODE_SESSION_ID`. `xcrun lldb-mcp --help` exited before protocol startup because dyld could not load `@rpath/lib_CompilerSwiftIDEUtils.dylib`.

The Xcode bundle passed `codesign --verify --deep --strict`. The required library exists in the selected toolchain and the bundled LLDB framework, but `lldb-mcp` has neither location in its recorded rpath list. That is strong evidence of an Apple packaging defect in this Beta 3 helper rather than a damaged local Xcode installation or a project-level configuration problem.

Socket history also recorded a Beta 2 rpath failure when the experimental config was first added. Together, that makes a persistent Beta 2-to-Beta 3 packaging regression plausible. It is still not proof that every installation has the same defect: the public release notes announce the feature but do not list this loader failure as a known issue, and no independently reproducible public report was identified in the Apple, LLVM, and general-web sources checked on 2026-07-12.

Do not alter Xcode, copy libraries, create symlinks, or ship an environment-variable workaround. Recheck the next beta or release with the selected toolchain before changing the availability guidance.
