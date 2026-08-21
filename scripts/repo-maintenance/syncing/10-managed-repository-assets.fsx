#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO
open System.Text.Json

let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let installer = Path.Combine(root, "plugins", "repository-skills", "skills", "maintain-project-repo", "scripts", "maintain-project-repo.fsx")
use profileDocument = JsonDocument.Parse(File.ReadAllText(Path.Combine(root, "scripts", "repo-maintenance", "config", "profile.json")))
let profile = profileDocument.RootElement.GetProperty("profile").GetString()
let info = ProcessStartInfo("dotnet")
info.WorkingDirectory <- root
info.UseShellExecute <- false
info.RedirectStandardOutput <- true
info.RedirectStandardError <- true
for argument in [ "fsi"; installer; "--repo-root"; root; "--operation"; "refresh"; "--profile"; profile ] do info.ArgumentList.Add(argument)
use child = Process.Start info
let stdout = child.StandardOutput.ReadToEnd()
let stderr = child.StandardError.ReadToEnd()
child.WaitForExit()
if child.ExitCode <> 0 then failwith $"Managed repository asset refresh failed: {stderr.Trim()}\n{stdout.Trim()}"
printfn "Refreshed managed repository assets from repository-skills 10.0.2."
