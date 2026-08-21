#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1 |> Array.toList
let value name = args |> List.tryFindIndex ((=) name) |> Option.bind (fun index -> args |> List.tryItem (index + 1))
let normalize (text: string) = String.Join(" ", text.Trim().ToLowerInvariant().Split([| ' '; '\t'; '\r'; '\n' |], StringSplitOptions.RemoveEmptyEntries))
let infer request =
    let text = normalize request
    if text.Contains("macro") || text.Contains("expansion") then Some "macro"
    elif text.Contains("trait") || text.Contains("feature flag") then Some "traits"
    elif text.Contains("command plugin") || text.Contains("plugin command") || text.Contains("format plugin") then Some "command-plugin"
    elif text.Contains("generated") || text.Contains("codegen") || text.Contains("code generation") then Some "generated-source"
    elif text.Contains("build tool plugin") || text.Contains("build plugin") || text.Contains("plugin") then Some "build-tool-plugin"
    else None
let requested = value "--repo-root" |> Option.defaultValue "." |> Path.GetFullPath
let candidate = if Directory.Exists(requested) then DirectoryInfo(requested) else FileInfo(requested).Directory
let packageRoot =
    Seq.unfold (fun (directory: DirectoryInfo) -> if isNull directory then None else Some(directory, directory.Parent)) candidate
    |> Seq.tryFind (fun directory -> File.Exists(Path.Combine(directory.FullName, "Package.swift")))
    |> Option.map (fun directory -> directory.FullName)
    |> Option.orElseWith (fun () ->
        if Directory.Exists(requested) then Directory.GetFiles(requested, "Package.swift", SearchOption.AllDirectories) |> Array.sort |> Array.tryHead |> Option.map Path.GetDirectoryName
        else None)
let extensionType = value "--extension-type" |> Option.orElseWith (fun () -> value "--request" |> Option.bind infer)
let scope = value "--toolchain-scope" |> Option.defaultValue "both"
let identity = [ if scope = "swiftly" || scope = "both" then yield! [ "swiftly use --print-location"; "swift --version" ]; if scope = "xcode" || scope = "both" then yield! [ "xcode-select -p"; "xcrun --find swift"; "xcrun swift --version" ] ]
let baseCommands kind =
    match kind with
    | "build-tool-plugin" -> [ "swift package plugin --list"; "swift package init --type build-tool-plugin" ]
    | "command-plugin" -> [ "swift package plugin --list"; "swift package plugin --help"; "swift package init --type command-plugin" ]
    | "macro" -> [ "swift package init --type macro"; "swift build"; "swift test" ]
    | "traits" -> [ "swift package show-traits --format json"; "swift build"; "swift test"; "swift build --disable-default-traits"; "swift test --disable-default-traits"; "swift build --enable-all-traits"; "swift test --enable-all-traits" ]
    | _ -> [ "swift package dump-package"; "swift build"; "swift build -v" ]
let planned = extensionType |> Option.map (fun kind -> let commands = baseCommands kind in identity @ [ if scope = "swiftly" || scope = "both" then yield! commands; if scope = "xcode" || scope = "both" then yield! commands |> List.map (fun command -> "xcrun " + command) ]) |> Option.defaultValue []
let status, next =
    if extensionType.IsNone then "blocked", "Pass --extension-type or a request identifying plugin, macro, trait, or generated-source work."
    elif not (Directory.Exists(requested) || File.Exists(requested)) then "blocked", "Resolve the requested repository path before continuing."
    elif packageRoot.IsNone then "blocked", "Use a Swift package repository containing Package.swift."
    else "success", "Proceed with the package-first extension plan."
let source = if value "--extension-type" |> Option.isSome then "explicit" elif extensionType.IsSome then "inferred" else "missing"
let context = {| requested_root = requested; package_root = packageRoot; exists = Directory.Exists(requested) || File.Exists(requested); has_package = packageRoot.IsSome |}
let support = {| minimum = "6.2"; policy = "latest stable minor plus previous stable minor" |}
let output = {| extension_type = extensionType; extension_type_source = source; package_context = context; toolchain_scope = scope; planned_commands = planned; support_window = support; next_step = next |}
let payload = {| status = status; path_type = "primary"; output = output |}
printfn "%s" (JsonSerializer.Serialize(payload, JsonSerializerOptions(WriteIndented = true)))
if status = "blocked" then exit 1
