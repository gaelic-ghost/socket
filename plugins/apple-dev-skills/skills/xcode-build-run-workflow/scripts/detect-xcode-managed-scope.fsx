#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let requested = fsi.CommandLineArgs |> Array.skip 1 |> Array.tryHead |> Option.defaultValue "."
let root = Path.GetFullPath(requested)
let markers =
    if not (Directory.Exists(root)) then [||]
    else
        Directory.EnumerateFileSystemEntries(root, "*", SearchOption.AllDirectories)
        |> Seq.filter (fun path ->
            let depth = Path.GetRelativePath(root, path).Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar).Length
            depth <= 4 && (path.EndsWith(".xcodeproj") || path.EndsWith(".xcworkspace") || path.EndsWith(".pbxproj")))
        |> Seq.truncate 20
        |> Seq.toArray
let payload = {| managed = not (Array.isEmpty markers); path = requested; markers = markers |}
printfn "%s" (JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)))
