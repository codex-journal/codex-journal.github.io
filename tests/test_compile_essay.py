"""Tests for build/compile_essay.py versioned output paths."""

import subprocess
import sys
from pathlib import Path

import pytest

BUILD_DIR = Path(__file__).resolve().parent.parent / "build"


def has_pandoc():
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


needs_pandoc = pytest.mark.skipif(not has_pandoc(), reason="pandoc not available")


@needs_pandoc
class TestVersionedOutput:
    def test_version_flag_creates_versioned_dir(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0")
        result = subprocess.run(
            [sys.executable, str(BUILD_DIR / "compile_essay.py"),
             str(d), "test_essay", "--version", "v1.0"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"compile failed: {result.stderr}"
        output_path = Path(result.stdout.strip())
        assert "/test_essay/v1.0/index.html" in str(output_path)
        assert output_path.exists()

    def test_no_flag_uses_manifest_name(self, tmp_publish_dir):
        """Without --version, compile_essay uses manifest name as version."""
        d = tmp_publish_dir(version="v1.0")
        result = subprocess.run(
            [sys.executable, str(BUILD_DIR / "compile_essay.py"),
             str(d), "test_essay_noversion"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"compile failed: {result.stderr}"
        output_path = Path(result.stdout.strip())
        assert "/test_essay_noversion/v1.0/index.html" in str(output_path)

    def test_output_contains_title(self, tmp_publish_dir):
        d = tmp_publish_dir(version="v1.0", title="My Great Essay")
        result = subprocess.run(
            [sys.executable, str(BUILD_DIR / "compile_essay.py"),
             str(d), "test_essay_content", "--version", "v1.0"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        output_path = Path(result.stdout.strip())
        html = output_path.read_text()
        assert "My Great Essay" in html

    def test_output_contains_version_nav_placeholder(self, tmp_publish_dir):
        d = tmp_publish_dir(version="v1.0")
        result = subprocess.run(
            [sys.executable, str(BUILD_DIR / "compile_essay.py"),
             str(d), "test_essay_nav", "--version", "v1.0"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        html = Path(result.stdout.strip()).read_text()
        assert 'id="essay-versions"' in html
        assert "versions.js" in html
