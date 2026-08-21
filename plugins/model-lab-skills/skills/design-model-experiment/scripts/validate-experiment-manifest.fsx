#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
if args.Length <> 1 then eprintfn "Usage: validate-experiment-manifest.fsx <manifest.json>"; exit 2
let required =
    [ "schema_version"; "experiment.id"; "experiment.title"; "experiment.hypothesis"; "experiment.decision"; "experiment.owner"
      "provenance.code_revision"; "provenance.model.id"; "provenance.model.revision"; "provenance.model.license"
      "provenance.tokenizer.id"; "provenance.tokenizer.revision"; "provenance.dataset.id"; "provenance.dataset.revision"
      "provenance.environment.lockfile"; "provenance.environment.hardware"; "method.controlled_variable"; "method.baseline"
      "method.treatment"; "method.seed"; "method.generation_parameters"; "evaluation.primary_metrics"; "evaluation.guardrail_metrics"
      "evaluation.failure_thresholds"; "budget.smoke_run"; "budget.full_run"; "budget.maximum_cost_usd"; "budget.stop_conditions"
      "artifacts.raw_results"; "artifacts.derived_results"; "artifacts.report"; "artifacts.sensitive_data" ]
let tryAt (root: JsonElement) (path: string) =
    ((Some root), path.Split('.')) ||> Array.fold (fun state name ->
        state |> Option.bind (fun value -> let mutable child = Unchecked.defaultof<JsonElement> in if value.TryGetProperty(name, &child) then Some child else None))
let empty (value: JsonElement) =
    value.ValueKind = JsonValueKind.Null || value.ValueKind = JsonValueKind.Undefined ||
    (value.ValueKind = JsonValueKind.String && String.IsNullOrWhiteSpace(value.GetString())) ||
    (value.ValueKind = JsonValueKind.Array && value.GetArrayLength() = 0)
let placeholder (value: JsonElement) = value.ToString().ToLowerInvariant().Contains("replace-with") || value.ToString().ToLowerInvariant().Contains("replace with")
try
    use document = JsonDocument.Parse(File.ReadAllText args[0])
    let root = document.RootElement
    let errors = ResizeArray<string>()
    for path in required do
        match tryAt root path with
        | None -> errors.Add($"Required field `{path}` is missing or empty.")
        | Some value when empty value -> errors.Add($"Required field `{path}` is missing or empty.")
        | Some value when placeholder value -> errors.Add($"Required field `{path}` still contains a template placeholder.")
        | _ -> ()
    match tryAt root "schema_version" with Some value when value.ValueKind = JsonValueKind.Number && value.GetInt32() = 1 -> () | _ -> errors.Add("`schema_version` must be the integer 1.")
    match tryAt root "method.seed" with Some value when value.ValueKind = JsonValueKind.Number -> () | _ -> errors.Add("`method.seed` must be an integer.")
    match tryAt root "artifacts.sensitive_data" with Some value when value.ValueKind = JsonValueKind.True || value.ValueKind = JsonValueKind.False -> () | _ -> errors.Add("`artifacts.sensitive_data` must be a boolean.")
    if errors.Count > 0 then errors |> Seq.iter (eprintfn "%s"); exit 1
    printfn "Experiment manifest is structurally valid: %s" args[0]
with error -> eprintfn "Experiment manifest is not valid JSON: %s" error.Message; exit 2
