#!/usr/bin/env -S dotnet fsi

open System
open System.Collections.Generic
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
let valueAfter flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let optionValues = [ valueAfter "--output" ] |> List.choose id |> Set.ofList
let positional = args |> Array.filter (fun value -> not (value.StartsWith("--")) && not (optionValues.Contains value))
if positional.Length <> 2 then
    eprintfn "Usage: compare-eval-runs.fsx <baseline.jsonl> <treatment.jsonl> [--allow-partial] [--output PATH]"
    exit 2

let load path =
    let values = Dictionary<string, float>()
    File.ReadLines(path)
    |> Seq.iteri (fun index line ->
        if not (String.IsNullOrWhiteSpace line) then
            use document = JsonDocument.Parse line
            let root = document.RootElement
            let mutable idElement = Unchecked.defaultof<JsonElement>
            let mutable scoreElement = Unchecked.defaultof<JsonElement>
            if not (root.TryGetProperty("id", &idElement)) || idElement.ValueKind <> JsonValueKind.String || String.IsNullOrWhiteSpace(idElement.GetString()) then
                failwith $"{path}:{index + 1} requires a non-empty string `id`."
            if not (root.TryGetProperty("score", &scoreElement)) || scoreElement.ValueKind <> JsonValueKind.Number then
                failwith $"{path}:{index + 1} requires a finite numeric `score`."
            let identifier = idElement.GetString()
            let score = scoreElement.GetDouble()
            if not (Double.IsFinite score) then failwith $"{path}:{index + 1} requires a finite numeric `score`."
            if values.ContainsKey identifier then failwith $"{path}:{index + 1} repeats evaluation id `{identifier}`."
            values.Add(identifier, score))
    if values.Count = 0 then failwith $"{path} contains no evaluation results."
    values

try
    let baseline = load positional[0]
    let treatment = load positional[1]
    let baselineIds = baseline.Keys |> Set.ofSeq
    let treatmentIds = treatment.Keys |> Set.ofSeq
    let shared = Set.intersect baselineIds treatmentIds |> Set.toArray |> Array.sort
    let partial = baselineIds <> treatmentIds
    if shared.Length = 0 then failwith "Evaluation comparison found no shared case ids."
    if partial && not (args |> Array.contains "--allow-partial") then failwith "Evaluation runs must contain identical case ids; pass --allow-partial only for a diagnostic comparison."
    let cases = shared |> Array.map (fun id -> let delta = treatment[id] - baseline[id] in {| id = id; baseline = baseline[id]; treatment = treatment[id]; delta = delta |})
    let payload =
        {| baseline_count = baseline.Count
           treatment_count = treatment.Count
           paired_count = shared.Length
           partial_comparison = partial
           baseline_only = Set.difference baselineIds treatmentIds |> Set.toArray |> Array.sort
           treatment_only = Set.difference treatmentIds baselineIds |> Set.toArray |> Array.sort
           mean_paired_delta = cases |> Array.averageBy _.delta
           improved = cases |> Array.filter (fun item -> item.delta > 0.0) |> Array.length
           unchanged = cases |> Array.filter (fun item -> item.delta = 0.0) |> Array.length
           regressed = cases |> Array.filter (fun item -> item.delta < 0.0) |> Array.length
           cases = cases |}
    let rendered = JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)) + "\n"
    match valueAfter "--output" with
    | Some path -> File.WriteAllText(path, rendered); printfn "Wrote paired evaluation comparison: %s" path
    | None -> printf "%s" rendered
with error ->
    eprintfn "Evaluation comparison could not load its inputs: %s" error.Message
    exit 2
