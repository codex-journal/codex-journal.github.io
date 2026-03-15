"""Tests for build/sync_lineage.py parsing and logic."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "build"))
from sync_lineage import ls_remote_versions, already_compiled


class TestLsRemoteVersions:
    def test_parses_refs(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = (
            "abc123\trefs/knots/publish/main/v1.0\n"
            "def456\trefs/knots/publish/main/v1.1\n"
        )
        with patch("sync_lineage.subprocess.run", return_value=mock_result):
            versions = ls_remote_versions("git@example.com:repo.git", "main")
        assert len(versions) == 2
        assert versions[0] == ("v1.0", "refs/knots/publish/main/v1.0")
        assert versions[1] == ("v1.1", "refs/knots/publish/main/v1.1")

    def test_empty_output(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        with patch("sync_lineage.subprocess.run", return_value=mock_result):
            versions = ls_remote_versions("git@example.com:repo.git", "main")
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
