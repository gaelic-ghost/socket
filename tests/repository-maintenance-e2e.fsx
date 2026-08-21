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
run testRoot "git" [ "add"; "-A" ] |> requireSuccess "stage generated repository"
run testRoot "git" [ "-c"; "user.name=Socket Tests"; "-c"; "user.email=tests@example.invalid"; "commit"; "-qm"; "test fixture" ] |> requireSuccess "commit generated repository"
run testRoot "just" [ "repo-validate" ] |> requireSuccess "managed repository validation"

printfn "Repository-maintenance end-to-end test passed."
printfn "Temporary fixture: %s" testRoot
