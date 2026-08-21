#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO
open System.Text
open System.Text.Json

type ManagedFile = { Source: string; Target: string; Profile: string option }
type Action = { Action: string; Target: string }
type Report = {
    Status: string
    Operation: string
    Profile: string
    RepoRoot: string
    ManagedFiles: string list
    Actions: Action list
    DocumentationResult: string
    Errors: string list
}

let scriptRoot = Path.GetFullPath(__SOURCE_DIRECTORY__)
let skillRoot = Path.GetFullPath(Path.Combine(scriptRoot, ".."))
let pluginRoot = Path.GetFullPath(Path.Combine(skillRoot, "..", ".."))
let manifestPath = Path.Combine(skillRoot, "assets", "managed-assets.json")

let parseArgs argv =
    let mutable repoRoot = "."
    let mutable operation = "install"
    let mutable profile = "generic"
    let rec loop args =
        match args with
        | [] -> ()
        | "--repo-root" :: value :: tail -> repoRoot <- value; loop tail
        | "--operation" :: value :: tail -> operation <- value; loop tail
        | "--profile" :: value :: tail -> profile <- value; loop tail
        | unknown :: _ -> failwith $"Unknown argument: {unknown}"
    loop (List.ofArray argv)
    Path.GetFullPath(repoRoot), operation, profile

let loadManifest () =
    use document = JsonDocument.Parse(File.ReadAllText(manifestPath))
    if document.RootElement.GetProperty("schemaVersion").GetInt32() <> 1 then failwith "Unsupported managed-assets schema."
    document.RootElement.GetProperty("files").EnumerateArray()
    |> Seq.map (fun item ->
        let hasProfile, profile = item.TryGetProperty("profile")
        { Source = item.GetProperty("source").GetString(); Target = item.GetProperty("target").GetString(); Profile = if hasProfile then Some(profile.GetString()) else None })
    |> Seq.toList

let ensureInside (root: string) (relative: string) =
    if Path.IsPathRooted(relative) || relative.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar) |> Array.contains ".." then
        failwith $"Managed target must be repository-relative: {relative}"
    Path.Combine(root, relative) |> Path.GetFullPath

let atomicWrite (path: string) (content: string) =
    let directory = Path.GetDirectoryName(path)
    Directory.CreateDirectory(directory) |> ignore
    let temporary = Path.Combine(directory, $".{Path.GetFileName(path)}.{Guid.NewGuid():N}.tmp")
    File.WriteAllText(temporary, content, UTF8Encoding(false))
    File.Move(temporary, path, true)

let ensureJustImport (root: string) (apply: bool) =
    let path = Path.Combine(root, "justfile")
    let importLine = "import 'scripts/repo-maintenance/repo-maintenance.just'"
    let existing = if File.Exists(path) then File.ReadAllText(path).Replace("\r\n", "\n") else ""
    if existing.Contains(importLine) then None
    else
        let updated = existing.TrimEnd() + (if String.IsNullOrWhiteSpace(existing) then "" else "\n\n") + "# BEGIN managed repo-maintenance\n" + importLine + "\n# END managed repo-maintenance\n"
        if apply then atomicWrite path updated
        Some { Action = (if File.Exists(path) then "update" else "install"); Target = "justfile" }

let writeProfile (root: string) (profile: string) (apply: bool) =
    let target = "scripts/repo-maintenance/config/profile.json"
    let path = ensureInside root target
    let content = $"{{\n  \"schemaVersion\": 1,\n  \"profile\": \"{profile}\"\n}}\n"
    let action = if File.Exists(path) && File.ReadAllText(path) = content then "unchanged" elif File.Exists(path) then "update" else "install"
    if apply && action <> "unchanged" then atomicWrite path content
    { Action = action; Target = target }

let copyManaged (root: string) (apply: bool) (managed: ManagedFile) =
    let source = Path.Combine(pluginRoot, managed.Source) |> Path.GetFullPath
    if not (File.Exists(source)) then failwith $"Managed source is missing: {source}"
    let target = ensureInside root managed.Target
    let content = File.ReadAllText(source).Replace("\r\n", "\n")
    let action = if File.Exists(target) && File.ReadAllText(target).Replace("\r\n", "\n") = content then "unchanged" elif File.Exists(target) then "update" else "install"
    if apply && action <> "unchanged" then atomicWrite target content
    { Action = action; Target = managed.Target }

let runDocs (root: string) (mode: string) =
    let startInfo = ProcessStartInfo("dotnet")
    startInfo.WorkingDirectory <- root
    startInfo.UseShellExecute <- false
    startInfo.RedirectStandardOutput <- true
    startInfo.RedirectStandardError <- true
    for argument in [ "fsi"; Path.Combine(scriptRoot, "maintain-project-docs.fsx"); "--project-root"; root; "--run-mode"; mode; "--format"; "json" ] do startInfo.ArgumentList.Add(argument)
    use child = Process.Start(startInfo)
    let stdout = child.StandardOutput.ReadToEnd()
    let stderr = child.StandardError.ReadToEnd()
    child.WaitForExit()
    if child.ExitCode <> 0 then failwith $"Managed documentation {mode} failed: {stderr.Trim()}\n{stdout.Trim()}"
    if String.IsNullOrWhiteSpace(stdout) then failwith "Managed documentation returned no report."
    stdout.Trim()

let isGitRepository root =
    let startInfo = ProcessStartInfo("git")
    startInfo.WorkingDirectory <- root
    startInfo.UseShellExecute <- false
    startInfo.RedirectStandardOutput <- true
    startInfo.RedirectStandardError <- true
    for argument in [ "rev-parse"; "--show-toplevel" ] do startInfo.ArgumentList.Add(argument)
    use child = Process.Start(startInfo)
    child.StandardOutput.ReadToEnd() |> ignore
    child.StandardError.ReadToEnd() |> ignore
    child.WaitForExit()
    child.ExitCode = 0

let jsonOptions =
    let value = JsonSerializerOptions(WriteIndented = true)
    value.PropertyNamingPolicy <- JsonNamingPolicy.CamelCase
    value

let execute argv =
    try
        let root, operation, profile = parseArgs argv
        if not (Directory.Exists(root)) then failwith $"Repository root does not exist: {root}"
        if not (isGitRepository root) then failwith $"Path is not a Git repository: {root}"
        if not (List.contains operation [ "install"; "refresh"; "report-only" ]) then failwith $"Unsupported operation: {operation}"
        if not (List.contains profile [ "generic"; "xcode-workspace" ]) then failwith $"Unsupported profile: {profile}"
        let apply = operation <> "report-only"
        let managed = loadManifest () |> List.filter (fun file -> file.Profile.IsNone || file.Profile = Some profile)
        let actions = managed |> List.map (copyManaged root apply) |> ResizeArray
        actions.Add(writeProfile root profile apply)
        match ensureJustImport root apply with Some action -> actions.Add(action) | None -> ()
        let docs = runDocs root (if apply then "apply" else "check-only")
        let report = {
            Status = "success"; Operation = operation; Profile = profile; RepoRoot = root
            ManagedFiles = (managed |> List.map (fun file -> file.Target)) @ [ "scripts/repo-maintenance/config/profile.json"; "justfile" ]
            Actions = List.ofSeq actions; DocumentationResult = docs; Errors = []
        }
        Console.Out.Write(JsonSerializer.Serialize(report, jsonOptions) + "\n")
        0
    with error ->
        let report = { Status = "failed"; Operation = ""; Profile = ""; RepoRoot = ""; ManagedFiles = []; Actions = []; DocumentationResult = ""; Errors = [ error.Message ] }
        Console.Out.Write(JsonSerializer.Serialize(report, jsonOptions) + "\n")
        1

fsi.CommandLineArgs |> Array.skip 1 |> execute |> exit
