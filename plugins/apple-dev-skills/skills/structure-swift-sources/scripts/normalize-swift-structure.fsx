#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json
open System.Text.RegularExpressions

let args = fsi.CommandLineArgs |> Array.skip 1
let has flag = args |> Array.contains flag
let value flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let positional = args |> Array.tryFind (fun item -> not (item.StartsWith("--")))
let root = value "--repo-path" |> Option.orElse positional |> Option.defaultValue "." |> Path.GetFullPath
if not (Directory.Exists root) then eprintfn "Swift source root does not exist: %s" root; exit 2
let ignored path = path.Split(Path.DirectorySeparatorChar) |> Array.exists (Set.ofList [ ".git"; ".build"; "DerivedData" ] |> Set.contains)
let files = Directory.GetFiles(root, "*.swift", SearchOption.AllDirectories) |> Array.filter (ignored >> not) |> Array.sort
let findings = ResizeArray<string>()
let ledger = ResizeArray<string>()
let todoPattern = Regex(@"^\s*//\s*(TODO|FIXME)\s*:?\s*(.+)$", RegexOptions.IgnoreCase)
for file in files do
    let relative = Path.GetRelativePath(root, file)
    let original = File.ReadAllText file
    let lines = original.Replace("\r\n", "\n").Split('\n')
    let expectedPrefix = $"//\n// {Path.GetFileName file}\n//\n// Purpose: Owns the {Path.GetFileNameWithoutExtension file} implementation.\n// Concern: Keep this file focused on one source-level responsibility.\n//\n"
    let hasManagedHeader = original.StartsWith("//\n// " + Path.GetFileName file + "\n//\n// Purpose:", StringComparison.Ordinal)
    if not hasManagedHeader then findings.Add($"{relative}: missing managed file header")
    let rewritten =
        lines
        |> Array.mapi (fun index line ->
            let matchValue = todoPattern.Match line
            if matchValue.Success then
                let kind = matchValue.Groups[1].Value.ToUpperInvariant()
                let message = matchValue.Groups[2].Value.Trim()
                ledger.Add($"- [ ] **{kind}** `{relative}:{index + 1}` — {message}")
                findings.Add($"{relative}:{index + 1}: inline {kind} requires ledger normalization")
                if has "--apply" then "// TODO(ledger): see TODO.md" else line
            else line)
        |> String.concat "\n"
    if has "--apply" then
        let withHeader = if hasManagedHeader then rewritten else expectedPrefix + rewritten.TrimStart('\n')
        File.WriteAllText(file, withHeader.TrimEnd() + "\n")
if has "--apply" && ledger.Count > 0 then
    let ledgerPath = Path.Combine(root, "TODO.md")
    let content = "# Source Work Ledger\n\n" + (ledger |> Seq.distinct |> Seq.sort |> String.concat "\n") + "\n"
    File.WriteAllText(ledgerPath, content)
let payload = {| status = if findings.Count = 0 || has "--apply" then "success" else "changes-required"; root = root; apply = has "--apply"; files = files.Length; findings = findings.ToArray() |}
printfn "%s" (JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)))
if findings.Count > 0 && not (has "--apply") then exit 1
