#!/usr/bin/env -S dotnet fsi

open System.Diagnostics
open System.IO

let pluginRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))
let info = ProcessStartInfo("node")
info.WorkingDirectory <- pluginRoot
info.UseShellExecute <- false
info.ArgumentList.Add(Path.Combine(pluginRoot, "scripts", "session-start-hook.mjs"))
use child = Process.Start(info)
child.WaitForExit()
exit child.ExitCode
