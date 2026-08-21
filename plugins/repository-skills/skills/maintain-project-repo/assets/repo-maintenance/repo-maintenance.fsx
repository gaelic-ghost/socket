#!/usr/bin/env -S dotnet fsi

open System
open System.Diagnostics
open System.IO
open System.Text.Json

type CommandResult = { ExitCode: int; Stdout: string; Stderr: string }

let maintenanceRoot = Path.GetFullPath(__SOURCE_DIRECTORY__)
let repoRoot = Path.GetFullPath(Path.Combine(maintenanceRoot, "..", ".."))

let fail message = raise (InvalidOperationException(message))

let runIn cwd executable arguments =
    let startInfo = ProcessStartInfo(executable)
    startInfo.WorkingDirectory <- cwd
    startInfo.UseShellExecute <- false
    startInfo.RedirectStandardOutput <- true
    startInfo.RedirectStandardError <- true
    for argument in arguments do startInfo.ArgumentList.Add(argument)
    use child = Process.Start(startInfo)
    let stdout = child.StandardOutput.ReadToEnd()
    let stderr = child.StandardError.ReadToEnd()
    child.WaitForExit()
    { ExitCode = child.ExitCode; Stdout = stdout.Trim(); Stderr = stderr.Trim() }

let requireSuccess description result =
    if result.ExitCode <> 0 then
        let detail = if String.IsNullOrWhiteSpace(result.Stderr) then result.Stdout else result.Stderr
        fail $"{description} failed in {repoRoot}: {detail}"
    result.Stdout

let run executable arguments = runIn repoRoot executable arguments
let git arguments = run "git" arguments
let gh arguments = run "gh" arguments

let ensureGitRepo () =
    git [ "rev-parse"; "--show-toplevel" ]
    |> requireSuccess "Git repository check"
    |> Path.GetFullPath
    |> fun actual -> if actual <> repoRoot then fail $"Repo-maintenance expected repository root {repoRoot}, but Git resolved {actual}."

let runFsxDirectory name =
    let directory = Path.Combine(maintenanceRoot, name)
    if Directory.Exists(directory) then
        Directory.GetFiles(directory, "*.fsx")
        |> Array.sortWith (fun left right -> StringComparer.Ordinal.Compare(left, right))
        |> Array.iter (fun script ->
            let result = runIn repoRoot "dotnet" [ "fsi"; script ]
            requireSuccess $"Repo-maintenance {name} step {Path.GetFileName(script)}" result |> ignore
            if not (String.IsNullOrWhiteSpace(result.Stdout)) then printfn "%s" result.Stdout)

let validate () =
    ensureGitRepo ()
    let required = [
        "repo-maintenance.fsx"
        "maintain-project-docs.fsx"
        "repo-maintenance.just"
        "lib/ProjectDocs.fsx"
        "lib/DocsCoordinator.fsx"
        "config/profile.json"
    ]
    for relative in required do
        let path = Path.Combine(maintenanceRoot, relative)
        if not (File.Exists(path)) then fail $"Managed repo-maintenance file is missing: {path}"
    let justfile = Path.Combine(repoRoot, "justfile")
    if not (File.Exists(justfile)) then fail $"Repository justfile is missing: {justfile}"
    let justText = File.ReadAllText(justfile)
    if not (justText.Contains("scripts/repo-maintenance/repo-maintenance.just")) then
        fail "Repository justfile does not import scripts/repo-maintenance/repo-maintenance.just."
    runFsxDirectory "validations"
    let profile = JsonDocument.Parse(File.ReadAllText(Path.Combine(maintenanceRoot, "config", "profile.json"))).RootElement.GetProperty("profile").GetString()
    if profile = "xcode-workspace" then
        let components = Path.Combine(maintenanceRoot, "workspace", "validate-components.fsx")
        if not (File.Exists(components)) then fail $"xcode-workspace component validator is missing: {components}"
        runIn repoRoot "dotnet" [ "fsi"; components ] |> requireSuccess "xcode-workspace component validation" |> ignore
    runIn repoRoot "dotnet" [ "fsi"; Path.Combine(maintenanceRoot, "maintain-project-docs.fsx"); "--project-root"; repoRoot; "--run-mode"; "check-only"; "--format"; "markdown"; "--fail-on-issues" ]
    |> requireSuccess "Canonical documentation validation"
    |> ignore
    printfn "Repo-maintenance validation passed."

let sync () =
    ensureGitRepo ()
    runFsxDirectory "syncing"
    validate ()
    printfn "Repo-maintenance shared sync and validation passed."

let cleanWorktree (cwd: string) =
    let status = runIn cwd "git" [ "status"; "--porcelain" ] |> requireSuccess "Worktree status"
    if not (String.IsNullOrWhiteSpace(status)) then fail $"Release requires a clean worktree: {cwd}"

let currentBranch (cwd: string) = runIn cwd "git" [ "branch"; "--show-current" ] |> requireSuccess "Current branch"

let normalizeTag (value: string) =
    let tag = if value.StartsWith("v") then value else "v" + value
    if not (System.Text.RegularExpressions.Regex.IsMatch(tag, "^v[0-9]+\\.[0-9]+\\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")) then
        fail $"Release version must use SemVer syntax: {value}"
    tag

let optionValue (name: string) (args: string list) =
    args
    |> List.tryFindIndex ((=) name)
    |> Option.bind (fun index -> args |> List.tryItem (index + 1))

let hasFlag (name: string) (args: string list) = List.contains name args

let ensureReleaseNotes (cwd: string) (tag: string) =
    let candidates = [ Path.Combine(cwd, "docs", "releases", tag + ".md"); Path.Combine(cwd, "docs", "releases", tag.TrimStart('v') + ".md") ]
    candidates |> List.tryFind File.Exists |> Option.defaultWith (fun () -> fail $"Checked-in release notes are required for {tag} under docs/releases/.")

let branchVisible (branch: string) (expected: string) =
    let output = git [ "ls-remote"; "origin"; $"refs/heads/{branch}" ] |> requireSuccess "Remote branch visibility"
    not (String.IsNullOrWhiteSpace(output)) && output.Split([|' '; '\t'|], StringSplitOptions.RemoveEmptyEntries).[0] = expected

let tagVisible (cwd: string) (tag: string) (expected: string) =
    let output = runIn cwd "git" [ "ls-remote"; "origin"; $"refs/tags/{tag}^{{}}" ] |> requireSuccess "Remote tag visibility"
    not (String.IsNullOrWhiteSpace(output)) && output.Split([|' '; '\t'|], StringSplitOptions.RemoveEmptyEntries).[0] = expected

let prNumber (branch: string) =
    let output = gh [ "pr"; "list"; "--state"; "all"; "--head"; branch; "--base"; "main"; "--limit"; "1"; "--json"; "number" ] |> requireSuccess "Release PR lookup"
    use json = JsonDocument.Parse(output)
    if json.RootElement.GetArrayLength() = 0 then None else Some(json.RootElement[0].GetProperty("number").GetInt32())

type Gate = { Number: int; Url: string; State: string; Head: string; Sha: string; Phase: string; Comments: int }

let inspectGate number =
    let pr = gh [ "pr"; "view"; string number; "--json"; "url,state,headRefName,headRefOid,reviewDecision,comments,reviews" ] |> requireSuccess "Release PR inspection"
    use data = JsonDocument.Parse(pr)
    let root = data.RootElement
    let checksResult = gh [ "pr"; "checks"; string number; "--json"; "name,bucket" ]
    let checks =
        if String.IsNullOrWhiteSpace(checksResult.Stdout) then []
        else
            use parsed = JsonDocument.Parse(checksResult.Stdout)
            parsed.RootElement.EnumerateArray()
            |> Seq.map (fun item -> item.GetProperty("name").GetString(), item.GetProperty("bucket").GetString())
            |> Seq.toList
    let state = root.GetProperty("state").GetString()
    let review = root.GetProperty("reviewDecision").GetString()
    let comments = root.GetProperty("comments").GetArrayLength() + (root.GetProperty("reviews").EnumerateArray() |> Seq.filter (fun item -> item.GetProperty("state").GetString() = "COMMENTED") |> Seq.length)
    let names = checks |> List.map fst |> Set.ofList
    let buckets = checks |> List.map snd |> Set.ofList
    let phase =
        if state = "MERGED" then "merged"
        elif state <> "OPEN" then "closed"
        elif List.isEmpty checks || not (names.Contains("validate")) then "awaiting-required-checks"
        elif buckets.Contains("fail") || buckets.Contains("cancel") then "failed-checks"
        elif buckets.Contains("pending") then "awaiting-pr-checks"
        elif review = "CHANGES_REQUESTED" then "changes-requested"
        elif comments > 0 then "comments-require-review"
        else "ready-to-advance"
    { Number = number; Url = root.GetProperty("url").GetString(); State = state; Head = root.GetProperty("headRefName").GetString(); Sha = root.GetProperty("headRefOid").GetString(); Phase = phase; Comments = comments }

let continuation tag gate =
    let repository = gh [ "repo"; "view"; "--json"; "nameWithOwner"; "--jq"; ".nameWithOwner" ] |> requireSuccess "Repository identity"
    let payload = {| schema = "repo-maintenance-continuation/v1"; operation = "standard-release"; repository = repository; releaseTag = tag; branch = gate.Head; headCommit = gate.Sha; prNumber = gate.Number; phase = gate.Phase; minimumDelayMinutes = 5; resumeCommand = $"just repo-release-inspect {tag}"; advanceCommand = $"just repo-release-advance {tag}" |}
    printfn "%s" (JsonSerializer.Serialize(payload))

let findMainWorktree () =
    let output = git [ "worktree"; "list"; "--porcelain" ] |> requireSuccess "Worktree inventory"
    let mutable path: string option = None
    let mutable found: string option = None
    for line in output.Split('\n') do
        if line.StartsWith("worktree ") then path <- Some(line.Substring(9))
        elif line = "branch refs/heads/main" then found <- path
    found |> Option.defaultWith (fun () -> fail "No clean worktree owns local main.")

let accountBranches (mainRoot: string) (supplied: string list) =
    let allowed = Set.ofList [ "preserved"; "in-progress"; "archived"; "merged"; "safe-to-delete" ]
    let parsed =
        supplied
        |> List.map (fun value ->
            let parts = value.Split('=', 2)
            if parts.Length <> 2 || not (allowed.Contains(parts[1])) then fail $"Invalid branch accounting: {value}"
            parts[0], parts[1])
        |> Map.ofList
    let branches =
        runIn mainRoot "git" [ "branch"; "--no-merged"; "main"; "--format=%(refname:short)" ]
        |> requireSuccess "Unmerged branch inventory"
        |> fun output -> output.Split('\n', StringSplitOptions.RemoveEmptyEntries) |> Array.filter ((<>) "main") |> Array.toList
    let missing = branches |> List.filter (fun branch -> not (parsed.ContainsKey(branch)))
    if not (List.isEmpty missing) then
        let rendered = String.concat ", " missing
        fail $"Branch accounting is incomplete for: {rendered}"
    branches |> List.map (fun branch -> branch, parsed[branch])

let releasePrepare (tag: string) (args: string list) =
    ensureGitRepo ()
    cleanWorktree repoRoot
    let branch = currentBranch repoRoot
    if String.IsNullOrWhiteSpace(branch) || branch = "main" then fail "Release prepare must run from a named feature branch, not main."
    ensureReleaseNotes repoRoot tag |> ignore
    validate ()
    let versionScript = Path.Combine(maintenanceRoot, "version-bump.fsx")
    if not (hasFlag "--skip-version-bump" args) then
        if not (File.Exists(versionScript)) then fail $"Version bump script is required: {versionScript}"
        let result = runIn repoRoot "dotnet" [ "fsi"; versionScript; tag.TrimStart('v') ]
        requireSuccess "Version bump" result |> ignore
        let status = git [ "status"; "--porcelain" ] |> requireSuccess "Version bump status"
        if String.IsNullOrWhiteSpace(status) then fail "Version bump completed without changing files."
        git [ "add"; "-A" ] |> requireSuccess "Stage version bump" |> ignore
        git [ "commit"; "-m"; $"release: bump versions for {tag}" ] |> requireSuccess "Commit version bump" |> ignore
    cleanWorktree repoRoot
    git [ "push"; "-u"; "origin"; branch ] |> requireSuccess "Push release branch" |> ignore
    let head = git [ "rev-parse"; "HEAD" ] |> requireSuccess "Release head"
    if not (branchVisible branch head) then
        let gate = { Number = 0; Url = ""; State = "OPEN"; Head = branch; Sha = head; Phase = "awaiting-branch-visibility"; Comments = 0 }
        continuation tag gate
    else
        let number =
            match prNumber branch with
            | Some existing -> existing
            | None ->
                gh [ "pr"; "create"; "--base"; "main"; "--head"; branch; "--title"; $"release: prepare {tag}"; "--body"; $"Prepare {tag} through the canonical repository-maintenance workflow." ] |> requireSuccess "Create release PR" |> ignore
                prNumber branch |> Option.defaultWith (fun () -> fail "GitHub did not return the created release PR.")
        let gate = inspectGate number
        printfn "PR #%d: %s (%s)" gate.Number gate.Phase gate.Url
        continuation tag gate

let releaseInspect (tag: string) =
    ensureGitRepo ()
    cleanWorktree repoRoot
    let branch = currentBranch repoRoot
    let number = prNumber branch |> Option.defaultWith (fun () -> fail $"No release PR exists for {branch}.")
    let gate = inspectGate number
    printfn "PR #%d: %s (%s)" gate.Number gate.Phase gate.Url
    continuation tag gate

let releaseAdvance (tag: string) (args: string list) =
    ensureGitRepo ()
    cleanWorktree repoRoot
    let branch = currentBranch repoRoot
    let number = prNumber branch |> Option.defaultWith (fun () -> fail $"No release PR exists for {branch}.")
    let gate = inspectGate number
    let head = git [ "rev-parse"; "HEAD" ] |> requireSuccess "Release head"
    if gate.Head <> branch || gate.Sha <> head then fail "Release PR branch or commit identity changed; inspect before advancing."
    if gate.Phase <> "ready-to-advance" && not (gate.Phase = "comments-require-review" && hasFlag "--review-comments-addressed" args) then
        continuation tag gate
        fail $"Release PR #{number} is not ready to advance: {gate.Phase}."
    gh [ "pr"; "merge"; string number; "--merge"; "--delete-branch" ] |> requireSuccess "Merge release PR" |> ignore
    let mainRoot = findMainWorktree ()
    cleanWorktree mainRoot
    runIn mainRoot "git" [ "fetch"; "origin"; "main"; "--prune" ] |> requireSuccess "Fetch main" |> ignore
    runIn mainRoot "git" [ "pull"; "--ff-only"; "origin"; "main" ] |> requireSuccess "Fast-forward main" |> ignore
    let mainHead = runIn mainRoot "git" [ "rev-parse"; "HEAD" ] |> requireSuccess "Reviewed main head"
    let accountingValues =
        args |> List.mapi (fun index value -> index, value) |> List.choose (fun (index, value) -> if value = "--branch-accounting" then args |> List.tryItem(index + 1) else None)
    let accounting = accountBranches mainRoot accountingValues
    ensureReleaseNotes mainRoot tag |> ignore
    let existingTag = runIn mainRoot "git" [ "rev-parse"; "-q"; "--verify"; $"refs/tags/{tag}" ]
    if existingTag.ExitCode <> 0 then runIn mainRoot "git" [ "tag"; "-a"; tag; "-m"; $"Release {tag}" ] |> requireSuccess "Create release tag" |> ignore
    runIn mainRoot "git" [ "push"; "origin"; tag ] |> requireSuccess "Push release tag" |> ignore
    if not (tagVisible mainRoot tag mainHead) then fail $"Remote tag {tag} is not visible at reviewed main {mainHead}."
    let releaseView = runIn mainRoot "gh" [ "release"; "view"; tag; "--json"; "tagName,isPrerelease,url" ]
    if releaseView.ExitCode <> 0 then
        let notes = ensureReleaseNotes mainRoot tag
        let createArgs = [ "release"; "create"; tag; "--verify-tag"; "--title"; tag; "--notes-file"; notes ] @ (if tag.Contains("-") then [ "--prerelease" ] else [])
        runIn mainRoot "gh" createArgs |> requireSuccess "Create GitHub release" |> ignore
    printfn "Branch accounting:"
    if List.isEmpty accounting then printfn "- No local branches remain outside main."
    else for branchName, status in accounting do printfn "- %s: %s" branchName status
    printfn "Release %s completed from %s." tag mainHead

let release (operation: string) (args: string list) =
    let tag = optionValue "--version" args |> Option.defaultWith (fun () -> fail "Pass --version vX.Y.Z.") |> normalizeTag
    match operation with
    | "prepare" -> releasePrepare tag args
    | "inspect" -> releaseInspect tag
    | "advance" -> releaseAdvance tag args
    | _ -> fail $"Unsupported release operation: {operation}"

let main argv =
    match List.ofArray argv with
    | [ "validate" ] -> validate (); 0
    | [ "sync" ] -> sync (); 0
    | "release" :: operation :: args -> release operation args; 0
    | _ -> fail "Usage: repo-maintenance.fsx validate|sync|release prepare|inspect|advance --version vX.Y.Z"

try fsi.CommandLineArgs |> Array.skip 1 |> main |> exit
with error -> eprintfn "ERROR: %s" error.Message; exit 1
