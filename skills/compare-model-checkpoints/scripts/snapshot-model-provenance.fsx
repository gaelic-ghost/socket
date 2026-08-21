#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Security.Cryptography
open System.Text
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
let valueAfter flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let positional = args |> Array.filter (fun value -> not (value.StartsWith("--")) && not (args |> Array.exists (fun flag -> (flag = "--model-id" || flag = "--revision" || flag = "--output") && valueAfter flag = Some value)))
if positional.Length <> 1 then
    eprintfn "Usage: snapshot-model-provenance.fsx <artifact> [--model-id ID] [--revision REVISION] [--output PATH]"
    exit 2

let artifact = Path.GetFullPath(positional[0])
if not (File.Exists artifact || Directory.Exists artifact) then
    eprintfn "Model artifact does not exist: %s" artifact
    exit 2

let output = valueAfter "--output" |> Option.map Path.GetFullPath
match output with
| Some path when path = artifact || (Directory.Exists artifact && path.StartsWith(artifact + string Path.DirectorySeparatorChar, StringComparison.Ordinal)) ->
    eprintfn "Provenance output must not overwrite or be inside the model artifact: %s" path
    exit 2
| _ -> ()

let digest path =
    use stream = File.OpenRead path
    SHA256.HashData(stream) |> Convert.ToHexString |> fun value -> value.ToLowerInvariant()

let files =
    if File.Exists artifact then [| artifact |]
    else Directory.GetFiles(artifact, "*", SearchOption.AllDirectories) |> Array.sort
let entries =
    files
    |> Array.map (fun path ->
        let name = if File.Exists artifact then Path.GetFileName path else Path.GetRelativePath(artifact, path)
        {| path = name; bytes = FileInfo(path).Length; sha256 = digest path |})
let aggregateText = entries |> Array.map (fun entry -> $"{entry.path}\000{entry.sha256}\n") |> String.concat ""
let aggregate = SHA256.HashData(Encoding.UTF8.GetBytes aggregateText) |> Convert.ToHexString |> fun value -> value.ToLowerInvariant()
let payload =
    {| artifact = artifact
       kind = if File.Exists artifact then "file" else "directory"
       model_id = valueAfter "--model-id"
       revision = valueAfter "--revision"
       file_count = entries.Length
       total_bytes = entries |> Array.sumBy _.bytes
       inventory_sha256 = aggregate
       files = entries |}
let rendered = JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)) + "\n"
match output with
| Some path ->
    Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
    File.WriteAllText(path, rendered)
    printfn "Wrote model provenance snapshot: %s" path
| None -> printf "%s" rendered
