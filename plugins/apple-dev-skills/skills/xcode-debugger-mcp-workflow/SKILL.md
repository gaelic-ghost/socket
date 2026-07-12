---
name: xcode-debugger-mcp-workflow
description: Diagnose a running Apple app through Xcode’s active LLDB debugging session and assess the experimental Xcode 27 lldb-mcp executable. Use when setting breakpoints, inspecting frames or variables, issuing LLDB commands, or distinguishing a usable Xcode debugger session from an unavailable standalone debugger MCP server.
---

# Xcode Debugger MCP Workflow

## Purpose

Use Xcode's active debugger session as the stable agent-facing LLDB route. Treat the standalone `xcrun lldb-mcp` executable as experimental until it starts successfully on the selected Xcode toolchain and exposes a documented tool contract.

## Current Xcode 27 Beta 3 State

On 2026-07-12, the selected Xcode 27.0 Beta 3 toolchain (`27A5218g`) resolves both `mcpbridge` and `lldb-mcp`. `mcpbridge --help` works and documents bridge and agent export behavior. `lldb-mcp --help` fails before startup because dyld cannot resolve `@rpath/lib_CompilerSwiftIDEUtils.dylib`, even though that library exists elsewhere inside the Xcode bundle.

Do not work around this with copied libraries, symlinks, modified Xcode bundles, or a persistent loader-path override. Recheck a later Xcode beta or release before claiming standalone `lldb-mcp` support.

## Workflow

1. Classify the need: breakpoint, crash/exception, stalled thread, incorrect value, object lifetime, framework behavior, or an ordinary build/test failure.
2. For normal project execution, use `xcode-build-run-workflow` to open the project, select the destination, and run with the debugger attached. Do not attach a debugger merely to replace a build log.
3. Verify an active Xcode debug session before sending a command. If no session exists, report that prerequisite instead of inventing a process identifier or attaching to an unrelated process.
4. Use Xcode's active-session debugger command surface for focused LLDB requests: `bt`, `thread list`, `frame variable`, `po`, a named breakpoint, or a bounded step. The command shares Xcode's own LLDB state.
5. Capture the smallest evidence packet: the triggering action, stopped thread/frame, relevant variables, exception or return state, and the exact command output. Redact user content, secrets, and unnecessary memory values.
6. Hand off by evidence type: tests to `xcode-testing-workflow`, simulator trace or memgraph evidence to `ios-runtime-forensics-workflow`, device selection or capture to `xcode-device-hub-workflow`, and source repair to the owning code workflow.
7. If the request specifically requires standalone `lldb-mcp`, run a no-mutation capability probe on the selected toolchain first. If startup fails, return the loader failure and use the Xcode active-session path only when a project debug session exists.

## Guards

- Do not claim `lldb-mcp` is available merely because `xcrun --find lldb-mcp` returns a path.
- Do not modify Xcode, inject dylibs, change loader paths, or attach to arbitrary user processes to make an experimental debugger server work.
- Do not run unbounded `continue`, expression evaluation with side effects, or process-control commands without user intent and a clear debug-session owner.
- Do not treat a debugger value as a leak, performance profile, or test result without the matching runtime or test evidence.
- Do not replace Xcode's normal debugger session with an unverified third-party MCP server.

## References

- `references/beta3-capability-evidence.md`
- `references/active-session-debugging-contract.md`
