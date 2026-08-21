open System
open System.Diagnostics
open System.IO
open System.Text.Json

type Result = { ExitCode: int; Stdout: string; Stderr: string }

let socketRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))
let installer = Path.Combine(socketRoot, "plugins", "repository-skills", "skills", "maintain-project-repo", "scripts", "maintain-project-repo.fsx")
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

let nestedTests =
    Directory.GetFiles(socketRoot, "*", SearchOption.AllDirectories)
    |> Array.map (fun path -> Path.GetRelativePath(socketRoot, path))
    |> Array.filter (fun path ->
        let parts = path.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
        not (parts |> Array.exists (fun part -> part = ".git" || part = ".venv" || part = ".codex"))
        && parts.Length > 1
        && parts[0] <> "tests"
        && (parts |> Array.exists (fun part -> part = "test" || part = "tests")))
if not (Array.isEmpty nestedTests) then
    let rendered = String.concat ", " nestedTests
    failwith $"Tests must live only at the Socket root: {rendered}"

let snapshot () =
    Directory.GetFiles(testRoot, "*", SearchOption.AllDirectories)
    |> Array.filter (fun path -> not (path.Contains($"{Path.DirectorySeparatorChar}.git{Path.DirectorySeparatorChar}")))
    |> Array.sort
    |> Array.map (fun path -> Path.GetRelativePath(testRoot, path), File.ReadAllBytes(path))

run testRoot "git" [ "init"; "-q" ] |> requireSuccess "temporary Git initialization"
run socketRoot "dotnet" [ "fsi"; installer; "--repo-root"; testRoot; "--operation"; "install"; "--profile"; "generic" ] |> requireSuccess "repository-skills installation"

let contributing = Path.Combine(testRoot, "CONTRIBUTING.md")
File.AppendAllText(contributing, "\n```text\nSigned-off-by: Your Name <you@example.com>\n```\n")

run testRoot "just" [ "docs-apply" ] |> requireSuccess "first full documentation apply"
let first = snapshot ()
run testRoot "just" [ "docs-apply" ] |> requireSuccess "second full documentation apply"
let second = snapshot ()
if first.Length <> second.Length || Array.exists2 (fun (leftPath, leftBytes) (rightPath, rightBytes) -> leftPath <> rightPath || leftBytes <> rightBytes) first second then
    failwith "Second full documentation apply was not byte-idempotent."

run testRoot "just" [ "docs-check" ] |> requireSuccess "full documentation check"
let fixtureRecipes = run testRoot "just" [ "--summary" ]
requireSuccess "fixture Just recipe discovery" fixtureRecipes
let fixtureDocs =
    fixtureRecipes.Stdout.Split([| ' '; '\r'; '\n' |], StringSplitOptions.RemoveEmptyEntries)
    |> Array.filter (fun name -> name.StartsWith("docs-", StringComparison.Ordinal))
    |> Array.sort
if fixtureDocs <> [| "docs-apply"; "docs-check" |] then
    let rendered = String.concat ", " fixtureDocs
    failwith $"Installed repository exposed unexpected docs recipes: {rendered}"
run testRoot "git" [ "add"; "-A" ] |> requireSuccess "stage generated repository"
run testRoot "git" [ "-c"; "user.name=Socket Tests"; "-c"; "user.email=tests@example.invalid"; "commit"; "-qm"; "test fixture" ] |> requireSuccess "commit generated repository"
run testRoot "just" [ "repo-validate" ] |> requireSuccess "managed repository validation"

printfn "Repository-maintenance end-to-end test passed."
printfn "Temporary fixture: %s" testRoot
