#!/usr/bin/env -S dotnet fsi
#load "../../../shared/project-docs/ProjectDocs.fsx"
#load "../../../shared/project-docs/DocsCoordinator.fsx"

open System.IO
open DocsCoordinator

let pluginRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let asset skill target template =
    let root = Path.Combine(pluginRoot, "skills", skill, "assets")
    { Name = skill; Target = target; Contract = Path.Combine(root, "document.contract.json"); Template = Path.Combine(root, template) }

let assets = [
    asset "maintain-project-readme" "README.md" "README.template.md"
    asset "maintain-project-contributing" "CONTRIBUTING.md" "CONTRIBUTING.template.md"
    asset "maintain-project-agents" "AGENTS.md" "AGENTS.template.md"
    asset "maintain-project-roadmap" "ROADMAP.md" "ROADMAP.template.md"
]

fsi.CommandLineArgs |> Array.skip 1 |> execute assets |> exit
