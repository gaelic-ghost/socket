#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
let has flag = args |> Array.contains flag
let value flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let operation = value "--operation" |> Option.defaultValue "create"
let name = value "--name" |> Option.orElseWith (fun () -> value "--component-name")
let repo =
    match value "--repo-root", name with
    | Some path, _ -> Path.GetFullPath path
    | None, Some product -> Path.GetFullPath(Path.Combine(value "--destination" |> Option.defaultValue ".", product))
    | _ -> Path.GetFullPath "."
let dryRun = has "--dry-run"
let blocked message =
    printfn "%s" (JsonSerializer.Serialize({| status = "blocked"; operation = operation; workspace_root = repo; error = message |}, JsonSerializerOptions(WriteIndented = true)))
    exit 2
let write (relative: string) (content: string) =
    let path = Path.Combine(repo, relative)
    Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
    File.WriteAllText(path, content.Replace("\r\n", "\n"))
let copyManaged (asset: string) (relative: string) =
    let source = Path.Combine(__SOURCE_DIRECTORY__, "..", "assets", "managed-guidance", asset)
    let target = Path.Combine(repo, relative)
    Directory.CreateDirectory(Path.GetDirectoryName target) |> ignore
    File.Copy(source, target, true)
let ensureCanonicalRoot () =
    [ "Apps"; "Packages"; "Services"; "Configurations"; "docs"; "Scripts"; ".github/workflows" ] |> List.iter (fun path -> Directory.CreateDirectory(Path.Combine(repo, path)) |> ignore)
    let product = name |> Option.defaultValue (DirectoryInfo(repo).Name)
    write "project.yml" $"name: {product}\noptions:\n  bundleIdPrefix: com.galewilliams\nconfigs:\n  Debug: debug\n  Staging: release\n  Release: release\n  AppStore: release\n  DirectDistribution: release\n  AltStore: release\ninclude:\n  - path: Apps/apps-shared.yml\n  - path: Packages/packages-shared.yml\n  - path: Services/services-shared.yml\n"
    write "Apps/apps-shared.yml" "targets: {}\n"
    write "Packages/packages-shared.yml" "packages: {}\n"
    write "Services/services-shared.yml" "packages: {}\n"
    write $"{product}.xcworkspace/contents.xcworkspacedata" $"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Workspace version=\"1.0\"><FileRef location=\"group:{product}.xcodeproj\"></FileRef></Workspace>\n"
    copyManaged "AGENTS-root.md" "AGENTS.md"
    copyManaged "AGENTS-apps.md" "Apps/AGENTS.md"
    copyManaged "AGENTS-packages.md" "Packages/AGENTS.md"
    copyManaged "AGENTS-services.md" "Services/AGENTS.md"
    copyManaged "CONTRIBUTING.md" "CONTRIBUTING.md"
    copyManaged "pre-commit" ".git/hooks/pre-commit"
    write "justfile" "setup:\n    xcodegen generate\n\nalign:\n    dotnet fsi .socket/repo-maintenance/repo-maintenance.fsx sync\n    xcodegen generate\n"
let addComponent () =
    let componentName = value "--component-name" |> Option.defaultWith (fun () -> blocked "--component-name is required for add-component.")
    let kind = value "--component-kind" |> Option.defaultWith (fun () -> blocked "--component-kind is required for add-component.")
    match kind with
    | "library" | "service" ->
        let rootName = if kind = "library" then "Packages" else "Services"
        let target = Path.Combine(rootName, componentName)
        Directory.CreateDirectory(Path.Combine(repo, target, "Sources", componentName)) |> ignore
        write (Path.Combine(target, "Package.swift")) $"// swift-tools-version: 6.2\nimport PackageDescription\nlet package = Package(name: \"{componentName}\", platforms: [.macOS(.v15)], products: [.library(name: \"{componentName}\", targets: [\"{componentName}\"])], targets: [.target(name: \"{componentName}\")])\n"
    | "app" | "extension" ->
        let target = Path.Combine("Apps", componentName)
        Directory.CreateDirectory(Path.Combine(repo, target, "Sources")) |> ignore
        let platform = value "--platform" |> Option.defaultValue "iOS"
        write (Path.Combine(target, "target.yml")) $"targets:\n  {componentName}:\n    type: application\n    platform: {platform}\n    sources: [Sources]\n"
    | other -> blocked $"Unsupported component kind: {other}"

if operation = "create" && name.IsNone then blocked "--name is required for create."
if operation <> "create" && not (Directory.Exists repo) then blocked $"Repository does not exist: {repo}"
if operation = "create" && Directory.Exists repo && Directory.EnumerateFileSystemEntries(repo) |> Seq.isEmpty |> not then blocked $"Create destination is not empty: {repo}"
if operation = "adopt" && not (has "--apply") then
    let components = Directory.GetFiles(repo, "Package.swift", SearchOption.AllDirectories) |> Array.map (fun path -> Path.GetRelativePath(repo, Path.GetDirectoryName path)) |> Array.sort
    printfn "%s" (JsonSerializer.Serialize({| status = "success"; operation = operation; workspace_root = repo; components = components; migration_required = true; next_step = "Review the inventory, then rerun with --apply and an approved adoption map." |}, JsonSerializerOptions(WriteIndented = true)))
elif dryRun then
    printfn "%s" (JsonSerializer.Serialize({| status = "success"; operation = operation; workspace_root = repo; dry_run = true; policy = "fixed-gale-workspace" |}, JsonSerializerOptions(WriteIndented = true)))
else
    if operation = "create" || operation = "align" || operation = "adopt" then ensureCanonicalRoot ()
    if operation = "add-component" then addComponent ()
    printfn "%s" (JsonSerializer.Serialize({| status = "success"; operation = operation; workspace_root = repo; policy = "fixed-gale-workspace"; next_step = "Run just setup, then use just align for managed refreshes." |}, JsonSerializerOptions(WriteIndented = true)))
