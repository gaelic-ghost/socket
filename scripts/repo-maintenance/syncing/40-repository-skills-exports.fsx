#!/usr/bin/env -S dotnet fsi

open System
open System.IO

let repositoryRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let pluginsRoot = Path.Combine(repositoryRoot, "plugins")

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

let exportedSkills =
    Directory.GetDirectories(Path.Combine(repositoryRoot, "skills"))
    |> Array.filter (fun directory -> File.Exists(Path.Combine(directory, "SKILL.md")))
    |> Array.sort
for target in exportedSkills do
    let skillName = Path.GetFileName(target)
    let source =
        let candidates = Directory.GetDirectories(pluginsRoot) |> Array.map (fun plugin -> Path.Combine(plugin, "skills", skillName)) |> Array.filter Directory.Exists
        match candidates with
        | [| only |] -> only
        | [||] -> failwith $"Root skill export has no owning plugin source: {skillName}"
        | many ->
            let rendered = String.concat ", " many
            failwith $"Root skill export has ambiguous owners: {skillName} ({rendered})"
    replaceTree source target

replaceTree
    (Path.Combine(pluginsRoot, "repository-skills", "shared", "project-docs"))
    (Path.Combine(repositoryRoot, "shared", "project-docs"))

printfn "Synchronized %d managed root skill exports and the shared documentation runtime." exportedSkills.Length
