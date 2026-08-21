module DocsCoordinator

open System
open System.IO
open System.Text.Json
open ProjectDocs

type DocumentAsset = { Name: string; Target: string; Contract: string; Template: string }

type DocsReport = {
    Mode: string
    DocumentOrder: string list
    Documents: DocumentReport list
    ResponsibilityIssues: Finding list
    Applied: bool
    Errors: string list
}

let private parseArgs argv =
    let mutable projectRoot = "."
    let mutable mode = CheckOnly
    let mutable format = "markdown"
    let mutable failOnIssues = false
    let rec loop args =
        match args with
        | [] -> ()
        | "--project-root" :: value :: tail -> projectRoot <- value; loop tail
        | "--run-mode" :: "check-only" :: tail -> mode <- CheckOnly; loop tail
        | "--run-mode" :: "apply" :: tail -> mode <- Apply; loop tail
        | "--format" :: value :: tail -> format <- value; loop tail
        | "--fail-on-issues" :: tail -> failOnIssues <- true; loop tail
        | unknown :: _ -> failwith $"Unknown argument: {unknown}"
    loop (List.ofArray argv)
    projectRoot, mode, format, failOnIssues

let private headingPresent (heading: string) (text: string) =
    let pattern = $"(?im)^#+\\s+{System.Text.RegularExpressions.Regex.Escape(heading)}\\s*$"
    System.Text.RegularExpressions.Regex.IsMatch(text, pattern)

let private auditResponsibilities root =
    let read file = let path = Path.Combine(root, file) in if File.Exists(path) then File.ReadAllText(path) else ""
    let findings = ResizeArray<Finding>()
    let check file headings owner id =
        let text = read file
        for heading in headings do
            if headingPresent heading text then
                findings.Add({ Id = id; Severity = "warning"; Message = $"{file} contains '{heading}', whose canonical owner is {owner}." })
    check "README.md" [ "Contribution Workflow"; "Review Expectations"; "Release Process" ] "CONTRIBUTING.md or maintainer docs" "readme-responsibility-drift"
    check "CONTRIBUTING.md" [ "Product Principles"; "Milestones"; "Small Tickets" ] "ROADMAP.md" "contributing-responsibility-drift"
    check "AGENTS.md" [ "Quick Start"; "Usage"; "Known Gaps" ] "README.md or ROADMAP.md" "agents-responsibility-drift"
    check "ROADMAP.md" [ "Contribution Workflow"; "Local Setup"; "Safety Boundaries" ] "CONTRIBUTING.md or AGENTS.md" "roadmap-responsibility-drift"
    List.ofSeq findings

let private jsonOptions =
    let value = JsonSerializerOptions(WriteIndented = true)
    value.PropertyNamingPolicy <- JsonNamingPolicy.CamelCase
    value

let private renderMarkdown report =
    let lines = ResizeArray<string>()
    lines.Add("# Project documentation maintenance report")
    lines.Add("")
    lines.Add($"- Mode: `{report.Mode}`")
    lines.Add($"- Applied: `{report.Applied.ToString().ToLowerInvariant()}`")
    lines.Add("")
    lines.Add("## Documents")
    lines.Add("")
    for document in report.Documents do
        lines.Add($"- `{document.Document}`: {document.Findings.Length} finding(s), {document.Fixes.Length} fix(es), changed `{document.Changed.ToString().ToLowerInvariant()}`")
        for finding in document.Findings do
            lines.Add($"  - `{finding.Severity}` `{finding.Id}`: {finding.Message}")
        for fix in document.Fixes do
            lines.Add($"  - `fix` `{fix.Id}`: {fix.Message}")
    lines.Add("")
    lines.Add("## Responsibility issues")
    lines.Add("")
    if List.isEmpty report.ResponsibilityIssues then lines.Add("- None.")
    else for issue in report.ResponsibilityIssues do lines.Add($"- `{issue.Id}`: {issue.Message}")
    lines.Add("")
    lines.Add("## Errors")
    lines.Add("")
    if List.isEmpty report.Errors then lines.Add("- None.")
    else for error in report.Errors do lines.Add($"- {error}")
    String.Join("\n", lines) + "\n"

let execute (assets: DocumentAsset list) argv =
    try
        let rootArg, mode, format, failOnIssues = parseArgs argv
        let root = Path.GetFullPath(rootArg)
        let options target = {
            ProjectRoot = root; TargetPath = Some target; RunMode = mode; Format = format
            FailOnIssues = failOnIssues; CollectSourceTickets = false; CollectGithubIssues = false
            GithubRepo = None; TicketSection = None; TicketText = None; TicketState = None
            TicketSource = None; TicketMatch = None; AllowDuplicate = false
        }
        let plans = assets |> List.map (fun asset -> planDocument asset.Contract asset.Template (options asset.Target))
        let planningErrors = plans |> List.collect (fun plan -> plan.Report.Errors)
        let applyErrors, applied =
            if mode = Apply && List.isEmpty planningErrors then
                match applyPlans plans with | Ok () -> [], true | Error errors -> errors, false
            else [], false
        let responsibilityIssues = auditResponsibilities root
        let report = {
            Mode = if mode = Apply then "apply" else "check-only"
            DocumentOrder = assets |> List.map (fun asset -> asset.Target)
            Documents = plans |> List.map (fun plan -> plan.Report)
            ResponsibilityIssues = responsibilityIssues
            Applied = applied
            Errors = planningErrors @ applyErrors
        }
        Console.Out.Write(if format = "json" then JsonSerializer.Serialize(report, jsonOptions) + "\n" else renderMarkdown report)
        let issueCount =
            report.Documents
            |> List.sumBy (fun document -> document.Findings |> List.filter (fun finding -> finding.Severity = "error") |> List.length)
        if not (List.isEmpty report.Errors) then 1
        elif failOnIssues && (issueCount > 0 || not (List.isEmpty responsibilityIssues)) then 2
        else 0
    with error ->
        Console.Error.WriteLine($"ERROR: {error.Message}")
        1
