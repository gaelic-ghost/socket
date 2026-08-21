#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text
open System.Text.Encodings.Web
open System.Text.Json
open System.Text.Json.Nodes
open System.Text.RegularExpressions

let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", ".."))
let fail message = raise (InvalidOperationException(message))
let jsonOptions = JsonSerializerOptions(WriteIndented = true, Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping)

let atomicWrite (path: string) (content: string) =
    let directory = Path.GetDirectoryName(path)
    Directory.CreateDirectory(directory) |> ignore
    let temporary = Path.Combine(directory, $".{Path.GetFileName(path)}.{Guid.NewGuid():N}.tmp")
    File.WriteAllText(temporary, content, UTF8Encoding(false))
    File.Move(temporary, path, true)

let serialize (node: JsonNode) = node.ToJsonString(jsonOptions) + "\n"

let normalizePrompt (value: string) =
    let trimmed = value.Trim()
    if trimmed.Length <= 128 then trimmed else trimmed.Substring(0, 127).TrimEnd() + "…"

let requiredString (owner: string) (name: string) (node: JsonObject) =
    match node[name] with
    | null -> fail $"{owner} is missing required field {name}."
    | value ->
        let text = value.GetValue<string>()
        if String.IsNullOrWhiteSpace(text) then fail $"{owner} has an empty {name}."
        text

let objectAt (owner: string) (name: string) (node: JsonObject) =
    match node[name] with
    | :? JsonObject as value -> value
    | _ -> fail $"{owner} is missing object {name}."

let pluginRoots =
    let plugins = Path.Combine(root, "plugins")
    if Directory.Exists(plugins) then
        Directory.GetDirectories(plugins)
        |> Array.filter (fun directory -> File.Exists(Path.Combine(directory, ".codex-plugin", "plugin.json")))
        |> Array.sortWith (fun left right -> StringComparer.Ordinal.Compare(left, right))
    elif File.Exists(Path.Combine(root, ".codex-plugin", "plugin.json")) then [| root |]
    else fail $"No plugin manifests were found under {root}."

let manifestPath (pluginRoot: string) = Path.Combine(pluginRoot, ".codex-plugin", "plugin.json")
let loadObject (path: string) = JsonNode.Parse(File.ReadAllText(path)).AsObject()

let normalizeManifest (pluginRoot: string) =
    let path = manifestPath pluginRoot
    let manifest = loadObject path
    let directoryName = Path.GetFileName(pluginRoot)
    let name = requiredString path "name" manifest
    if name <> directoryName then fail $"Plugin manifest name {name} does not match directory {directoryName}."

    let author =
        match manifest["author"] with
        | :? JsonObject as value -> value
        | _ -> let value = JsonObject() in manifest["author"] <- value; value
    author["name"] <- "Gale"
    author["email"] <- "mail@galewilliams.com"
    author["url"] <- "https://github.com/gaelic-ghost"
    manifest["license"] <- "Apache-2.0"

    if manifest["homepage"] = null then
        manifest["homepage"] <- $"https://github.com/gaelic-ghost/{name}"
    if manifest["repository"] = null then
        manifest["repository"] <- $"https://github.com/gaelic-ghost/{name}"

    match manifest["hooks"] with
    | null -> ()
    | value when value.GetValue<string>() = "./hooks/hooks.json" -> manifest.Remove("hooks") |> ignore
    | _ -> ()

    match manifest["interface"] with
    | :? JsonObject as interfaceNode ->
        match interfaceNode["defaultPrompt"] with
        | :? JsonValue as prompt ->
            let prompts = JsonArray()
            prompts.Add(normalizePrompt (prompt.GetValue<string>()))
            interfaceNode["defaultPrompt"] <- prompts
        | :? JsonArray as prompts ->
            while prompts.Count > 3 do prompts.RemoveAt(prompts.Count - 1)
            for index in 0 .. prompts.Count - 1 do
                prompts[index] <- normalizePrompt (prompts[index].GetValue<string>())
        | _ -> ()
    | _ -> ()

    let updated = serialize manifest
    if File.ReadAllText(path).Replace("\r\n", "\n") <> updated then atomicWrite path updated

let ensureSocketMarketplace () =
    let path = Path.Combine(root, ".agents", "plugins", "marketplace.json")
    if File.Exists(path) then
        let marketplace = loadObject path
        let entries = marketplace["plugins"].AsArray()
        let existing =
            entries
            |> Seq.choose (fun node -> if isNull node then None else Some(node["name"].GetValue<string>()))
            |> Set.ofSeq
        for pluginRoot in pluginRoots do
            let manifest = loadObject (manifestPath pluginRoot)
            let name = manifest["name"].GetValue<string>()
            if not (existing.Contains(name)) then
                let category =
                    match manifest["interface"] with
                    | :? JsonObject as value when value["category"] <> null -> value["category"].GetValue<string>()
                    | _ -> "Developer Tools"
                let entry = JsonObject()
                entry["name"] <- name
                let source = JsonObject()
                source["source"] <- "local"
                source["path"] <- $"./plugins/{name}"
                entry["source"] <- source
                let policy = JsonObject()
                policy["installation"] <- "AVAILABLE"
                policy["authentication"] <- "ON_INSTALL"
                entry["policy"] <- policy
                entry["category"] <- category
                entries.Add(entry)
        let updated = serialize marketplace
        if File.ReadAllText(path).Replace("\r\n", "\n") <> updated then atomicWrite path updated

let ensureSkillsExport () =
    let path = Path.Combine(root, "skills.sh.json")
    if File.Exists(path) then
        let document = loadObject path
        let groupings = document["groupings"].AsArray()
        for groupingNode in groupings do
            let skills = groupingNode["skills"].AsArray()
            let staleIndexes =
                skills
                |> Seq.indexed
                |> Seq.choose (fun (index, node) ->
                    let name = node.GetValue<string>()
                    if name = "bootstrap-skills-plugin-repo" || name = "sync-skills-repo-guidance" then Some index else None)
                |> Seq.sortDescending
                |> Seq.toList
            for index in staleIndexes do skills.RemoveAt(index)
        let pluginGrouping =
            groupings
            |> Seq.tryFind (fun node -> node["title"].GetValue<string>() = "Agent Plugin Skills")
        match pluginGrouping with
        | Some grouping ->
            let skills = grouping["skills"].AsArray()
            if not (skills |> Seq.exists (fun node -> node.GetValue<string>() = "maintain-agent-plugins")) then skills.Add("maintain-agent-plugins")
        | None ->
            let grouping = JsonObject()
            grouping["title"] <- "Agent Plugin Skills"
            let skills = JsonArray()
            skills.Add("maintain-agent-plugins")
            grouping["skills"] <- skills
            groupings.Insert(0, grouping)
        let updated = serialize document
        if File.ReadAllText(path).Replace("\r\n", "\n") <> updated then atomicWrite path updated

let validateManifest (pluginRoot: string) =
    let path = manifestPath pluginRoot
    let manifest = loadObject path
    let name = requiredString path "name" manifest
    if name <> Path.GetFileName(pluginRoot) then fail $"Plugin manifest name {name} does not match its directory."
    let version = requiredString path "version" manifest
    if not (Regex.IsMatch(version, "^[0-9]+\\.[0-9]+\\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")) then fail $"Plugin {name} has invalid SemVer {version}."
    requiredString path "description" manifest |> ignore
    if requiredString path "license" manifest <> "Apache-2.0" then fail $"Plugin {name} must use Apache-2.0."
    let author = objectAt path "author" manifest
    if requiredString path "name" author <> "Gale"
       || requiredString path "email" author <> "mail@galewilliams.com"
       || requiredString path "url" author <> "https://github.com/gaelic-ghost" then
        fail $"Plugin {name} does not use the fixed Socket publisher identity."
    requiredString path "homepage" manifest |> ignore
    requiredString path "repository" manifest |> ignore
    let interfaceNode = objectAt path "interface" manifest
    for field in [ "displayName"; "shortDescription"; "longDescription"; "developerName"; "category" ] do
        requiredString path field interfaceNode |> ignore
    match interfaceNode["defaultPrompt"] with
    | null -> ()
    | :? JsonArray as prompts when prompts.Count <= 3 ->
        for prompt in prompts do
            let value = prompt.GetValue<string>()
            if String.IsNullOrWhiteSpace(value) || value.Length > 128 then fail $"Plugin {name} has an invalid default prompt."
    | :? JsonArray -> fail $"Plugin {name} has more than three default prompts."
    | _ -> fail $"Plugin {name} interface.defaultPrompt must be an array."
    if manifest["hooks"] <> null && manifest["hooks"].GetValue<string>() = "./hooks/hooks.json" then
        fail $"Plugin {name} redundantly declares the default hooks/hooks.json path."
    for field in [ "composerIcon"; "logo"; "logoDark" ] do
        match interfaceNode[field] with
        | null -> ()
        | value ->
            let relative = value.GetValue<string>().TrimStart('.', '/', '\\')
            if not (File.Exists(Path.Combine(pluginRoot, relative))) then fail $"Plugin {name} references missing {field} asset {relative}."
    if manifest["skills"] <> null then
        let relative = manifest["skills"].GetValue<string>().TrimStart('.', '/', '\\')
        let skillsRoot = Path.Combine(pluginRoot, relative)
        if not (Directory.Exists(skillsRoot)) then fail $"Plugin {name} references missing skills directory {relative}."
        if Array.isEmpty (Directory.GetFiles(skillsRoot, "SKILL.md", SearchOption.AllDirectories)) then fail $"Plugin {name} contains no SKILL.md files."

let validateSocketMarketplace () =
    let path = Path.Combine(root, ".agents", "plugins", "marketplace.json")
    if File.Exists(path) then
        let marketplace = loadObject path
        let entries = marketplace["plugins"].AsArray()
        let byName =
            entries
            |> Seq.map (fun node -> node["name"].GetValue<string>(), node.AsObject())
            |> Seq.groupBy fst
            |> Seq.map (fun (name, values) -> name, values |> Seq.map snd |> Seq.toList)
            |> Map.ofSeq
        for KeyValue(name, values) in byName do
            if values.Length <> 1 then fail $"Socket marketplace contains duplicate plugin {name}."
        for pluginRoot in pluginRoots do
            let manifest = loadObject (manifestPath pluginRoot)
            let name = manifest["name"].GetValue<string>()
            match byName.TryFind(name) with
            | None -> fail $"Socket marketplace is missing plugin {name}. Run just plugins-apply."
            | Some [ entry ] ->
                let source = objectAt name "source" entry
                if requiredString name "source" source <> "local" || requiredString name "path" source <> $"./plugins/{name}" then
                    fail $"Socket marketplace source is incorrect for {name}."
                let policy = objectAt name "policy" entry
                if requiredString name "installation" policy <> "AVAILABLE" || requiredString name "authentication" policy <> "ON_INSTALL" then
                    fail $"Socket marketplace policy is incorrect for {name}."
            | _ -> fail $"Socket marketplace contains duplicate plugin {name}."

let validateStaleExports () =
    let path = Path.Combine(root, "skills.sh.json")
    if File.Exists(path) then
        let text = File.ReadAllText(path)
        for stale in [ "bootstrap-skills-plugin-repo"; "sync-skills-repo-guidance" ] do
            if text.Contains(stale, StringComparison.Ordinal) then fail $"Stale removed skill remains exported: {stale}."

let validateAll () =
    pluginRoots |> Array.iter validateManifest
    validateSocketMarketplace ()
    validateStaleExports ()
    printfn "Validated %d agent plugin manifest(s), assets, marketplace entries, and removed-surface guards." pluginRoots.Length

let operation = fsi.CommandLineArgs |> Array.skip 1 |> Array.tryHead |> Option.defaultValue "check"
match operation with
| "check" -> validateAll ()
| "apply" ->
    pluginRoots |> Array.iter normalizeManifest
    ensureSocketMarketplace ()
    ensureSkillsExport ()
    validateAll ()
    printfn "Applied deterministic agent-plugin policy to the complete plugin set."
| _ -> fail $"Usage: agent-plugins.fsx check|apply"
