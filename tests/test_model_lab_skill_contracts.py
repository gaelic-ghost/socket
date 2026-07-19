from __future__ import annotations

import importlib.util
import json
import os
import sys
import tomllib
from pathlib import Path
from types import ModuleType

import pytest
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
    errors = module.validate(template)
    assert errors
    assert any("template placeholder" in error for error in errors)
    template["experiment"].update(
        id="exp-001",
        title="Adapter comparison",
        hypothesis="The adapter improves the held-out score.",
        decision="Choose whether to deploy the adapter.",
        owner="model-team",
    )
    template["provenance"]["code_revision"] = "abc123"
    template["provenance"]["model"].update(
        id="model", revision="rev", license="license"
    )
    template["provenance"]["tokenizer"].update(id="tokenizer", revision="rev")
    template["provenance"]["dataset"].update(id="dataset", revision="rev")
    template["provenance"]["environment"].update(lockfile="uv.lock", hardware="M4 Pro")
    template["method"].update(
        controlled_variable="adapter", baseline="base", treatment="adapter"
    )
    template["evaluation"]["primary_metrics"] = ["accuracy"]
    template["evaluation"]["guardrail_metrics"] = ["regression"]
    template["evaluation"]["failure_thresholds"] = {"accuracy": 0.5}
    template["budget"]["smoke_run"] = "10 cases"
    template["budget"]["full_run"] = "100 cases"
    template["budget"]["stop_conditions"] = ["cost exceeds budget"]
    template["artifacts"].update(
        raw_results="raw", derived_results="derived", report="report.md"
    )
    assert module.validate(template) == []
    template["budget"]["maximum_cost_usd"] = "free"
    assert (
        "`budget.maximum_cost_usd` must be a finite non-negative number."
        in module.validate(template)
    )
    template["budget"]["maximum_cost_usd"] = 0
    template["evaluation"]["primary_metrics"] = ["replace-with-primary-metric"]
    assert any(
        "evaluation.primary_metrics" in error and "placeholder" in error
        for error in module.validate(template)
    )
    template["evaluation"]["primary_metrics"] = ["accuracy"]
    template["evaluation"]["failure_thresholds"] = {
        "replace-with-metric": "replace-with-threshold"
    }
    assert any(
        "evaluation.failure_thresholds" in error and "placeholder" in error
        for error in module.validate(template)
    )


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
    assert module.paired_ids(baseline, treatment, allow_partial=False) == ["a", "b"]
    comparison = module.build_comparison(baseline, treatment)
    assert comparison["mean_paired_delta"] == -0.25
    assert comparison["improved"] == 1
    assert comparison["regressed"] == 1
    assert comparison["partial_comparison"] is False


def test_eval_comparison_rejects_missing_or_overwritten_inputs(tmp_path: Path) -> None:
    module = load_module(
        "model_lab_eval_comparison_guards",
        SKILLS_ROOT / "evaluate-language-model" / "scripts" / "compare_eval_runs.py",
    )
    with pytest.raises(ValueError, match="identical case ids"):
        module.paired_ids({"a": {"score": 1}}, {"b": {"score": 1}}, False)
    baseline = tmp_path / "baseline.jsonl"
    treatment = tmp_path / "treatment.jsonl"
    with pytest.raises(ValueError, match="overwrite an input"):
        module.validate_output_path(baseline, baseline, treatment)
    baseline.write_text("baseline", encoding="utf-8")
    hard_link = tmp_path / "hard-link.jsonl"
    os.link(baseline, hard_link)
    with pytest.raises(ValueError, match="overwrite an input"):
        module.validate_output_path(hard_link, baseline, treatment)
    with pytest.raises(ValueError, match="could not write output"):
        module.write_output(tmp_path / "missing" / "output.json", "{}")
    invalid = tmp_path / "invalid.jsonl"
    invalid.write_text('{"id":"a","score":NaN}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="finite numeric"):
        module.load_results(invalid)


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
    snapshot = module.build_snapshot(tmp_path, "model", "revision")
    entries = snapshot["files"]
    assert [entry["path"] for entry in entries] == ["a.bin", "z.bin"]
    assert all(len(entry["sha256"]) == 64 for entry in entries)
    assert snapshot["file_count"] == 2
    with pytest.raises(ValueError, match="outside the model artifact directory"):
        module.validate_output_path(tmp_path, tmp_path / "snapshot.json")
    with pytest.raises(ValueError, match="overwrite the model artifact"):
        module.validate_output_path(first, first)
    external_link = tmp_path.parent / f"{tmp_path.name}-model-hard-link"
    os.link(first, external_link)
    try:
        with pytest.raises(ValueError, match="hard-link alias"):
            module.validate_output_path(tmp_path, external_link)
    finally:
        external_link.unlink()
    with pytest.raises(ValueError, match="could not write output"):
        module.write_output(tmp_path / "missing" / "snapshot.json", "{}")


def test_plugin_manifest_matches_socket_version() -> None:
    plugin = json.loads(
        (
            ROOT / "plugins" / "model-lab-skills" / ".codex-plugin" / "plugin.json"
        ).read_text(encoding="utf-8")
    )
    with (ROOT / "pyproject.toml").open("rb") as stream:
        root_project = tomllib.load(stream)
    assert plugin["version"] == root_project["project"]["version"]
