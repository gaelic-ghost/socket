#!/usr/bin/env -S dotnet fsi

open System
open System.IO
open System.Text.Json

let args = fsi.CommandLineArgs |> Array.skip 1
let value flag = args |> Array.tryFindIndex ((=) flag) |> Option.bind (fun index -> if index + 1 < args.Length then Some args[index + 1] else None)
let has flag = args |> Array.contains flag
let missing = [ "--repo-root"; "--name"; "--framework" ] |> List.filter (value >> Option.isNone)
if missing.Length > 0 then eprintfn "Missing required arguments: %s" (String.concat ", " missing); exit 2
let repo = value "--repo-root" |> Option.get |> Path.GetFullPath
let name = value "--name" |> Option.get
let framework = value "--framework" |> Option.get
if framework <> "hummingbird" && framework <> "vapor" then eprintfn "--framework must be hummingbird or vapor."; exit 2
let target = Path.Combine(repo, "Services", name)
if not (has "--dry-run") then
    Directory.CreateDirectory(Path.Combine(target, "Sources", name)) |> ignore
    let dependency, product = if framework = "hummingbird" then ".package(url: \"https://github.com/hummingbird-project/hummingbird.git\", from: \"2.0.0\")", ".product(name: \"Hummingbird\", package: \"hummingbird\")" else ".package(url: \"https://github.com/vapor/vapor.git\", from: \"4.0.0\")", ".product(name: \"Vapor\", package: \"vapor\")"
    File.WriteAllText(Path.Combine(target, "Package.swift"), $"// swift-tools-version: 6.2\nimport PackageDescription\nlet package = Package(name: \"{name}\", platforms: [.macOS(.v15)], dependencies: [{dependency}], targets: [.executableTarget(name: \"{name}\", dependencies: [{product}])])\n")
printfn "%s" (JsonSerializer.Serialize({| status = "success"; service_root = target; framework = framework; dry_run = has "--dry-run"; policy = "fixed-native-macos-and-github-linux" |}, JsonSerializerOptions(WriteIndented = true)))
