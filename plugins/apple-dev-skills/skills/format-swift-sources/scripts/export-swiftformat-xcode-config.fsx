#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
let value flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let run executable arguments =
    let info = ProcessStartInfo(executable)
    info.UseShellExecute <- false; info.RedirectStandardOutput <- true; info.RedirectStandardError <- true
    arguments |> List.iter info.ArgumentList.Add
    use child = Process.Start info
    let stdout = child.StandardOutput.ReadToEnd()
    let stderr = child.StandardError.ReadToEnd()
    child.WaitForExit()
    if child.ExitCode <> 0 then failwith (if String.IsNullOrWhiteSpace stderr then stdout else stderr)
    stdout
let suite = value "--suite-domain" |> Option.defaultValue "com.charcoaldesign.SwiftFormat"
let json =
    match value "--input-plist" with
    | Some path -> run "plutil" [ "-convert"; "json"; "-o"; "-"; path ]
    | None ->
        let plist = run "defaults" [ "export"; suite; "-" ]
        let temporary = Path.GetTempFileName()
        try
            File.WriteAllText(temporary, plist)
            run "plutil" [ "-convert"; "json"; "-o"; "-"; temporary ]
        finally File.Delete temporary
use document = JsonDocument.Parse json
let root = document.RootElement
let mapping (name: string) = let mutable item = Unchecked.defaultof<JsonElement> in if root.TryGetProperty(name, &item) && item.ValueKind = JsonValueKind.Object then item.EnumerateObject() |> Seq.toArray else [||]
let enabled = mapping "rules" |> Array.filter (fun item -> item.Value.ValueKind = JsonValueKind.True) |> Array.map _.Name |> Array.sort
let mutable infer = Unchecked.defaultof<JsonElement>
let inferOptions = not (root.TryGetProperty("infer-options", &infer)) || infer.ValueKind = JsonValueKind.True
let versions = Set.ofList [ "swiftversion"; "swift-version"; "languagemode"; "language-mode" ]
let options =
    mapping "format-options"
    |> Array.filter (fun item -> not inferOptions || versions.Contains item.Name)
    |> Array.map (fun item -> item.Name, item.Value.ToString())
    |> Array.filter (fun (name, value) -> not (String.IsNullOrWhiteSpace value) && not (versions.Contains name && Set.ofList [ "0"; "auto"; "undefined" ] |> Set.contains (value.ToLowerInvariant())))
    |> Array.sortBy fst
let lines = ResizeArray [ "# Generated from SwiftFormat for Xcode shared defaults."; $"# Source suite: {suite}"; "" ]
if enabled.Length > 0 then lines.Add("--rules " + String.concat "," enabled)
for name, raw in options do
    let value = if raw.IndexOfAny([|' '; '"'|]) >= 0 then "\"" + raw.Replace("\"", "\\\"") + "\"" else raw
    lines.Add($"--{name} {value}")
if enabled.Length = 0 && options.Length = 0 then lines.Add("# No explicit rules or exportable options were found.")
let rendered = String.concat "\n" lines + "\n"
match value "--output" with Some path -> File.WriteAllText(path, rendered) | None -> printf "%s" rendered
