#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
let has flag = args |> Array.contains flag
let value flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let mode = value "--mode" |> Option.defaultValue "explore"
let query = value "--query"
let request = value "--docset-request"
let preferred = value "--preferred-source" |> Option.defaultValue "auto"
let mcpFailed = value "--mcp-failure-reason" |> Option.isSome
let source =
    if preferred <> "auto" then Some preferred
    elif not mcpFailed then Some "xcode-mcp-docs"
    else Some "dash"
let blocked = mode = "explore" && query.IsNone || mode <> "explore" && request.IsNone || mode = "dash-install" && not (has "--yes" || has "--dry-run")
let next =
    if mode = "explore" && query.IsNone then "Provide --query."
    elif mode <> "explore" && request.IsNone then "Provide --docset-request."
    elif mode = "dash-install" && not (has "--yes" || has "--dry-run") then "Rerun with --yes to authorize the Dash install side effect."
    elif mode = "dash-install" then "Install the selected catalog match in Dash, then return to explore mode."
    elif mode = "dash-generate" then "Generate a deterministic Dash docset only after confirming no existing source is available."
    elif source = Some "xcode-mcp-docs" then "Use Xcode MCP DocumentationSearch first."
    elif source = Some "dash" then "Use Dash MCP, then its localhost HTTP API if MCP is unavailable."
    elif source = Some "source-repo" then "Use checked-out source, generated DocC, or the canonical source repository."
    else "Use readable official Apple or Swift documentation."
let payload =
    {| status = if blocked then "blocked" else "success"
       mode = mode
       query = query
       docset_request = request
       source_used = source
       source_order = [| "xcode-mcp-docs"; "dash"; "dash-http"; "source-repo"; "official-web" |]
       policy = {| customization = "fixed"; install_requires_yes = true; snippets_are_not_evidence = true |}
       dry_run = has "--dry-run"
       next_step = next |}
printfn "%s" (JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)))
if blocked then exit 1
