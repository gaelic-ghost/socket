#!/usr/bin/env -S dotnet fsi

open System
open System.IO

let repositoryRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let pluginRoot = Path.Combine(repositoryRoot, "plugins", "repository-skills")

let copyTree (source: string) (target: string) =
    if not (Directory.Exists(source)) then failwith $"Repository-skills source is missing: {source}"
    Directory.CreateDirectory(target) |> ignore
    for directory in Directory.GetDirectories(source, "*", SearchOption.AllDirectories) do
        Directory.CreateDirectory(Path.Combine(target, Path.GetRelativePath(source, directory))) |> ignore
    for file in Directory.GetFiles(source, "*", SearchOption.AllDirectories) do
        let destination = Path.Combine(target, Path.GetRelativePath(source, file))
        Directory.CreateDirectory(Path.GetDirectoryName(destination)) |> ignore
        File.Copy(file, destination, true)

let replaceTree (source: string) (target: string) =
    let parent = Path.GetDirectoryName(target)
    Directory.CreateDirectory(parent) |> ignore
    let token = Guid.NewGuid().ToString("N")
    let staging = Path.Combine(parent, $".{Path.GetFileName(target)}.{token}.staging")
    let backup = Path.Combine(parent, $".{Path.GetFileName(target)}.{token}.backup")
    try
        copyTree source staging
        if Directory.Exists(target) then Directory.Move(target, backup)
        Directory.Move(staging, target)
        if Directory.Exists(backup) then Directory.Delete(backup, true)
    with error ->
        if Directory.Exists(staging) then Directory.Delete(staging, true)
        if not (Directory.Exists(target)) && Directory.Exists(backup) then Directory.Move(backup, target)
        raise error

let skillNames =
    [ "maintain-project-readme"
      "maintain-project-contributing"
      "maintain-project-agents"
      "maintain-project-roadmap"
      "maintain-project-repo" ]

for skillName in skillNames do
    replaceTree
        (Path.Combine(pluginRoot, "skills", skillName))
        (Path.Combine(repositoryRoot, "skills", skillName))

replaceTree
    (Path.Combine(pluginRoot, "shared", "project-docs"))
    (Path.Combine(repositoryRoot, "shared", "project-docs"))

printfn "Synchronized %d repository skills and the shared documentation runtime." skillNames.Length
