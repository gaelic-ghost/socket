#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO

let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let script = Path.Combine(root, "scripts", "agent-plugins", "agent-plugins.fsx")
if not (File.Exists(script)) then failwith $"Managed agent-plugin runtime is missing: {script}"

let info = ProcessStartInfo("dotnet")
info.WorkingDirectory <- root
info.UseShellExecute <- false
info.RedirectStandardOutput <- true
info.RedirectStandardError <- true
for argument in [ "fsi"; script; "apply" ] do info.ArgumentList.Add(argument)
use child = Process.Start(info)
let stdout = child.StandardOutput.ReadToEnd()
let stderr = child.StandardError.ReadToEnd()
child.WaitForExit()
if child.ExitCode <> 0 then failwith $"Agent-plugin apply failed: {stderr.Trim()}\n{stdout.Trim()}"
printfn "%s" (stdout.Trim())
