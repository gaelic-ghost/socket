#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let arguments = fsi.CommandLineArgs |> Array.skip 1
let has flag = arguments |> Array.contains flag
let value flag = arguments |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < arguments.Length then Some arguments[index + 1] else None)
let skill = DirectoryInfo(Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))).Name
let start =
    [ value "--repo-root"; value "--repo-path"; value "--workspace-path" ]
    |> List.choose id
    |> List.tryHead
    |> Option.defaultValue (Directory.GetCurrentDirectory())
    |> Path.GetFullPath

let rec nearestWith marker (directory: DirectoryInfo) =
    if File.Exists(Path.Combine(directory.FullName, marker)) || Directory.GetDirectories(directory.FullName, marker).Length > 0 then Some directory.FullName
    elif isNull directory.Parent then None
    else nearestWith marker directory.Parent

let packageRoot = nearestWith "Package.swift" (DirectoryInfo start)
let xcodeRoot =
    match value "--workspace-path" with
    | Some path -> Some(Path.GetFullPath path)
    | None -> nearestWith "*.xcworkspace" (DirectoryInfo start) |> Option.orElseWith (fun () -> nearestWith "*.xcodeproj" (DirectoryInfo start))
let operation = value "--operation-type" |> Option.orElseWith (fun () -> value "--cleanup-kind") |> Option.orElseWith (fun () -> value "--task-type") |> Option.defaultValue "inspect"
let request = value "--request" |> Option.defaultValue ""
let directEdit = has "--direct-pbxproj-edit"
let optedIn = has "--direct-pbxproj-edit-opt-in"

let surface, root, commands =
    if skill.StartsWith("swift-package-", StringComparison.Ordinal) then
        "swift-package", packageRoot, [| "swift package describe"; if skill.Contains("testing") then "swift test" else "swift build" |]
    elif skill.StartsWith("xcode-", StringComparison.Ordinal) then
        "xcode", xcodeRoot, [| "Xcode MCP first"; "xcodebuild only as the documented fallback" |]
    elif skill = "author-swift-docc-docs" then
        "documentation", packageRoot |> Option.orElse xcodeRoot, [| "author or review DocC sources"; if has "--needs-generation" then "generate documentation with the owning SwiftPM or Xcode surface" |]
    elif skill = "structure-swift-sources" then
        "source-structure", Some start, [| "inventory Swift source structure"; "apply managed headers and TODO/FIXME ledgers only when explicitly requested" |]
    else "apple-workflow", Some start, [| "inspect the owning project surface" |]

let blockedReason =
    if directEdit && not optedIn then Some "Direct project.pbxproj editing requires the explicit --direct-pbxproj-edit-opt-in flag."
    elif root.IsNone then Some $"{skill} could not locate its required project surface from {start}."
    else None
let payload =
    {| status = if blockedReason.IsSome then "blocked" else "success"
       skill = skill
       execution_surface = surface
       root = root
       operation = operation
       request = request
       dry_run = has "--dry-run"
       policy = {| customization = "fixed"; mcp_first = surface = "xcode"; direct_pbxproj_edit = directEdit && optedIn |}
       commands = commands
       error = blockedReason |}
printfn "%s" (JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)))
if blockedReason.IsSome then exit 2
