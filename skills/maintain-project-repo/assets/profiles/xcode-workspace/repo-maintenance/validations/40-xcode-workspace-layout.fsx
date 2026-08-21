open System
open System.IO
open System.Text.Json

let maintenanceRoot = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, ".."))
let repoRoot = Path.GetFullPath(Path.Combine(maintenanceRoot, "..", ".."))

let exactlyOne pattern = Directory.GetDirectories(repoRoot, pattern, SearchOption.TopDirectoryOnly).Length = 1
let requiredDirectories = [ "Apps"; "Packages"; "Services" ]

if not (exactlyOne "*.xcworkspace") then failwith "xcode-workspace profile requires exactly one root .xcworkspace."
if not (exactlyOne "*.xcodeproj") then failwith "xcode-workspace profile requires exactly one root .xcodeproj."
if not (File.Exists(Path.Combine(repoRoot, "project.yml"))) then failwith "xcode-workspace profile requires root project.yml."
for directory in requiredDirectories do
    if not (Directory.Exists(Path.Combine(repoRoot, directory))) then failwith $"xcode-workspace profile requires {directory}/."

printfn "Validated canonical xcode-workspace layout."
