#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO
open System.Text.Json

let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let fail message = raise (InvalidOperationException(message))

let readJson path = JsonDocument.Parse(File.ReadAllText(path))
let relative path = Path.GetRelativePath(root, path)

let marketplacePath = Path.Combine(root, ".agents", "plugins", "marketplace.json")
let marketplace = readJson marketplacePath
let entries = marketplace.RootElement.GetProperty("plugins").EnumerateArray() |> Seq.toList
let names = entries |> List.map (fun item -> item.GetProperty("name").GetString())
let duplicateNames = names |> List.countBy id |> List.choose (fun (name, count) -> if count > 1 then Some name else None)
if not (List.isEmpty duplicateNames) then
    let rendered = String.concat ", " duplicateNames
    fail $"Socket marketplace has duplicate plugin names: {rendered}"

let mutable sharedVersion: string option = None
for entry in entries do
    let name = entry.GetProperty("name").GetString()
    let source = entry.GetProperty("source")
    if source.GetProperty("source").GetString() = "local" then
        let sourcePath = source.GetProperty("path").GetString()
        let pluginRoot = Path.GetFullPath(Path.Combine(root, sourcePath))
        if not (Directory.Exists(pluginRoot)) then fail $"Marketplace plugin {name} is missing at {sourcePath}."
        let manifestPath = Path.Combine(pluginRoot, ".codex-plugin", "plugin.json")
        if not (File.Exists(manifestPath)) then fail $"Marketplace plugin {name} has no .codex-plugin/plugin.json."
        use manifest = readJson manifestPath
        if manifest.RootElement.GetProperty("name").GetString() <> name then fail $"Marketplace and manifest names differ for {name}."
        let version = manifest.RootElement.GetProperty("version").GetString()
        match sharedVersion with
        | None -> sharedVersion <- Some version
        | Some expected when version <> expected -> fail $"Plugin {name} is version {version}; expected {expected}."
        | _ -> ()

let claudePath = Path.Combine(root, ".claude-plugin", "marketplace.json")
let claude = readJson claudePath
let claudeNames =
    claude.RootElement.GetProperty("plugins").EnumerateArray()
    |> Seq.map (fun item -> item.GetProperty("name").GetString())
    |> Set.ofSeq
let unknownClaude = Set.difference claudeNames (Set.ofList names)
if not (Set.isEmpty unknownClaude) then
    let rendered = String.concat ", " unknownClaude
    fail $"Claude marketplace references plugins absent from Socket: {rendered}"

let nestedTests =
    Directory.GetFiles(root, "*", SearchOption.AllDirectories)
    |> Array.filter (fun path ->
        let rel = relative path
        let parts = rel.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
        not (parts |> Array.exists (fun part -> part = ".git" || part = ".venv" || part = ".codex"))
        && parts.Length > 1
        && parts[0] <> "tests"
        && (parts |> Array.exists (fun part -> part = "test" || part = "tests")))
if not (Array.isEmpty nestedTests) then fail $"Tests must live only at Socket root; found {relative nestedTests[0]}."

let repositorySkillRoot = Path.Combine(root, "plugins", "repository-skills")
let legacyRepositoryScripts =
    Directory.GetFiles(repositorySkillRoot, "*", SearchOption.AllDirectories)
    |> Array.filter (fun path -> path.EndsWith(".py") || path.EndsWith(".sh"))
if not (Array.isEmpty legacyRepositoryScripts) then fail $"Repository Skills contains a legacy script: {relative legacyRepositoryScripts[0]}."

printfn "Socket marketplace integration, compatibility wiring, root-only tests, and repository-skills automation are valid."
