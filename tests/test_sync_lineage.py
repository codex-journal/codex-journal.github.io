"""Tests for build/sync_lineage.py parsing and logic."""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "build"))
from sync_lineage import list_versions_v0, list_versions_v2, already_compiled, version_in_registry


class TestListVersionsV0:
    def test_parses_tree_entries(self, tmp_path):
        """list_versions_v0 parses git ls-tree output for lineage subtrees."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "040000 tree abc123\texocap_index/1.0\n"
            "040000 tree def456\texocap_index/1.1\n"
        )
        with patch("sync_lineage.subprocess.run", return_value=mock_result):
            versions = list_versions_v0("/tmp/git", "fake_sha", "exocap_index")
        assert versions == [("1.0", None), ("1.1", None)]

    def test_empty_output(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        with patch("sync_lineage.subprocess.run", return_value=mock_result):
            versions = list_versions_v0("/tmp/git", "fake_sha", "exocap_index")
        assert versions == []


class TestListVersionsV2:
    def test_parses_git_log_with_manifests(self, tmp_path):
        """list_versions_v2 walks git log and reads manifest.json from each commit."""
        log_result = MagicMock()
        log_result.returncode = 0
        log_result.stdout = "sha_newer\nsha_older\n"

        manifest_older = MagicMock()
        manifest_older.returncode = 0
        manifest_older.stdout = json.dumps({"name": "1.0"})

        manifest_newer = MagicMock()
        manifest_newer.returncode = 0
        manifest_newer.stdout = json.dumps({"name": "1.1"})

        def mock_run(cmd, **kwargs):
            if "log" in cmd:
                return log_result
            if "sha_older:manifest.json" in cmd[-1]:
                return manifest_older
            if "sha_newer:manifest.json" in cmd[-1]:
                return manifest_newer
            return MagicMock(returncode=1, stdout="")

        with patch("sync_lineage.subprocess.run", side_effect=mock_run):
            versions = list_versions_v2("/tmp/git", "sha_newer")

        assert versions == [("1.0", "sha_older"), ("1.1", "sha_newer")]


class TestAlreadyCompiled:
    def test_returns_true_when_exists(self, tmp_path):
        essay_dir = tmp_path / "test_essay" / "v1.0"
        essay_dir.mkdir(parents=True)
        (essay_dir / "index.html").write_text("<html></html>")
        with patch("sync_lineage.PROJECT_ROOT", tmp_path):
            assert already_compiled("test_essay", "v1.0") is True

    def test_returns_false_when_missing(self, tmp_path):
        with patch("sync_lineage.PROJECT_ROOT", tmp_path):
            assert already_compiled("test_essay", "v1.0") is False
