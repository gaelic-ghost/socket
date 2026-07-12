# Active-Session Debugging Contract

The Xcode MCP surface available to this session exposes `InvokeDebuggerCommand`. It sends an LLDB command to Xcode's active debugging session, returns whether a session is active, preserves the same debugger state visible in Xcode, and reports output plus a process identifier when Xcode provides one.

Use the smallest safe command for the question:

| Question | Example command |
| --- | --- |
| Where did execution stop? | `bt` |
| Which threads exist? | `thread list` |
| What does this frame hold? | `frame variable` |
| What is one displayable value? | `po value` |
| Is a named method reached? | `breakpoint set -n Type.method` |
| Can this one line advance? | `thread step-over` |

`continue`, process signals, mutating expression evaluation, and breakpoint changes can change execution or future behavior. Use them only with an active debug-session owner and explicit user intent. Gather a fresh state after a resume or navigation command; frame and variable references can become stale.
