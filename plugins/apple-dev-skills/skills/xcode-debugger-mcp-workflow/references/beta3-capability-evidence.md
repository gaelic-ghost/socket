# Xcode 27 Beta 3 Capability Evidence

Checked locally on 2026-07-12 with the Xcode toolchain selected through Xcode Settings > Locations:

```text
xcode-select -p
/Applications/Xcode-beta.app/Contents/Developer

xcodebuild -version
Xcode 27.0
Build version 27A5218g

xcrun --find mcpbridge
/Applications/Xcode-beta.app/Contents/Developer/usr/bin/mcpbridge

xcrun --find lldb-mcp
/Applications/Xcode-beta.app/Contents/Developer/usr/bin/lldb-mcp
```

`xcrun mcpbridge --help` completed. It documents its normal STDIO Xcode MCP bridge, `run-agent`, `MCP_XCODE_PID`, `MCP_XCODE_SESSION_ID`, and `run-agent skills export`.

`xcrun lldb-mcp --help` did not start. dyld reported the unresolved `@rpath/lib_CompilerSwiftIDEUtils.dylib` dependency. A scoped `DYLD_FALLBACK_LIBRARY_PATH` probe using the matching toolchain's compiler library directory still failed with the same unresolved dependency. The library exists under the Xcode toolchain and LLDB framework, but the executable's rpath search does not reach it.

This is a local Beta 3 observation, not a claim about future Xcode releases or upstream LLVM builds.
