"""Tests for build/sync_lineage.py parsing and logic."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "build"))
from sync_lineage import list_versions, already_compiled


class TestListVersions:
    def test_parses_tree_entries(self, tmp_path):
        """list_versions parses git ls-tree output for lineage subtrees."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "040000 tree abc123\texocap_index/1.0\n"
            "040000 tree def456\texocap_index/1.1\n"
        )
        with patch("sync_lineage.subprocess.run", return_value=mock_result):
            versions = list_versions("/tmp/git", "fake_sha", "exocap_index")
        assert versions == ["1.0", "1.1"]

    def test_empty_output(self, tmp_path):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        with patch("sync_lineage.subprocess.run", return_value=mock_result):
            versions = list_versions("/tmp/git", "fake_sha", "exocap_index")
        assert versions == []


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
