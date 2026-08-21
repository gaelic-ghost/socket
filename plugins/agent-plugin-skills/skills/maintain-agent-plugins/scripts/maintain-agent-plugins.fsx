#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO
open System.Text
open System.Text.Json

type ManagedFile = { Source: string; Target: string; RequiresRepoMaintenance: bool }
type Action = { Action: string; Target: string }

let scriptRoot = Path.GetFullPath(__SOURCE_DIRECTORY__)
let skillRoot = Path.GetFullPath(Path.Combine(scriptRoot, ".."))
let assetsRoot = Path.Combine(skillRoot, "assets")

let managed = [
    { Source = "agent-plugins/agent-plugins.fsx"; Target = "scripts/agent-plugins/agent-plugins.fsx"; RequiresRepoMaintenance = false }
    { Source = "agent-plugins/agent-plugins.just"; Target = "scripts/agent-plugins/agent-plugins.just"; RequiresRepoMaintenance = false }
    { Source = "repo-maintenance/validations/30-agent-plugins.fsx"; Target = "scripts/repo-maintenance/validations/30-agent-plugins.fsx"; RequiresRepoMaintenance = true }
    { Source = "repo-maintenance/syncing/20-agent-plugins.fsx"; Target = "scripts/repo-maintenance/syncing/20-agent-plugins.fsx"; RequiresRepoMaintenance = true }
]

let parseArgs argv =
    let mutable repoRoot = "."
    let mutable operation = "install"
    let rec loop args =
        match args with
        | [] -> ()
        | "--repo-root" :: value :: tail -> repoRoot <- value; loop tail
        | "--operation" :: value :: tail -> operation <- value; loop tail
        | unknown :: _ -> failwith $"Unknown argument: {unknown}"
    loop (List.ofArray argv)
    Path.GetFullPath(repoRoot), operation

let atomicWrite (path: string) (content: string) =
    let directory = Path.GetDirectoryName(path)
    Directory.CreateDirectory(directory) |> ignore
    let temporary = Path.Combine(directory, $".{Path.GetFileName(path)}.{Guid.NewGuid():N}.tmp")
    File.WriteAllText(temporary, content, UTF8Encoding(false))
    File.Move(temporary, path, true)

let ensureInside (root: string) (relative: string) =
    if Path.IsPathRooted(relative) || relative.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar) |> Array.contains ".." then
        failwith $"Managed target must be repository-relative: {relative}"
    Path.Combine(root, relative) |> Path.GetFullPath

let isGitRepository (root: string) =
    let info = ProcessStartInfo("git")
    info.WorkingDirectory <- root
    info.UseShellExecute <- false
    info.RedirectStandardOutput <- true
    info.RedirectStandardError <- true
    info.ArgumentList.Add("rev-parse")
    info.ArgumentList.Add("--show-prefix")
    use child = Process.Start(info)
    let output = child.StandardOutput.ReadToEnd().Trim()
    child.StandardError.ReadToEnd() |> ignore
    child.WaitForExit()
    child.ExitCode = 0 && String.IsNullOrWhiteSpace(output)

let copyManaged (root: string) (apply: bool) (file: ManagedFile) =
    let source = Path.Combine(assetsRoot, file.Source)
    let target = ensureInside root file.Target
    if not (File.Exists(source)) then failwith $"Managed source is missing: {source}"
    if File.Exists(target) && not ((File.GetAttributes(target) &&& FileAttributes.Directory) = enum 0) then
        failwith $"Managed target is not a regular file: {target}"
    let content = File.ReadAllText(source).Replace("\r\n", "\n")
    let action =
        if File.Exists(target) && File.ReadAllText(target).Replace("\r\n", "\n") = content then "unchanged"
        elif File.Exists(target) then "update"
        else "install"
    if apply && action <> "unchanged" then atomicWrite target content
    { Action = action; Target = file.Target }

let ensureJustImport (root: string) (apply: bool) =
    let path = Path.Combine(root, "justfile")
    let importLine = "import 'scripts/agent-plugins/agent-plugins.just'"
    let existing = if File.Exists(path) then File.ReadAllText(path).Replace("\r\n", "\n") else ""
    if existing.Contains(importLine, StringComparison.Ordinal) then { Action = "unchanged"; Target = "justfile" }
    else
        let updated = existing.TrimEnd() + (if String.IsNullOrWhiteSpace(existing) then "" else "\n\n") + "# BEGIN managed agent-plugins\n" + importLine + "\n# END managed agent-plugins\n"
        if apply then atomicWrite path updated
        { Action = (if File.Exists(path) then "update" else "install"); Target = "justfile" }

let runRuntime (root: string) (operation: string) =
    let info = ProcessStartInfo("dotnet")
    info.WorkingDirectory <- root
    info.UseShellExecute <- false
    info.RedirectStandardOutput <- true
    info.RedirectStandardError <- true
    for argument in [ "fsi"; Path.Combine(root, "scripts", "agent-plugins", "agent-plugins.fsx"); operation ] do info.ArgumentList.Add(argument)
    use child = Process.Start(info)
    let stdout = child.StandardOutput.ReadToEnd()
    let stderr = child.StandardError.ReadToEnd()
    child.WaitForExit()
    if child.ExitCode <> 0 then failwith $"Managed agent-plugin {operation} failed: {stderr.Trim()}\n{stdout.Trim()}"
    stdout.Trim()

let root, operation = parseArgs (fsi.CommandLineArgs |> Array.skip 1)
if not (Directory.Exists(root)) then failwith $"Repository root does not exist: {root}"
if not (isGitRepository root) then failwith $"Path is not the root of a Git repository: {root}"
if not (List.contains operation [ "install"; "refresh"; "report-only" ]) then failwith $"Unsupported operation: {operation}"
let apply = operation <> "report-only"
let hasRepoMaintenance = Directory.Exists(Path.Combine(root, "scripts", "repo-maintenance"))
let files = managed |> List.filter (fun file -> not file.RequiresRepoMaintenance || hasRepoMaintenance)
let actions = (files |> List.map (copyManaged root apply)) @ [ ensureJustImport root apply ]
let hasDrift = actions |> List.exists (fun action -> action.Action <> "unchanged")
let runtimeResult =
    if apply then runRuntime root "apply"
    elif hasDrift then "Managed files differ; run the installer with --operation refresh."
    else runRuntime root "check"
let report = {| status = (if operation = "report-only" && hasDrift then "drift" else "success"); operation = operation; repoRoot = root; actions = actions; result = runtimeResult |}
let options = JsonSerializerOptions(WriteIndented = true)
Console.WriteLine(JsonSerializer.Serialize(report, options))
if operation = "report-only" && hasDrift then exit 1
