from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import importlib.util


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "speak_with_profile.py"
    spec = importlib.util.spec_from_file_location("speak_with_profile", module_path)
    assert spec is not None
    assert spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


m = _load_module()


class SpeakWithProfileTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)

    def _write_profiles(self) -> Path:
        path = self.root / "profiles.yaml"
        path.write_text(
            """
version: "1"
default_profile: default-general
profiles:
  - id: default-general
    voice: cedar
    instructions: Base instruction
    speed: 1.0
    response_format: mp3
  - id: a11y-slow-clear
    voice: marin
    instructions: Slow and clear
    speed: 0.9
    response_format: wav
""".strip()
            + "\n",
            encoding="utf-8",
        )
        return path

    def _set_cwd_root(self) -> None:
        old_cwd = os.getcwd()
        os.chdir(self.root)
        self.addCleanup(lambda: os.chdir(old_cwd))

    def _write_customization(self, relative_path: str, content: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")
        return path

    def test_unknown_profile_raises(self) -> None:
        profiles = m.load_profiles(self._write_profiles())
        ns = type("NS", (), {"profile": "missing", "voice": None, "instructions": None, "speed": None, "format": None, "model": None})
        with self.assertRaises(m.WrapperError):
            m.resolve_effective_config(ns, profiles)

    def test_precedence_flag_over_profile_over_defaults(self) -> None:
        profiles = m.load_profiles(self._write_profiles())
        ns = type(
            "NS",
            (),
            {
                "profile": "a11y-slow-clear",
                "voice": "ash",
                "instructions": None,
                "speed": None,
                "format": "aac",
                "model": None,
            },
        )
        effective, profile_id, profile_source, disclosure = m.resolve_effective_config(ns, profiles)
        self.assertEqual(profile_id, "a11y-slow-clear")
        self.assertEqual(profile_source, "file")
        self.assertEqual(disclosure, m.DEFAULT_DISCLOSURE)
        self.assertEqual(effective["voice"], "ash")
        self.assertEqual(effective["response_format"], "aac")
        self.assertEqual(effective["instructions"], "Slow and clear")
        self.assertEqual(effective["speed"], 0.9)

    def test_runtime_config_override_beats_template(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  defaultDisclosure: "Template disclosure."
  localCli:
    defaultPlaybackBackend: open
""",
        )
        self._write_customization(
            "config/customization.yaml",
            """
version: "1"
workflow:
  defaultDisclosure: "Override disclosure."
  localCli:
    defaultPlaybackBackend: afplay
""",
        )

        config = m.load_runtime_config()
        self.assertEqual(config.default_disclosure, "Override disclosure.")
        self.assertEqual(config.local_playback_backend, "afplay")

    def test_explicit_flags_beat_runtime_config(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  defaultDisclosure: "Template disclosure."
""",
        )

        profiles = m.load_profiles(self._write_profiles())
        ns = type(
            "NS",
            (),
            {
                "profile": "a11y-slow-clear",
                "voice": None,
                "instructions": "Explicit instruction",
                "speed": None,
                "format": None,
                "model": None,
            },
        )
        effective, _, _, disclosure = m.resolve_effective_config(ns, profiles, m.load_runtime_config())
        self.assertEqual(effective["instructions"], "Explicit instruction")
        self.assertEqual(disclosure, "Template disclosure.")

    def test_missing_runtime_config_preserves_defaults(self) -> None:
        self._set_cwd_root()
        config = m.load_runtime_config()
        self.assertEqual(config.default_profiles_file, m.DEFAULT_PROFILES_FILE)
        self.assertEqual(config.default_disclosure, m.DEFAULT_DISCLOSURE)
        self.assertEqual(config.local_output_dir, "output/speech")
        self.assertEqual(config.local_playback_backend, "none")
        self.assertFalse(config.local_autoplay_generated_audio)

    def test_config_default_profiles_file_used_when_flag_absent(self) -> None:
        self._set_cwd_root()
        profiles_dir = self.root / "custom-profiles"
        profiles_dir.mkdir(parents=True, exist_ok=True)
        profiles_path = profiles_dir / "profiles.yaml"
        profiles_path.write_text(
            """
version: "1"
default_profile: from-config
profiles:
  - id: from-config
    voice: marin
    instructions: From config file.
    speed: 0.91
    response_format: wav
""".strip()
            + "\n",
            encoding="utf-8",
        )
        self._write_customization(
            "config/customization.template.yaml",
            f"""
version: "1"
workflow:
  defaultProfilesFile: {profiles_path}
""",
        )

        args = m.parse_args(["--text", "hello", "--dry-run"])
        profiles = m.resolve_profile_set(args, m.load_runtime_config())
        assert profiles is not None
        self.assertEqual(profiles.default_profile, "from-config")

    def test_config_default_disclosure_used_when_profile_has_none(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  defaultDisclosure: "Configured disclosure."
""",
        )
        profiles = m.load_profiles(self._write_profiles())
        ns = type("NS", (), {"profile": "default-general", "voice": None, "instructions": None, "speed": None, "format": None, "model": None})
        _, _, _, disclosure = m.resolve_effective_config(ns, profiles, m.load_runtime_config())
        self.assertEqual(disclosure, "Configured disclosure.")

    def test_config_default_output_dir_changes_resolved_output_path(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  localCli:
    defaultOutputDir: configured/output
""",
        )
        args = m.parse_args(["--text", "hello", "--dry-run"])
        out = m.resolve_output_path(args, "mp3", m.load_runtime_config())
        self.assertEqual(out.parent, Path("configured/output"))

    def test_config_default_playback_backend_used_when_flag_omitted(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  localCli:
    defaultPlaybackBackend: afplay
""",
        )
        args = m.parse_args(["--text", "hello", "--dry-run"])
        config = m.load_runtime_config()
        effective_playback_backend = args.playback if args.playback is not None else config.local_playback_backend
        self.assertEqual(effective_playback_backend, "afplay")

    def test_config_autoplay_generated_audio_used_when_flag_unset(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  localCli:
    autoplayGeneratedAudio: true
""",
        )
        args = m.parse_args(["--text", "hello", "--dry-run"])
        config = m.load_runtime_config()
        queue = m.resolve_playback_queue(args, self.root / "out.mp3", config.local_autoplay_generated_audio)
        self.assertEqual(queue, [self.root / "out.mp3"])

    def test_invalid_customization_yaml_raises(self) -> None:
        self._set_cwd_root()
        self._write_customization("config/customization.template.yaml", "version: '1'\nworkflow: [\n")
        with self.assertRaises(m.WrapperError):
            m.load_runtime_config()

    def test_unsupported_customization_version_raises(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "2"
workflow: {}
""",
        )
        with self.assertRaises(m.WrapperError):
            m.load_runtime_config()

    def test_invalid_default_playback_backend_raises(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  localCli:
    defaultPlaybackBackend: bad
""",
        )
        with self.assertRaises(m.WrapperError):
            m.load_runtime_config()

    def test_non_boolean_autoplay_generated_audio_raises(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow:
  localCli:
    autoplayGeneratedAudio: "yes"
""",
        )
        with self.assertRaises(m.WrapperError):
            m.load_runtime_config()

    def test_customization_file_requires_yaml_support(self) -> None:
        self._set_cwd_root()
        self._write_customization(
            "config/customization.template.yaml",
            """
version: "1"
workflow: {}
""",
        )
        old_yaml = m.yaml
        m.yaml = None
        self.addCleanup(lambda: setattr(m, "yaml", old_yaml))
        with self.assertRaises(m.WrapperError):
            m.load_runtime_config()

    def test_manifest_written_contains_required_keys(self) -> None:
        out = self.root / "out" / "audio.mp3"
        payload = {
            "timestamp": "2026-02-28T00:00:00+00:00",
            "input_source": "inline",
            "profile_id": "default-general",
            "effective_voice": "cedar",
            "effective_instructions": "x",
            "effective_speed": 1.0,
            "summarize_mode": "none",
            "target_chars": None,
            "playback_backend": "none",
            "playback_result": "skipped",
            "backend_mode": "local-cli",
            "disclosure": m.DEFAULT_DISCLOSURE,
            "audio_output_path": str(out),
            "text_sha256": "abc",
        }
        manifest = m.write_manifest(out, payload)
        self.assertTrue(manifest.exists())
        parsed = json.loads(manifest.read_text(encoding="utf-8"))
        for key in m.REQUIRED_MANIFEST_KEYS:
            self.assertIn(key, parsed)

    def test_main_fails_on_missing_api_key(self) -> None:
        old = os.environ.pop("OPENAI_API_KEY", None)
        self.addCleanup(lambda: os.environ.__setitem__("OPENAI_API_KEY", old) if old else os.environ.pop("OPENAI_API_KEY", None))
        rc = m.main(["--text", "hello", "--dry-run"])
        self.assertEqual(rc, 2)

    def test_load_profiles_rejects_duplicate_ids(self) -> None:
        path = self.root / "dupe.yaml"
        path.write_text(
            """
version: "1"
profiles:
  - id: dup
    voice: cedar
    instructions: One
    speed: 1.0
    response_format: mp3
  - id: dup
    voice: ash
    instructions: Two
    speed: 1.1
    response_format: wav
""".strip()
            + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(m.WrapperError):
            m.load_profiles(path)

    def test_load_profiles_invalid_json_raises_wrapper_error(self) -> None:
        path = self.root / "bad.json"
        path.write_text("{ invalid", encoding="utf-8")
        with self.assertRaises(m.WrapperError):
            m.load_profiles(path)

    def test_load_profiles_invalid_yaml_raises_wrapper_error(self) -> None:
        path = self.root / "bad.yaml"
        path.write_text("version: '1'\nprofiles: [\n", encoding="utf-8")
        with self.assertRaises(m.WrapperError):
            m.load_profiles(path)

    def test_main_propagates_cli_failure_and_skips_manifest(self) -> None:
        fake_cli = self.root / "fake_tts_cli.py"
        fake_cli.write_text(
            "import sys\n"
            "raise SystemExit(7)\n",
            encoding="utf-8",
        )
        out = self.root / "failure.mp3"

        old = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-key"
        self.addCleanup(
            lambda: os.environ.__setitem__("OPENAI_API_KEY", old)
            if old is not None
            else os.environ.pop("OPENAI_API_KEY", None)
        )

        rc = m.main(
            [
                "--text",
                "hello",
                "--tts-cli-path",
                str(fake_cli),
                "--python-bin",
                sys.executable,
                "--out",
                str(out),
            ]
        )
        self.assertEqual(rc, 7)
        self.assertFalse(out.with_suffix(out.suffix + ".manifest.json").exists())

    def test_resolve_playback_queue_autoplay_and_queue_file(self) -> None:
        generated = self.root / "out.mp3"
        queue_file = self.root / "queue.txt"
        queue_file.write_text(f"{self.root / 'a.mp3'}\n#comment\n\n{self.root / 'b.wav'}\n", encoding="utf-8")
        ns = type("NS", (), {"autoplay": True, "queue_file": str(queue_file)})
        queue = m.resolve_playback_queue(ns, generated)
        self.assertEqual(queue, [generated, self.root / "a.mp3", self.root / "b.wav"])

    def test_execute_playback_stop_on_error_returns_deterministic_code(self) -> None:
        missing = self.root / "missing.mp3"
        summary = m.execute_playback(
            backend="afplay",
            queue=[missing],
            repeat=1,
            stop_on_error=True,
            dry_run=False,
        )
        self.assertEqual(summary.exit_code, 3)
        self.assertEqual(summary.result, "failed")
        self.assertEqual(summary.failed, 1)
        self.assertIn("File not found for playback", summary.errors[0])

    def test_execute_playback_continue_on_error_returns_partial(self) -> None:
        missing = self.root / "missing.mp3"
        existing = self.root / "ok.mp3"
        existing.write_text("x", encoding="utf-8")

        with mock.patch.object(m.subprocess, "run", return_value=None) as run_mock:
            summary = m.execute_playback(
                backend="afplay",
                queue=[missing, existing],
                repeat=1,
                stop_on_error=False,
                dry_run=False,
            )
        self.assertEqual(summary.exit_code, 3)
        self.assertEqual(summary.result, "partial")
        self.assertEqual(summary.succeeded, 1)
        self.assertEqual(summary.failed, 1)
        self.assertEqual(run_mock.call_count, 1)

    def test_main_dry_run_records_playback_metadata(self) -> None:
        old = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-key"
        self.addCleanup(
            lambda: os.environ.__setitem__("OPENAI_API_KEY", old)
            if old is not None
            else os.environ.pop("OPENAI_API_KEY", None)
        )

        out = self.root / "dry.mp3"
        rc = m.main(
            [
                "--text",
                "hello",
                "--out",
                str(out),
                "--dry-run",
                "--playback",
                "afplay",
                "--autoplay",
                "--repeat",
                "2",
                "--no-stop-on-error",
            ]
        )
        self.assertEqual(rc, 0)
        manifest = out.with_suffix(out.suffix + ".manifest.json")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(payload["playback_backend"], "afplay")
        self.assertEqual(payload["playback_result"], "dry_run")
        self.assertEqual(payload["playback_attempted"], 2)
        self.assertEqual(payload["playback_queue_size"], 1)
        self.assertFalse(payload["playback_stop_on_error"])
        self.assertEqual(payload["backend_mode"], "local-cli")
        self.assertEqual(payload["disclosure"], m.DEFAULT_DISCLOSURE)

    def test_main_playback_queue_failure_stop_on_error_sets_exit_3(self) -> None:
        old = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-key"
        self.addCleanup(
            lambda: os.environ.__setitem__("OPENAI_API_KEY", old)
            if old is not None
            else os.environ.pop("OPENAI_API_KEY", None)
        )

        fake_cli = self.root / "fake_tts_cli.py"
        fake_cli.write_text("print('ok')\n", encoding="utf-8")
        out = self.root / "audio.mp3"
        missing = self.root / "missing.mp3"
        queue_file = self.root / "queue.txt"
        queue_file.write_text(f"{missing}\n", encoding="utf-8")

        with mock.patch.object(m.subprocess, "run", return_value=None) as run_mock:
            rc = m.main(
                [
                    "--text",
                    "hello",
                    "--tts-cli-path",
                    str(fake_cli),
                    "--python-bin",
                    sys.executable,
                    "--out",
                    str(out),
                    "--playback",
                    "afplay",
                    "--queue-file",
                    str(queue_file),
                ]
            )
        self.assertEqual(rc, 3)
        self.assertEqual(run_mock.call_count, 1)

        manifest = out.with_suffix(out.suffix + ".manifest.json")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(payload["playback_backend"], "afplay")
        self.assertEqual(payload["playback_result"], "failed")
        self.assertEqual(payload["playback_attempted"], 1)
        self.assertEqual(payload["playback_failed"], 1)
        self.assertEqual(payload["playback_succeeded"], 0)
        self.assertEqual(payload["backend_mode"], "local-cli")
        self.assertEqual(payload["disclosure"], m.DEFAULT_DISCLOSURE)

    def test_main_playback_queue_partial_when_continue_on_error(self) -> None:
        old = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-key"
        self.addCleanup(
            lambda: os.environ.__setitem__("OPENAI_API_KEY", old)
            if old is not None
            else os.environ.pop("OPENAI_API_KEY", None)
        )

        fake_cli = self.root / "fake_tts_cli.py"
        fake_cli.write_text("print('ok')\n", encoding="utf-8")
        out = self.root / "audio.mp3"
        missing = self.root / "missing.mp3"
        existing = self.root / "queued-ok.mp3"
        existing.write_text("x", encoding="utf-8")
        queue_file = self.root / "queue.txt"
        queue_file.write_text(f"{missing}\n{existing}\n", encoding="utf-8")

        with mock.patch.object(m.subprocess, "run", return_value=None) as run_mock:
            rc = m.main(
                [
                    "--text",
                    "hello",
                    "--tts-cli-path",
                    str(fake_cli),
                    "--python-bin",
                    sys.executable,
                    "--out",
                    str(out),
                    "--playback",
                    "afplay",
                    "--queue-file",
                    str(queue_file),
                    "--no-stop-on-error",
                ]
            )
        self.assertEqual(rc, 3)
        self.assertEqual(run_mock.call_count, 2)

        manifest = out.with_suffix(out.suffix + ".manifest.json")
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(payload["playback_backend"], "afplay")
        self.assertEqual(payload["playback_result"], "partial")
        self.assertEqual(payload["playback_attempted"], 2)
        self.assertEqual(payload["playback_failed"], 1)
        self.assertEqual(payload["playback_succeeded"], 1)
        self.assertEqual(payload["backend_mode"], "local-cli")
        self.assertEqual(payload["disclosure"], m.DEFAULT_DISCLOSURE)
