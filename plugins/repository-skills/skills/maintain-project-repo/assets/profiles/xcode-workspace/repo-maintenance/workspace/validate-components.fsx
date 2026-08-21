open System
open System.Diagnostics
open System.IO

let maintenanceRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))
let repoRoot = Path.GetFullPath(Path.Combine(maintenanceRoot, "..", ".."))

let componentRoots = [ "Apps"; "Packages"; "Services" ]

for container in componentRoots do
    let path = Path.Combine(repoRoot, container)
    if Directory.Exists(path) then
        for component in Directory.GetDirectories(path) |> Array.sort do
            let script = Path.Combine(component, "scripts", "repo-maintenance", "repo-maintenance.fsx")
            if File.Exists(script) then
                let info = ProcessStartInfo("dotnet")
                info.WorkingDirectory <- component
                info.UseShellExecute <- false
                info.ArgumentList.Add("fsi")
                info.ArgumentList.Add(script)
                info.ArgumentList.Add("validate")
                use child = Process.Start(info)
                child.WaitForExit()
                if child.ExitCode <> 0 then failwith $"Component validation failed: {component}"

printfn "Validated xcode-workspace components."
