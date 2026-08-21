#!/usr/bin/env -S dotnet fsi
#load "lib/ProjectDocs.fsx"
#load "lib/DocsCoordinator.fsx"

open System.IO
open DocsCoordinator

let root = Path.GetFullPath(__SOURCE_DIRECTORY__)
let asset name target folder template = {
    Name = name
    Target = target
    Contract = Path.Combine(root, "docs", folder, "document.contract.json")
    Template = Path.Combine(root, "docs", folder, template)
}

let assets = [
    asset "readme" "README.md" "readme" "README.template.md"
    asset "contributing" "CONTRIBUTING.md" "contributing" "CONTRIBUTING.template.md"
    asset "agents" "AGENTS.md" "agents" "AGENTS.template.md"
    asset "roadmap" "ROADMAP.md" "roadmap" "ROADMAP.template.md"
]

fsi.CommandLineArgs |> Array.skip 1 |> execute assets |> exit
