open System
open System.Diagnostics
open System.IO
open System.Text.Json

type Result = { ExitCode: int; Stdout: string; Stderr: string }

let socketRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))
let installer = Path.Combine(socketRoot, "plugins", "repository-skills", "skills", "maintain-project-repo", "scripts", "maintain-project-repo.fsx")
let pluginInstaller = Path.Combine(socketRoot, "plugins", "agent-plugin-skills", "skills", "maintain-agent-plugins", "scripts", "maintain-agent-plugins.fsx")
let testRoot = Path.Combine(Path.GetTempPath(), $"socket-repository-maintenance-e2e-{Guid.NewGuid():N}")
Directory.CreateDirectory(testRoot) |> ignore

let run cwd executable arguments =
    let info = ProcessStartInfo(executable)
    info.WorkingDirectory <- cwd
    info.UseShellExecute <- false
    info.RedirectStandardOutput <- true
    info.RedirectStandardError <- true
    for argument in arguments do info.ArgumentList.Add(argument)
    use child = Process.Start(info)
    let stdout = child.StandardOutput.ReadToEnd()
    let stderr = child.StandardError.ReadToEnd()
    child.WaitForExit()
    { ExitCode = child.ExitCode; Stdout = stdout; Stderr = stderr }

let requireSuccess description result =
    if result.ExitCode <> 0 then failwith $"{description} failed: {result.Stderr}\n{result.Stdout}"

let rootRecipes = run socketRoot "just" [ "--summary" ]
requireSuccess "Socket Just recipe discovery" rootRecipes
let documentationRecipes =
    rootRecipes.Stdout.Split([| ' '; '\r'; '\n' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.filter (fun name -> name.StartsWith("docs-", StringComparison.Ordinal))
    |> Array.sort
if documentationRecipes <> [| "docs-apply"; "docs-check" |] then
    let rendered = String.concat ", " documentationRecipes
    failwith $"Expected exactly docs-apply and docs-check, found: {rendered}"
let pluginRecipes =
    rootRecipes.Stdout.Split([| ' '; '\r'; '\n' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.filter (fun name -> name.StartsWith("plugins-", StringComparison.Ordinal))
    |> Array.sort
if pluginRecipes <> [| "plugins-apply"; "plugins-check" |] then
    let rendered = String.concat ", " pluginRecipes
    failwith $"Expected exactly plugins-apply and plugins-check, found: {rendered}"

let nestedTests =
    Directory.GetFiles(socketRoot, "*", SearchOption.AllDirectories)
    |> Array.map (fun path -> Path.GetRelativePath(socketRoot, path))
    |> Array.filter (fun path ->
        let parts = path.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
        not (parts |> Array.exists (fun part -> part = ".git" || part = ".venv" || part = ".codex"))
        && parts.Length > 1
        && parts[0] <> "tests"
        && (parts |> Array.exists (fun part -> part = "test" || part = "tests" || part = "evals")))
if not (Array.isEmpty nestedTests) then
    let rendered = String.concat ", " nestedTests
    failwith $"Tests must live only at the Socket root: {rendered}"

let legacyAutomation =
    Directory.GetFiles(socketRoot, "*", SearchOption.AllDirectories)
    |> Array.map (fun path -> Path.GetRelativePath(socketRoot, path))
    |> Array.filter (fun path ->
        let parts = path.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
        not (parts |> Array.exists (fun part -> part = ".git" || part = ".venv" || part = ".codex"))
        && (path.EndsWith(".py", StringComparison.Ordinal) || path.EndsWith(".sh", StringComparison.Ordinal)))
if not (Array.isEmpty legacyAutomation) then
    failwith $"Socket automation must use FSX only; found {legacyAutomation[0]}."

let snapshot () =
    Directory.GetFiles(testRoot, "*", SearchOption.AllDirectories)
    |> Array.filter (fun path -> not (path.Contains($"{Path.DirectorySeparatorChar}.git{Path.DirectorySeparatorChar}")))
    |> Array.sort
    |> Array.map (fun path -> Path.GetRelativePath(testRoot, path), File.ReadAllBytes(path))

run testRoot "git" [ "init"; "-q" ] |> requireSuccess "temporary Git initialization"
run socketRoot "dotnet" [ "fsi"; installer; "--repo-root"; testRoot; "--operation"; "install"; "--profile"; "generic" ] |> requireSuccess "repository-skills installation"

let fixturePluginRoot = Path.Combine(testRoot, "plugins", "sample-agent-plugin")
Directory.CreateDirectory(Path.Combine(fixturePluginRoot, ".codex-plugin")) |> ignore
Directory.CreateDirectory(Path.Combine(fixturePluginRoot, "skills", "sample-workflow")) |> ignore
File.WriteAllText(
    Path.Combine(fixturePluginRoot, ".codex-plugin", "plugin.json"),
    """{
  "name": "sample-agent-plugin",
  "version": "1.0.0",
  "description": "A deterministic plugin-maintenance fixture.",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "interface": {
    "displayName": "Sample Agent Plugin",
    "shortDescription": "Exercise managed plugin maintenance.",
    "longDescription": "Exercise managed plugin maintenance through the repository root E2E path.",
    "developerName": "Gale",
    "category": "Developer Tools",
    "defaultPrompt": "Maintain this sample plugin."
  }
}
""")
File.WriteAllText(
    Path.Combine(fixturePluginRoot, "skills", "sample-workflow", "SKILL.md"),
    """---
name: sample-workflow
description: Exercise the managed plugin fixture.
---

# Sample Workflow

Exercise the fixture.
""")
run socketRoot "dotnet" [ "fsi"; pluginInstaller; "--repo-root"; testRoot; "--operation"; "install" ] |> requireSuccess "agent-plugin-skills installation"

let contributing = Path.Combine(testRoot, "CONTRIBUTING.md")
File.AppendAllText(contributing, "\n```text\nSigned-off-by: Your Name <you@example.com>\n```\n")

run testRoot "just" [ "docs-apply" ] |> requireSuccess "first full documentation apply"
run testRoot "just" [ "plugins-apply" ] |> requireSuccess "first full plugin apply"
let first = snapshot ()
run testRoot "just" [ "docs-apply" ] |> requireSuccess "second full documentation apply"
run testRoot "just" [ "plugins-apply" ] |> requireSuccess "second full plugin apply"
let second = snapshot ()
if first.Length <> second.Length || Array.exists2 (fun (leftPath, leftBytes) (rightPath, rightBytes) -> leftPath <> rightPath || leftBytes <> rightBytes) first second then
    failwith "Second full documentation apply was not byte-idempotent."

run testRoot "just" [ "docs-check" ] |> requireSuccess "full documentation check"
run testRoot "just" [ "plugins-check" ] |> requireSuccess "full plugin check"
let fixtureRecipes = run testRoot "just" [ "--summary" ]
requireSuccess "fixture Just recipe discovery" fixtureRecipes
let fixtureDocs =
    fixtureRecipes.Stdout.Split([| ' '; '\r'; '\n' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.filter (fun name -> name.StartsWith("docs-", StringComparison.Ordinal))
    |> Array.sort
if fixtureDocs <> [| "docs-apply"; "docs-check" |] then
    let rendered = String.concat ", " fixtureDocs
    failwith $"Installed repository exposed unexpected docs recipes: {rendered}"
let fixturePlugins =
    fixtureRecipes.Stdout.Split([| ' '; '\r'; '\n' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.filter (fun name -> name.StartsWith("plugins-", StringComparison.Ordinal))
    |> Array.sort
if fixturePlugins <> [| "plugins-apply"; "plugins-check" |] then
    let rendered = String.concat ", " fixturePlugins
    failwith $"Installed repository exposed unexpected plugin recipes: {rendered}"
run testRoot "git" [ "add"; "-A" ] |> requireSuccess "stage generated repository"
run testRoot "git" [ "-c"; "user.name=Socket Tests"; "-c"; "user.email=tests@example.invalid"; "commit"; "-qm"; "test fixture" ] |> requireSuccess "commit generated repository"
run testRoot "just" [ "repo-validate" ] |> requireSuccess "managed repository validation"

printfn "Repository-maintenance end-to-end test passed."
printfn "Temporary fixture: %s" testRoot
