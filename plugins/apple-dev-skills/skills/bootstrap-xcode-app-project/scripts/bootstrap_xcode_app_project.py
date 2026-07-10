#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# ///
"""Create the current supported XcodeGen-backed app-project scaffold."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

XCODEGEN_TEMPLATE_DIR = Path(__file__).resolve().parents[3] / "templates" / "xcodegen" / "swiftui-app"
XCODEGEN_TEMPLATE_OUTPUTS = {
    "project.yml.tmpl": "project.yml",
    "Sources/Support/App.entitlements.tmpl": "Sources/Support/__APP_NAME__.entitlements",
    "Sources/Resources/Assets.xcassets/Contents.json.tmpl": "Sources/Resources/Assets.xcassets/Contents.json",
    "Sources/Resources/Assets.xcassets/AccentColor.colorset/Contents.json.tmpl": "Sources/Resources/Assets.xcassets/AccentColor.colorset/Contents.json",
    "Sources/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json.tmpl": "Sources/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json",
    "Configurations/Shared.xcconfig.tmpl": "Configurations/Shared.xcconfig",
    "Configurations/App.xcconfig.tmpl": "Configurations/App.xcconfig",
    "Configurations/App-Debug.xcconfig.tmpl": "Configurations/App-Debug.xcconfig",
    "Configurations/App-Release.xcconfig.tmpl": "Configurations/App-Release.xcconfig",
    "Configurations/Tests.xcconfig.tmpl": "Configurations/Tests.xcconfig",
    "Configurations/Tests-Debug.xcconfig.tmpl": "Configurations/Tests-Debug.xcconfig",
    "Configurations/Tests-Release.xcconfig.tmpl": "Configurations/Tests-Release.xcconfig",
}

STANDARD_TOP_LEVEL_DIRECTORIES = (
    "Sources",
    "Tests",
    "Shared",
    "Extensions",
    "Configurations",
    "Scripts",
    "Packages",
)

STANDARD_SOURCE_DIRECTORIES = (
    "Sources/Views/Shared",
    "Sources/Views/macOS",
    "Sources/Views/iOS",
    "Sources/Models",
    "Sources/Services/Consumed",
    "Sources/Services/Internal",
    "Sources/Services/Provided",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True)
    parser.add_argument("--file-prefix", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--ui-stack", required=True)
    parser.add_argument("--project-generator", required=True)
    parser.add_argument("--bundle-identifier", required=True)
    parser.add_argument("--org-identifier", required=True)
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--copy-agents", action="store_true")
    return parser


def blocked_payload(path: Path, inputs: dict, next_step: str, *, stderr: str = "", validation_result: str | None = None) -> dict:
    return {
        "status": "blocked",
        "path_type": "primary",
        "resolved_path": str(path),
        "normalized_inputs": inputs,
        "validation_result": validation_result,
        "stderr": stderr,
        "next_step": next_step,
    }


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_template(relative_path: str, replacements: dict[str, str]) -> str:
    template_path = XCODEGEN_TEMPLATE_DIR / relative_path
    if not template_path.is_file():
        raise RuntimeError(f"XcodeGen template is missing: {template_path}")
    text = template_path.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    return text


def install_xcodegen_templates(target_dir: Path, name: str, platform: str, bundle_identifier: str) -> list[str]:
    xcodegen_platform = "iOS" if platform in {"ios", "ipados"} else "macOS"
    replacements = {
        "__APP_NAME__": name,
        "__BUNDLE_IDENTIFIER__": bundle_identifier,
        "__XCODEGEN_PLATFORM__": xcodegen_platform,
    }
    installed_paths: list[str] = []
    for template_relative_path, output_relative_path in XCODEGEN_TEMPLATE_OUTPUTS.items():
        rendered_output_relative_path = output_relative_path
        for placeholder, value in replacements.items():
            rendered_output_relative_path = rendered_output_relative_path.replace(placeholder, value)
        output_path = target_dir / rendered_output_relative_path
        write_text(output_path, render_template(template_relative_path, replacements))
        installed_paths.append(str(output_path))
    return installed_paths


def install_standard_directories(target_dir: Path) -> list[str]:
    installed_paths: list[str] = []
    for relative_path in STANDARD_TOP_LEVEL_DIRECTORIES + STANDARD_SOURCE_DIRECTORIES:
        directory = target_dir / relative_path
        directory.mkdir(parents=True, exist_ok=True)
        installed_paths.append(str(directory))

    for relative_path in (
        "Shared/.gitkeep",
        "Extensions/.gitkeep",
        "Scripts/.gitkeep",
        "Packages/.gitkeep",
        "Sources/Views/macOS/.gitkeep",
        "Sources/Views/iOS/.gitkeep",
        "Sources/Models/.gitkeep",
        "Sources/Services/Consumed/.gitkeep",
        "Sources/Services/Provided/.gitkeep",
    ):
        placeholder = target_dir / relative_path
        write_text(placeholder, "")
        installed_paths.append(str(placeholder))

    return installed_paths


def install_local_environment(target_dir: Path, scheme_name: str) -> str:
    template_path = (
        Path(__file__).resolve().parents[3]
        / "templates"
        / "codex-local-environments"
        / "xcode-project.toml"
    )
    target_path = target_dir / ".codex" / "environments" / "xcode-project.toml"
    if not template_path.is_file():
        raise RuntimeError(f"Codex local environment template is missing: {template_path}")
    template_text = template_path.read_text(encoding="utf-8").replace("SCHEME_NAME", scheme_name)
    write_text(target_path, template_text)
    return str(target_path)


def render_app_file(prefix: str) -> str:
    app_type = f"{prefix}App"
    return f"""import SwiftUI

@main
struct {app_type}: App {{
    @State private var service = {prefix}AppService()

    var body: some Scene {{
        WindowGroup {{
            {prefix}ContentView(viewModel: {prefix}ContentViewModel(service: service))
                .environment(service)
        }}
    }}
}}
"""


def render_app_domain(prefix: str) -> str:
    return f"""struct {prefix} {{
    var title = "Hello, world!"
}}
"""

def render_app_service(prefix: str) -> str:
    return f"""import Observation

@Observable
final class {prefix}AppService {{
    var app = {prefix}()
}}
"""


def render_content_view(prefix: str) -> str:
    return f"""import SwiftUI

struct {prefix}ContentView: View {{
    @State var viewModel: {prefix}ContentViewModel

    var body: some View {{
        Text(viewModel.title)
            .padding()
    }}
}}
"""


def render_content_view_model(prefix: str) -> str:
    return f"""import Observation

@Observable
final class {prefix}ContentViewModel {{
    private let service: {prefix}AppService

    var title: String {{ service.app.title }}

    init(service: {prefix}AppService) {{
        self.service = service
    }}
}}
"""


def render_test_file(name: str, prefix: str) -> str:
    return f"""import XCTest
@testable import {name}

final class {prefix}AppTests: XCTestCase {{
    func testExample() throws {{
        XCTAssertTrue(true)
    }}
}}
"""


def maintain_project_repo_runner() -> Path:
    plugins_root = Path(__file__).resolve().parents[4]
    runner = plugins_root / "productivity-skills" / "skills" / "maintain-project-repo" / "scripts" / "run_workflow.py"
    if not runner.is_file():
        raise RuntimeError(
            "bootstrap-xcode-app-project needs productivity-skills/maintain-project-repo "
            f"to install repo-maintenance files, but the runner was missing at {runner}. "
            "Install productivity-skills alongside apple-dev-skills, or add the socket "
            "marketplace with 'codex plugin marketplace add gaelic-ghost/socket' and "
            "enable both apple-dev-skills and productivity-skills from the Socket catalog, "
            "then rerun this workflow."
        )
    return runner


def main() -> int:
    args = build_parser().parse_args()
    target_dir = (Path(args.destination).expanduser() / args.name).resolve()
    normalized_inputs = {
        "name": args.name,
        "file_prefix": args.file_prefix,
        "destination": args.destination,
        "platform": args.platform,
        "ui_stack": args.ui_stack,
        "project_generator": args.project_generator,
        "bundle_identifier": args.bundle_identifier,
        "org_identifier": args.org_identifier,
        "skip_validation": args.skip_validation,
        "copy_agents_md": args.copy_agents,
    }

    if args.project_generator != "xcodegen":
        payload = blocked_payload(
            target_dir,
            normalized_inputs,
            "Use the documented XcodeGen path for the current supported mutating implementation.",
            stderr="bootstrap_xcode_app_project.py only supports the xcodegen path.",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if args.ui_stack != "swiftui":
        payload = blocked_payload(
            target_dir,
            normalized_inputs,
            "Switch to --ui-stack swiftui for the current supported mutating implementation or use the guided path.",
            stderr="The first supported mutating implementation only scaffolds SwiftUI app projects.",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if not re.fullmatch(r"[A-Z]{3}", args.file_prefix):
        payload = blocked_payload(
            target_dir,
            normalized_inputs,
            "Choose an explicit three-letter uppercase Swift file prefix and rerun the workflow.",
            stderr="--file-prefix must contain exactly three uppercase ASCII letters.",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    if target_dir.exists() and any(target_dir.iterdir()):
        payload = blocked_payload(
            target_dir,
            normalized_inputs,
            "Choose an empty destination directory and rerun the workflow.",
            stderr="The target directory already exists and is not empty.",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    xcodegen = os.environ.get("XCODEGEN_BIN") or shutil.which("xcodegen")
    if not xcodegen or not Path(xcodegen).exists():
        payload = blocked_payload(
            target_dir,
            normalized_inputs,
            "Install XcodeGen or choose the guided Xcode path and rerun the workflow.",
            stderr="xcodegen is required for the current supported mutating path.",
        )
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)
    standard_directory_paths = install_standard_directories(target_dir)

    try:
        xcodegen_template_paths = install_xcodegen_templates(
            target_dir,
            args.name,
            args.platform,
            args.bundle_identifier,
        )
    except RuntimeError as exc:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "resolved_path": str(target_dir),
            "normalized_inputs": normalized_inputs,
            "validation_result": "failed (xcodegen template install)",
            "stderr": str(exc),
            "next_step": "Restore the bootstrap XcodeGen templates and rerun bootstrap-xcode-app-project.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    prefix = args.file_prefix
    write_text(target_dir / f"Sources/{prefix}App.swift", render_app_file(prefix))
    write_text(target_dir / f"Sources/{prefix}.swift", render_app_domain(prefix))
    write_text(target_dir / f"Sources/Services/Internal/{prefix}AppService.swift", render_app_service(prefix))
    write_text(target_dir / f"Sources/Views/Shared/{prefix}ContentView.swift", render_content_view(prefix))
    write_text(target_dir / f"Sources/Views/Shared/{prefix}ContentViewModel.swift", render_content_view_model(prefix))
    write_text(target_dir / f"Tests/{args.name}Tests/{prefix}AppTests.swift", render_test_file(args.name, prefix))
    try:
        local_environment_path = install_local_environment(target_dir, args.name)
    except RuntimeError as exc:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "resolved_path": str(target_dir),
            "normalized_inputs": normalized_inputs,
            "validation_result": "failed (codex local environment install)",
            "stderr": str(exc),
            "next_step": "Resolve the Codex local environment template path and rerun bootstrap-xcode-app-project.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    agents_copied = False
    if args.copy_agents:
        agents_template = Path(__file__).resolve().parents[1] / "assets" / "AGENTS.md"
        if agents_template.exists():
            shutil.copyfile(agents_template, target_dir / "AGENTS.md")
            agents_copied = True

    try:
        runner = maintain_project_repo_runner()
    except RuntimeError as exc:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "resolved_path": str(target_dir),
            "normalized_inputs": normalized_inputs,
            "validation_result": "failed (maintain-project-repo install)",
            "stderr": str(exc),
            "next_step": "Install productivity-skills alongside apple-dev-skills, or add the socket marketplace and enable both plugin entries from the Socket catalog, then rerun bootstrap-xcode-app-project.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    proc_install_toolkit = subprocess.run(
        [
            str(runner),
            "--repo-root",
            str(target_dir),
            "--operation",
            "install",
            "--profile",
            "xcode-app",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_install_toolkit.returncode != 0:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "resolved_path": str(target_dir),
            "normalized_inputs": normalized_inputs,
            "validation_result": "failed (maintain-project-repo install)",
            "stdout": proc_install_toolkit.stdout,
            "stderr": proc_install_toolkit.stderr,
            "next_step": "Fix the maintain-project-repo install failure and rerun the workflow.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    proc_generate = subprocess.run(
        [xcodegen, "generate", "--spec", "project.yml"],
        cwd=target_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc_generate.returncode != 0:
        payload = {
            "status": "failed",
            "path_type": "primary",
            "resolved_path": str(target_dir),
            "normalized_inputs": normalized_inputs,
            "validation_result": "failed (xcodegen generate)",
            "stdout": proc_generate.stdout,
            "stderr": proc_generate.stderr,
            "next_step": "Fix the XcodeGen generation failure and rerun the workflow.",
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1

    validation_result = "skipped (--skip-validation)"
    validation_stdout = ""
    validation_stderr = ""
    if not args.skip_validation:
        xcodebuild = os.environ.get("XCODEBUILD_BIN") or shutil.which("xcodebuild")
        if xcodebuild and Path(xcodebuild).exists():
            proc_validate = subprocess.run(
                [xcodebuild, "-list", "-project", f"{args.name}.xcodeproj"],
                cwd=target_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            validation_stdout = proc_validate.stdout
            validation_stderr = proc_validate.stderr
            if proc_validate.returncode != 0:
                payload = {
                    "status": "failed",
                    "path_type": "primary",
                    "resolved_path": str(target_dir),
                    "normalized_inputs": normalized_inputs,
                    "validation_result": "failed (xcodebuild -list)",
                    "stdout": validation_stdout,
                    "stderr": validation_stderr,
                    "next_step": "Fix the generated project introspection failure and rerun the workflow.",
                }
                print(json.dumps(payload, indent=2, sort_keys=True))
                return 1
            validation_result = "passed (xcodebuild -list)"
        else:
            validation_result = "skipped (xcodebuild unavailable)"

    payload = {
        "status": "success",
        "path_type": "primary",
        "resolved_path": str(target_dir),
        "normalized_inputs": normalized_inputs,
        "validation_result": validation_result,
        "generator": "xcodegen",
        "project_file": str(target_dir / f"{args.name}.xcodeproj"),
        "xcodegen_template_paths": xcodegen_template_paths,
        "standard_directory_paths": standard_directory_paths,
        "local_environment_path": local_environment_path,
        "agents_copied": agents_copied,
        "stdout": proc_install_toolkit.stdout + proc_generate.stdout + validation_stdout,
        "stderr": proc_install_toolkit.stderr + proc_generate.stderr + validation_stderr,
        "next_step": "Use xcode-build-run-workflow for normal build or run work inside the generated project, and use xcode-testing-workflow when the task is primarily about tests.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
