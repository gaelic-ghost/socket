module ProjectDocs

open System
open System.Diagnostics
open System.IO
open System.Text
open System.Text.Json
open System.Text.RegularExpressions

type RunMode =
    | CheckOnly
    | Apply

type DocumentKind =
    | Readme
    | Contributing
    | Agents
    | Roadmap

type Section = {
    Heading: string
    Body: string
}

type ParsedDocument = {
    Preamble: string
    Sections: Section list
}

type Alias = {
    Canonical: string
    Values: string list
}

type Contract = {
    SchemaVersion: int
    Kind: DocumentKind
    TargetFile: string
    RequireTableOfContents: bool
    PreservePreamble: bool
    AllowAdditionalSections: bool
    RequiredSections: string list
    SectionOrder: string list
    RequiredSubsections: Map<string, string list>
    SectionAliases: Alias list
    SubsectionAliases: Alias list
    AllowedStatuses: string list
    StatusAliases: Alias list
}

type Finding = {
    Id: string
    Severity: string
    Message: string
}

type Fix = {
    Id: string
    Message: string
}

type DocumentReport = {
    Document: string
    Path: string
    Mode: string
    Findings: Finding list
    Fixes: Fix list
    Changed: bool
    Errors: string list
}

type DocumentPlan = {
    Report: DocumentReport
    TargetPath: string
    Original: string option
    Rendered: string
}

type CliOptions = {
    ProjectRoot: string
    TargetPath: string option
    RunMode: RunMode
    Format: string
    FailOnIssues: bool
    CollectSourceTickets: bool
    CollectGithubIssues: bool
    GithubRepo: string option
    TicketSection: string option
    TicketText: string option
    TicketState: string option
    TicketSource: string option
    TicketMatch: string option
    AllowDuplicate: bool
}

let private normalizeNewlines (text: string) =
    text.Replace("\r\n", "\n").Replace("\r", "\n")

let private normalizedBody (text: string) =
    normalizeNewlines text
    |> fun value -> value.Trim('\n')

let private canonicalText (text: string) =
    normalizeNewlines text
    |> fun value -> value.TrimEnd()
    |> fun value -> value + "\n"

let private headingRegex level =
    Regex($"^#{{{level}}}\\s+(.+?)\\s*$", RegexOptions.Compiled)

let private splitAtHeadings level (text: string) =
    let lines = normalizeNewlines text |> fun value -> value.Split('\n')
    let regex = headingRegex level
    let mutable inFence = false
    let mutable preamble = ResizeArray<string>()
    let sections = ResizeArray<Section>()
    let mutable currentHeading: string option = None
    let mutable currentBody = ResizeArray<string>()

    let flush () =
        match currentHeading with
        | Some heading ->
            sections.Add({ Heading = heading; Body = String.Join("\n", currentBody) |> normalizedBody })
        | None -> preamble <- ResizeArray<string>(currentBody)
        currentBody <- ResizeArray<string>()

    for line in lines do
        if line.TrimStart().StartsWith("```") || line.TrimStart().StartsWith("~~~") then
            inFence <- not inFence

        let matched = if inFence then Match.Empty else regex.Match(line)
        if matched.Success then
            flush ()
            currentHeading <- Some(matched.Groups[1].Value.Trim())
        else
            currentBody.Add(line)

    flush ()
    normalizedBody (String.Join("\n", preamble)), List.ofSeq sections

let parseDocument text =
    let preamble, sections = splitAtHeadings 2 text
    { Preamble = preamble; Sections = sections }

let private parseSubsections body =
    let intro, sections = splitAtHeadings 3 body
    intro, sections

let private slugify (heading: string) =
    let lowered = heading.Trim().ToLowerInvariant()
    Regex.Replace(lowered, "[^a-z0-9\\s-]", "")
    |> fun value -> Regex.Replace(value, "[\\s-]+", "-")
    |> fun value -> value.Trim('-')

let private sectionMap sections =
    sections
    |> List.map (fun section -> section.Heading, section)
    |> Map.ofList

let private aliasMap aliases =
    aliases
    |> List.collect (fun alias -> alias.Values |> List.map (fun value -> value, alias.Canonical))
    |> Map.ofList

let private parseKind value =
    match value with
    | "readme" -> Readme
    | "contributing" -> Contributing
    | "agents" -> Agents
    | "roadmap" -> Roadmap
    | unsupported -> failwith $"Unsupported managed document kind: {unsupported}"

let private stringList (element: JsonElement) =
    element.EnumerateArray()
    |> Seq.map (fun item -> item.GetString() |> Option.ofObj |> Option.defaultValue "")
    |> Seq.toList

let private aliases (root: JsonElement) (propertyName: string) =
    match root.TryGetProperty(propertyName) with
    | true, value ->
        value.EnumerateObject()
        |> Seq.map (fun property -> { Canonical = property.Name; Values = stringList property.Value })
        |> Seq.toList
    | false, _ -> []

let loadContract path =
    use document = JsonDocument.Parse(File.ReadAllText(path))
    let root = document.RootElement
    let requiredSubsections =
        match root.TryGetProperty("requiredSubsections") with
        | true, value ->
            value.EnumerateObject()
            |> Seq.map (fun property -> property.Name, stringList property.Value)
            |> Map.ofSeq
        | false, _ -> Map.empty

    let optionalList (propertyName: string) =
        match root.TryGetProperty(propertyName) with
        | true, value -> stringList value
        | false, _ -> []

    {
        SchemaVersion = root.GetProperty("schemaVersion").GetInt32()
        Kind = root.GetProperty("document").GetString() |> parseKind
        TargetFile = root.GetProperty("targetFile").GetString()
        RequireTableOfContents = root.GetProperty("requireTableOfContents").GetBoolean()
        PreservePreamble = root.GetProperty("preservePreamble").GetBoolean()
        AllowAdditionalSections = root.GetProperty("allowAdditionalSections").GetBoolean()
        RequiredSections = stringList (root.GetProperty("requiredSections"))
        SectionOrder = stringList (root.GetProperty("sectionOrder"))
        RequiredSubsections = requiredSubsections
        SectionAliases = aliases root "sectionAliases"
        SubsectionAliases = aliases root "subsectionAliases"
        AllowedStatuses = optionalList "allowedStatuses"
        StatusAliases = aliases root "statusAliases"
    }

let private sectionAliasLookup contract = aliasMap contract.SectionAliases

let private subsectionAliasLookup contract = aliasMap contract.SubsectionAliases

let private canonicalizeHeading lookup heading =
    lookup |> Map.tryFind heading |> Option.defaultValue heading

let private canonicalizeSections contract sections =
    let lookup = sectionAliasLookup contract
    sections
    |> List.map (fun section -> { section with Heading = canonicalizeHeading lookup section.Heading })

let private milestoneRegex = Regex("^Milestone\\s+(\\d+)\\s*:\\s*(.+?)\\s*$", RegexOptions.Compiled)

let private isMilestone (heading: string) = milestoneRegex.IsMatch(heading)

let private requiredSubsectionsFor contract sectionHeading =
    match contract.RequiredSubsections |> Map.tryFind sectionHeading with
    | Some required -> Some required
    | None when isMilestone sectionHeading -> contract.RequiredSubsections |> Map.tryFind "__MILESTONE__"
    | None -> None

let private renderSubsections contract sectionHeading existingBody templateBody =
    match requiredSubsectionsFor contract sectionHeading with
    | None -> existingBody, []
    | Some required ->
        let intro, existing = parseSubsections existingBody
        let _, templates = parseSubsections templateBody
        let lookup = subsectionAliasLookup contract
        let normalizedExisting =
            existing
            |> List.map (fun section -> { section with Heading = canonicalizeHeading lookup section.Heading })
        let existingMap = sectionMap normalizedExisting
        let templateMap = sectionMap templates
        let fixes = ResizeArray<Fix>()
        let ordered =
            required
            |> List.map (fun heading ->
                match existingMap |> Map.tryFind heading with
                | Some section -> section
                | None ->
                    fixes.Add({ Id = "add-subsection"; Message = $"Added missing subsection '{sectionHeading} > {heading}'." })
                    if isMilestone sectionHeading then { Heading = heading; Body = "" }
                    else
                        templateMap
                        |> Map.tryFind heading
                        |> Option.defaultValue { Heading = heading; Body = "TBD" })
        let extras = normalizedExisting |> List.filter (fun section -> not (List.contains section.Heading required))
        let rendered =
            [ if not (String.IsNullOrWhiteSpace intro) then yield normalizedBody intro
              for section in ordered @ extras do
                  yield $"### {section.Heading}\n\n{normalizedBody section.Body}" ]
            |> String.concat "\n\n"
        rendered, List.ofSeq fixes

let private milestoneNumber (heading: string) =
    let matched = milestoneRegex.Match(heading)
    if matched.Success then Int32.Parse(matched.Groups[1].Value) else Int32.MaxValue

let private topLevelOrder contract sections =
    let byHeading = sectionMap sections
    let milestones = sections |> List.filter (fun section -> isMilestone section.Heading) |> List.sortBy (fun section -> milestoneNumber section.Heading)
    let required = Set.ofList contract.RequiredSections
    let aliases = sectionAliasLookup contract |> Map.toSeq |> Seq.map fst |> Set.ofSeq
    let extras =
        sections
        |> List.filter (fun section ->
            section.Heading <> "Table of Contents"
            && not (required.Contains section.Heading)
            && not (aliases.Contains section.Heading)
            && not (isMilestone section.Heading))
    contract.SectionOrder
    |> List.collect (fun heading ->
        if heading = "__MILESTONES__" then milestones
        else byHeading |> Map.tryFind heading |> Option.toList)
    |> fun ordered -> if contract.AllowAdditionalSections then ordered @ extras else ordered

let private buildToc sections =
    sections
    |> List.filter (fun section -> section.Heading <> "Table of Contents")
    |> List.map (fun section -> $"- [{section.Heading}](#{slugify section.Heading})")
    |> String.concat "\n"

let private textOutsideFences (text: string) =
    let mutable inFence = false
    normalizeNewlines text
    |> fun value -> value.Split('\n')
    |> Array.choose (fun line ->
        if line.TrimStart().StartsWith("```") || line.TrimStart().StartsWith("~~~") then
            inFence <- not inFence
            None
        elif inFence then None
        else Some line)
    |> String.concat "\n"

let private containsManagedPlaceholder body =
    let lines = textOutsideFences body |> fun value -> value.Split('\n')
    lines
    |> Array.exists (fun line ->
        let value = line.Trim()
        value = "TBD"
        || value.StartsWith("Explain ")
        || value.StartsWith("Describe ")
        || value.StartsWith("Summarize ")
        || value.StartsWith("State any ")
        || value.StartsWith("Record ")
        || value.StartsWith("Add the first ")
        || value.StartsWith("Replace this "))

let private canonicalStatus contract (value: string) =
    contract.AllowedStatuses
    |> List.tryFind (fun allowed -> String.Equals(allowed, value.Trim(), StringComparison.OrdinalIgnoreCase))
    |> Option.orElseWith (fun () ->
        contract.StatusAliases
        |> List.tryPick (fun alias ->
            if alias.Values |> List.exists (fun candidate -> String.Equals(candidate, value.Trim(), StringComparison.OrdinalIgnoreCase)) then Some alias.Canonical else None))

let private normalizeMilestoneStatus contract body =
    let intro, children = parseSubsections body
    let fixes = ResizeArray<Fix>()
    let normalized =
        children
        |> List.map (fun child ->
            if child.Heading <> "Status" then child
            else
                match canonicalStatus contract child.Body with
                | Some status when status <> child.Body.Trim() ->
                    fixes.Add({ Id = "normalize-milestone-status"; Message = $"Normalized milestone status '{child.Body.Trim()}' to '{status}'." })
                    { child with Body = status }
                | _ -> child)
    let rendered =
        [ if not (String.IsNullOrWhiteSpace intro) then yield normalizedBody intro
          for child in normalized do yield $"### {child.Heading}\n\n{normalizedBody child.Body}" ]
        |> String.concat "\n\n"
    rendered, List.ofSeq fixes

let private milestoneStatus body =
    let _, children = parseSubsections body
    children |> List.tryFind (fun child -> child.Heading = "Status") |> Option.map (fun child -> child.Body.Trim()) |> Option.defaultValue "Planned"

let private audit contract (document: ParsedDocument) =
    let findings = ResizeArray<Finding>()
    let normalizedSections = canonicalizeSections contract document.Sections
    let headings = normalizedSections |> List.map (fun section -> section.Heading)

    for required in contract.RequiredSections do
        if not (List.contains required headings) then
            findings.Add({ Id = "missing-section"; Severity = "error"; Message = $"Missing required section '{required}'." })

    if contract.RequireTableOfContents && not (List.contains "Table of Contents" headings) then
        findings.Add({ Id = "missing-table-of-contents"; Severity = "error"; Message = "Missing required Table of Contents." })

    if contract.RequireTableOfContents then
        match normalizedSections |> List.tryFind (fun section -> section.Heading = "Table of Contents") with
        | Some toc ->
            let expected = normalizedSections |> List.filter (fun section -> section.Heading <> "Table of Contents") |> buildToc
            if normalizedBody toc.Body <> normalizedBody expected then
                findings.Add({ Id = "stale-table-of-contents"; Severity = "error"; Message = "Table of Contents does not match the canonical top-level heading order." })
        | None -> ()

    for section in normalizedSections do
        match requiredSubsectionsFor contract section.Heading with
        | None -> ()
        | Some requiredChildren ->
            let _, children = parseSubsections section.Body
            let lookup = subsectionAliasLookup contract
            let childHeadings = children |> List.map (fun child -> canonicalizeHeading lookup child.Heading)
            for child in requiredChildren do
                if not (List.contains child childHeadings) then
                    findings.Add({ Id = "missing-subsection"; Severity = "error"; Message = $"Missing required subsection '{section.Heading} > {child}'." })

    for section in normalizedSections do
        if containsManagedPlaceholder section.Body then
            findings.Add({ Id = "placeholder-content"; Severity = "warning"; Message = $"Section '{section.Heading}' contains managed placeholder content." })

    if contract.Kind = Roadmap then
        for section in normalizedSections |> List.filter (fun value -> isMilestone value.Heading) do
            let _, children = parseSubsections section.Body
            match children |> List.tryFind (fun child -> child.Heading = "Status") with
            | Some status when canonicalStatus contract status.Body |> Option.isNone ->
                findings.Add({ Id = "invalid-milestone-status"; Severity = "error"; Message = $"{section.Heading} has unsupported status '{status.Body.Trim()}'." })
            | _ -> ()

    List.ofSeq findings

let private renderDocument preamble sections =
    [ if not (String.IsNullOrWhiteSpace preamble) then yield normalizedBody preamble
      for section in sections do
          yield $"## {section.Heading}\n\n{normalizedBody section.Body}" ]
    |> String.concat "\n\n"
    |> canonicalText

let private normalizeDocument contract template current =
    let templateSections = template.Sections |> canonicalizeSections contract
    let currentSections = current.Sections |> canonicalizeSections contract
    let templateMap = sectionMap templateSections
    let currentMap = sectionMap currentSections
    let fixes = ResizeArray<Fix>()

    let materialized =
        contract.RequiredSections
        |> List.map (fun heading ->
            let templateSection = templateMap |> Map.tryFind heading |> Option.defaultValue { Heading = heading; Body = "TBD" }
            let existing =
                match currentMap |> Map.tryFind heading with
                | Some section -> section
                | None ->
                    fixes.Add({ Id = "add-section"; Message = $"Added missing section '{heading}'." })
                    templateSection
            let body, subsectionFixes = renderSubsections contract heading existing.Body templateSection.Body
            fixes.AddRange(subsectionFixes)
            { existing with Body = body })

    let milestones = currentSections |> List.filter (fun section -> isMilestone section.Heading)
    let milestoneTemplate = templateSections |> List.tryFind (fun section -> isMilestone section.Heading)
    let normalizedMilestones =
        milestones
        |> List.map (fun milestone ->
            match milestoneTemplate with
            | None -> milestone
            | Some templateMilestone ->
                let body, subsectionFixes = renderSubsections contract milestone.Heading milestone.Body templateMilestone.Body
                fixes.AddRange(subsectionFixes)
                let statusBody, statusFixes = normalizeMilestoneStatus contract body
                fixes.AddRange(statusFixes)
                { milestone with Body = statusBody })

    let extras =
        currentSections
        |> List.filter (fun section ->
            section.Heading <> "Table of Contents"
            && not (List.contains section.Heading contract.RequiredSections)
            && not (isMilestone section.Heading))

    let materializedWithProgress =
        if contract.Kind <> Roadmap then materialized
        else
            materialized
            |> List.map (fun section ->
                if section.Heading <> "Milestone Progress" then section
                else
                    let progress =
                        normalizedMilestones
                        |> List.map (fun milestone -> $"- {milestone.Heading} - {milestoneStatus milestone.Body}")
                        |> String.concat "\n"
                    if normalizedBody section.Body <> normalizedBody progress then
                        fixes.Add({ Id = "refresh-milestone-progress"; Message = "Regenerated Milestone Progress from canonical milestone headings and statuses." })
                    { section with Body = progress })
    let allWithoutToc = materializedWithProgress @ normalizedMilestones @ extras |> topLevelOrder contract
    let withToc =
        if contract.RequireTableOfContents then
            { Heading = "Table of Contents"; Body = buildToc allWithoutToc } :: allWithoutToc
        else allWithoutToc
    let preamble =
        if contract.PreservePreamble && not (String.IsNullOrWhiteSpace current.Preamble) then current.Preamble
        else template.Preamble
    renderDocument preamble withToc, List.ofSeq fixes

let private resolveInside (root: string) (requested: string option) (fallback: string) =
    let rootPath = Path.GetFullPath(root)
    let candidate =
        requested
        |> Option.map (fun path -> if Path.IsPathRooted(path) then path else Path.Combine(rootPath, path))
        |> Option.defaultValue (Path.Combine(rootPath, fallback))
        |> Path.GetFullPath
    let prefix = rootPath.TrimEnd(Path.DirectorySeparatorChar) + string Path.DirectorySeparatorChar
    if candidate <> rootPath && not (candidate.StartsWith(prefix, StringComparison.Ordinal)) then
        failwith $"Target path must remain inside project root: {candidate}"
    candidate

let private atomicWrite (path: string) (content: string) =
    let directory = Path.GetDirectoryName(path)
    Directory.CreateDirectory(directory) |> ignore
    let temporary = Path.Combine(directory, $".{Path.GetFileName(path)}.{Guid.NewGuid():N}.tmp")
    File.WriteAllText(temporary, content, UTF8Encoding(false))
    File.Move(temporary, path, true)

let planDocument contractPath templatePath options =
    try
        let root = Path.GetFullPath(options.ProjectRoot)
        if not (Directory.Exists(root)) then failwith $"Project root does not exist: {root}"
        let contract = loadContract contractPath
        if contract.SchemaVersion <> 1 then failwith $"Unsupported document contract schema: {contract.SchemaVersion}"
        let target = resolveInside root options.TargetPath contract.TargetFile
        let template = File.ReadAllText(templatePath) |> parseDocument
        let currentText = if File.Exists(target) then File.ReadAllText(target) else File.ReadAllText(templatePath)
        let current = parseDocument currentText
        let beforeFindings = audit contract current
        let rendered, fixes = normalizeDocument contract template current
        let changed = not (File.Exists(target)) || canonicalText currentText <> rendered
        let finalDocument = if options.RunMode = Apply then parseDocument rendered else current
        let finalFindings = audit contract finalDocument
        let report = {
                Document = contract.TargetFile
                Path = Path.GetRelativePath(root, target)
                Mode = if options.RunMode = Apply then "apply" else "check-only"
                Findings = if options.RunMode = Apply then finalFindings else beforeFindings
                Fixes = if options.RunMode = Apply then fixes else []
                Changed = options.RunMode = Apply && changed
                Errors = []
            }
        {
            Report = report
            TargetPath = target
            Original = if File.Exists(target) then Some currentText else None
            Rendered = rendered
        }
    with error ->
        let target = options.TargetPath |> Option.defaultValue ""
        {
            Report = {
                Document = Path.GetFileName(target)
                Path = target
                Mode = if options.RunMode = Apply then "apply" else "check-only"
                Findings = []
                Fixes = []
                Changed = false
                Errors = [ error.Message ]
            }
            TargetPath = target
            Original = None
            Rendered = ""
        }

let applyPlans plans =
    let errors = plans |> List.collect (fun plan -> plan.Report.Errors)
    if not (List.isEmpty errors) then Error errors
    else
        let changed = plans |> List.filter (fun plan -> plan.Report.Changed)
        let completed = ResizeArray<DocumentPlan>()
        try
            for plan in changed do
                atomicWrite plan.TargetPath plan.Rendered
                completed.Add(plan)
            Ok ()
        with error ->
            for plan in Seq.rev completed do
                match plan.Original with
                | Some content -> atomicWrite plan.TargetPath content
                | None when File.Exists(plan.TargetPath) -> File.Delete(plan.TargetPath)
                | None -> ()
            Error [ $"Documentation apply failed and completed writes were rolled back: {error.Message}" ]

let runDocument contractPath templatePath options =
    let plan = planDocument contractPath templatePath options
    if options.RunMode = Apply then
        match applyPlans [ plan ] with
        | Ok () -> plan.Report
        | Error errors -> { plan.Report with Changed = false; Errors = errors }
    else plan.Report

let private jsonOptions =
    let options = JsonSerializerOptions(WriteIndented = true)
    options.PropertyNamingPolicy <- JsonNamingPolicy.CamelCase
    options

let reportJson report = JsonSerializer.Serialize(report, jsonOptions) + "\n"

let reportMarkdown report =
    let lines = ResizeArray<string>()
    lines.Add($"# {report.Document} maintenance report")
    lines.Add("")
    lines.Add($"- Mode: `{report.Mode}`")
    lines.Add($"- Changed: `{report.Changed.ToString().ToLowerInvariant()}`")
    lines.Add("")
    lines.Add("## Findings")
    lines.Add("")
    if List.isEmpty report.Findings then lines.Add("- None.")
    else for finding in report.Findings do lines.Add($"- `{finding.Severity}` `{finding.Id}`: {finding.Message}")
    lines.Add("")
    lines.Add("## Fixes")
    lines.Add("")
    if List.isEmpty report.Fixes then lines.Add("- None.")
    else for fix in report.Fixes do lines.Add($"- `{fix.Id}`: {fix.Message}")
    lines.Add("")
    lines.Add("## Errors")
    lines.Add("")
    if List.isEmpty report.Errors then lines.Add("- None.")
    else for error in report.Errors do lines.Add($"- {error}")
    String.Join("\n", lines) + "\n"

let parseCli defaultTarget argv =
    let mutable root = "."
    let mutable target: string option = None
    let mutable mode = CheckOnly
    let mutable format = "markdown"
    let mutable failOnIssues = false
    let mutable collectSource = false
    let mutable collectGithub = false
    let mutable githubRepo: string option = None
    let mutable ticketSection: string option = None
    let mutable ticketText: string option = None
    let mutable ticketState: string option = None
    let mutable ticketSource: string option = None
    let mutable ticketMatch: string option = None
    let mutable allowDuplicate = false
    let args = List.ofArray argv
    let rec loop remaining =
        match remaining with
        | [] -> ()
        | "--project-root" :: value :: tail -> root <- value; loop tail
        | "--target-path" :: value :: tail -> target <- Some value; loop tail
        | "--run-mode" :: "check-only" :: tail -> mode <- CheckOnly; loop tail
        | "--run-mode" :: "apply" :: tail -> mode <- Apply; loop tail
        | "--format" :: value :: tail -> format <- value; loop tail
        | "--fail-on-issues" :: tail -> failOnIssues <- true; loop tail
        | "--collect-source-tickets" :: tail -> collectSource <- true; loop tail
        | "--collect-github-issues" :: tail -> collectGithub <- true; loop tail
        | "--github-repo" :: value :: tail -> githubRepo <- Some value; loop tail
        | "--ticket-section" :: value :: tail -> ticketSection <- Some value; loop tail
        | "--ticket-text" :: value :: tail -> ticketText <- Some value; loop tail
        | "--ticket-state" :: value :: tail -> ticketState <- Some value; loop tail
        | "--ticket-source" :: value :: tail -> ticketSource <- Some value; loop tail
        | "--ticket-match" :: value :: tail -> ticketMatch <- Some value; loop tail
        | "--allow-duplicate" :: tail -> allowDuplicate <- true; loop tail
        | unknown :: _ -> failwith $"Unknown argument: {unknown}"
    loop args
    {
        ProjectRoot = root
        TargetPath = target |> Option.orElse (Some defaultTarget)
        RunMode = mode
        Format = format
        FailOnIssues = failOnIssues
        CollectSourceTickets = collectSource
        CollectGithubIssues = collectGithub
        GithubRepo = githubRepo
        TicketSection = ticketSection
        TicketText = ticketText
        TicketState = ticketState
        TicketSource = ticketSource
        TicketMatch = ticketMatch
        AllowDuplicate = allowDuplicate
    }

let execute contractPath templatePath defaultTarget argv =
    try
        let options = parseCli defaultTarget argv
        let report = runDocument contractPath templatePath options
        let output = if options.Format = "json" then reportJson report else reportMarkdown report
        Console.Out.Write(output)
        if not (List.isEmpty report.Errors) then 1
        elif options.FailOnIssues && not (List.isEmpty report.Findings) then 2
        else 0
    with error ->
        Console.Error.WriteLine($"ERROR: {error.Message}")
        1
