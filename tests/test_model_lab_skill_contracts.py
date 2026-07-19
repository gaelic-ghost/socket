from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import yaml


ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = ROOT / "plugins" / "model-lab-skills" / "skills"
EXPECTED_SKILLS = {
    "choose-model-lab-workflow",
    "design-model-experiment",
    "prepare-language-model-dataset",
    "fine-tune-language-model",
    "evaluate-language-model",
    "compare-model-checkpoints",
    "choose-apple-model-runtime",
    "research-model-representations",
    "steer-language-model-behavior",
    "ablate-refusal-representations",
    "evaluate-jailbreak-resilience",
    "evaluate-tool-calling-model",
    "benchmark-model-runtime",
}


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def skill_text(name: str) -> str:
    return (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8").lower()


def test_inventory_is_complete_and_has_no_scaffold_placeholders() -> None:
    assert {
        path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()
    } == EXPECTED_SKILLS
    for name in EXPECTED_SKILLS:
        contents = skill_text(name)
        assert "[todo" not in contents
        assert "structuring this skill" not in contents
        assert (SKILLS_ROOT / name / "agents" / "openai.yaml").is_file()


def test_routing_preserves_neighbor_plugin_ownership() -> None:
    contents = skill_text("choose-model-lab-workflow")
    for owner in (
        "cloud-inference-skills",
        "python-skills",
        "apple-dev-skills",
        "productivity-skills",
        "cybersecurity-skills",
    ):
        assert owner in contents


def test_apple_runtime_covers_current_source_lanes() -> None:
    contents = skill_text("choose-apple-model-runtime")
    for term in (
        "coreai-models",
        "coreai-torch",
        "coreai-optimization",
        "coremltools",
        "mlx swift",
        "mlx lm",
        "executorch core ml",
        "experimental mlx",
        "foundation models",
    ):
        assert term in contents


def test_adversarial_workflows_keep_authorization_and_regression_controls() -> None:
    ablation = skill_text("ablate-refusal-representations")
    jailbreak = skill_text("evaluate-jailbreak-resilience")
    assert "authorized" in ablation
    assert "capability" in ablation
    assert "random norm-matched" in ablation
    assert "explicit authorization" in jailbreak
    assert "benign over-refusal" in jailbreak
    assert "side-effect" in jailbreak


def test_experiment_manifest_template_is_valid() -> None:
    module = load_module(
        "model_lab_manifest_validator",
        SKILLS_ROOT
        / "design-model-experiment"
        / "scripts"
        / "validate_experiment_manifest.py",
    )
    template = yaml.safe_load(
        (
            SKILLS_ROOT
            / "design-model-experiment"
            / "assets"
            / "experiment-manifest.yaml"
        ).read_text(encoding="utf-8")
    )
    assert module.validate(template) == []


def test_eval_comparison_reports_paired_regressions(tmp_path: Path) -> None:
    module = load_module(
        "model_lab_eval_comparison",
        SKILLS_ROOT / "evaluate-language-model" / "scripts" / "compare_eval_runs.py",
    )
    baseline_path = tmp_path / "baseline.jsonl"
    treatment_path = tmp_path / "treatment.jsonl"
    baseline_path.write_text(
        '{"id":"a","score":0.5}\n{"id":"b","score":1.0}\n', encoding="utf-8"
    )
    treatment_path.write_text(
        '{"id":"a","score":1.0}\n{"id":"b","score":0.0}\n', encoding="utf-8"
    )
    baseline = module.load_results(baseline_path)
    treatment = module.load_results(treatment_path)
    assert set(baseline) == {"a", "b"}
    assert treatment["b"]["score"] == 0.0


def test_provenance_snapshot_uses_sorted_relative_paths(tmp_path: Path) -> None:
    module = load_module(
        "model_lab_provenance_snapshot",
        SKILLS_ROOT
        / "compare-model-checkpoints"
        / "scripts"
        / "snapshot_model_provenance.py",
    )
    first = tmp_path / "z.bin"
    second = tmp_path / "a.bin"
    first.write_bytes(b"z")
    second.write_bytes(b"a")
    entries = [
        {"path": path.name, "sha256": module.digest(path)}
        for path in sorted((first, second))
    ]
    assert [entry["path"] for entry in entries] == ["a.bin", "z.bin"]
    assert all(len(entry["sha256"]) == 64 for entry in entries)


def test_plugin_manifest_matches_socket_version() -> None:
    plugin = json.loads(
        (
            ROOT / "plugins" / "model-lab-skills" / ".codex-plugin" / "plugin.json"
        ).read_text(encoding="utf-8")
    )
    root_project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert plugin["version"] == "9.17.0"
    assert 'version = "9.17.0"' in root_project
