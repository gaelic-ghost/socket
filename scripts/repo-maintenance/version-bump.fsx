#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text
open System.Text.Json
open System.Text.RegularExpressions

let repoRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", ".."))
let version =
    match fsi.CommandLineArgs |> Array.skip 1 with
    | [| value |] when Regex.IsMatch(value, "^(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)\\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?$") -> value
    | [| value |] -> failwith $"Release version must use SemVer syntax without a v prefix: {value}"
    | _ -> failwith "Usage: version-bump.fsx X.Y.Z"

let manifests =
    Directory.GetFiles(Path.Combine(repoRoot, "plugins"), "plugin.json", SearchOption.AllDirectories)
    |> Array.filter (fun path -> path.Contains($"{Path.DirectorySeparatorChar}.codex-plugin{Path.DirectorySeparatorChar}"))
    |> Array.filter (fun path -> not (path.Contains($"{Path.DirectorySeparatorChar}SpeakSwiftlyServer{Path.DirectorySeparatorChar}")))
    |> Array.sortWith (fun left right -> StringComparer.Ordinal.Compare(left, right))

if Array.isEmpty manifests then failwith "No Socket-owned plugin manifests were found."

let updates =
    manifests
    |> Array.map (fun path ->
        use document = JsonDocument.Parse(File.ReadAllText(path))
        let current = document.RootElement.GetProperty("version").GetString()
        let lines = File.ReadAllText(path).Replace("\r\n", "\n").Split('\n')
        let updated =
            lines
            |> Array.map (fun line ->
                if Regex.IsMatch(line, "^\\s*\"version\"\\s*:") then
                    Regex.Replace(line, "\"version\"\\s*:\\s*\"[^\"]+\"", $"\"version\": \"{version}\"")
                else line)
            |> String.concat "\n"
        path, current, updated)

for path, current, updated in updates do
    if current <> version then
        let temporary = path + $".{Guid.NewGuid():N}.tmp"
        File.WriteAllText(temporary, updated, UTF8Encoding(false))
        File.Move(temporary, path, true)
        printfn "Updated %s: %s -> %s" (Path.GetRelativePath(repoRoot, path)) current version

printfn "Socket plugin versions are aligned at %s across %d manifests." version manifests.Length
