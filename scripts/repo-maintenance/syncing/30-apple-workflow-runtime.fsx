#!/usr/bin/env -S dotnet fsi

open System.IO

let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let source = Path.Combine(root, "plugins", "apple-dev-skills", "shared", "workflow-planner.fsx")
let skills =
    [ "author-swift-docc-docs"; "structure-swift-sources"; "swift-package-build-run-workflow"
      "swift-package-testing-workflow"; "xcode-build-run-workflow"; "xcode-testing-workflow" ]
for skill in skills do
    let target = Path.Combine(root, "plugins", "apple-dev-skills", "skills", skill, "scripts", "run-workflow.fsx")
    Directory.CreateDirectory(Path.GetDirectoryName target) |> ignore
    File.Copy(source, target, true)
printfn "Synchronized the managed Apple workflow planner to %d skills." skills.Length
