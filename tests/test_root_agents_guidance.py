from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_live_docs_agree_that_speak_swiftly_has_no_local_mirror() -> None:
    contributing = (ROOT / "CONTRIBUTING.md").read_text()
    roadmap = (ROOT / "ROADMAP.md").read_text()
    subtree_workflow = (
        ROOT / "docs" / "maintainers" / "subtree-workflow.md"
    ).read_text()

    assert "does not keep a local `plugins/SpeakSwiftlyServer` mirror" in contributing
    assert "retiring the local `plugins/SpeakSwiftlyServer/` mirror" in roadmap
    assert "no longer imports the standalone source tree" in subtree_workflow
    assert not (ROOT / "plugins" / "SpeakSwiftlyServer").exists()
