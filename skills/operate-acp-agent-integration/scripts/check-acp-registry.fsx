#!/usr/bin/env -S dotnet fsi

open System
open System.Net.Http
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1 |> Array.toList
let optionValue name = args |> List.tryFindIndex ((=) name) |> Option.bind (fun index -> args |> List.tryItem(index + 1))
let positional = args |> List.filter (fun value -> not (value.StartsWith("--")) && Some value <> optionValue "--registry-url" && Some value <> optionValue "--format")
let query = positional |> List.tryHead |> Option.defaultWith (fun () -> failwith "Pass an exact ACP agent id or display name.")
let url = optionValue "--registry-url" |> Option.defaultValue "https://cdn.agentclientprotocol.com/registry/v1/latest/registry.json"
let format = optionValue "--format" |> Option.defaultValue "text"

let client = new HttpClient(Timeout = TimeSpan.FromSeconds(15.0))
client.DefaultRequestHeaders.UserAgent.ParseAdd("socket-acp-registry-check/1")
let content = client.GetStringAsync(url).GetAwaiter().GetResult()
let document = JsonDocument.Parse(content)
let root = document.RootElement
let mutable agents = Unchecked.defaultof<JsonElement>
if not (root.TryGetProperty("agents", &agents)) || agents.ValueKind <> JsonValueKind.Array then
    failwith $"The ACP registry response from {url} does not contain an agents array."
let matches =
    agents.EnumerateArray()
    |> Seq.filter (fun (agent: JsonElement) ->
        let exact (property: string) =
            let mutable value = Unchecked.defaultof<JsonElement>
            agent.TryGetProperty(property, &value) && value.ValueKind = JsonValueKind.String && String.Equals(value.GetString(), query, StringComparison.OrdinalIgnoreCase)
        exact "id" || exact "name")
    |> Seq.toArray
let version = let mutable value = Unchecked.defaultof<JsonElement> in if root.TryGetProperty("version", &value) then value.ToString() else ""
if format = "json" then
    let serializedMatches = matches |> Array.map (fun item -> JsonSerializer.Deserialize<JsonElement>(item.GetRawText()))
    let payload = {| query = query; registry_url = url; registry_version = version; present = not (Array.isEmpty matches); matches = serializedMatches |}
    printfn "%s" (JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)))
elif Array.isEmpty matches then
    printfn "ACP Registry does not currently contain an exact id or name match for '%s'." query
else
    for agent in matches do
        let field (name: string) fallback = let mutable value = Unchecked.defaultof<JsonElement> in if agent.TryGetProperty(name, &value) then value.ToString() else fallback
        printfn "ACP Registry contains %s (%s) at version %s." (field "name" "(unnamed)") (field "id" "(no id)") (field "version" "(unknown)")
if Array.isEmpty matches then exit 1
