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


def compile(publish_dir, essay_id, version=None, output_dir=None):
    cmd = [sys.executable, str(BUILD_DIR / "compile_essay.py"),
           str(publish_dir), essay_id]
    if version:
        cmd += ["--version", version]
    if output_dir:
        cmd += ["--output-dir", str(output_dir)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"compile failed: {result.stderr}"
    return Path(result.stdout.strip())


@needs_pandoc
class TestVersionedOutput:
    def test_version_flag_creates_versioned_dir(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0")
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", "v1.0", out)
        assert output_path == out / "test_essay" / "v1.0" / "index.html"
        assert output_path.exists()

    def test_no_flag_uses_manifest_name(self, tmp_publish_dir, tmp_path):
        """Without --version, compile_essay uses manifest name as version."""
        d = tmp_publish_dir(version="v1.0")
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", output_dir=out)
        assert output_path == out / "test_essay" / "v1.0" / "index.html"

    def test_output_contains_title(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0", title="My Great Essay")
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", "v1.0", out)
        html = output_path.read_text()
        assert "My Great Essay" in html

    def test_output_contains_version_nav_placeholder(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0")
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", "v1.0", out)
        html = output_path.read_text()
        assert 'id="essay-versions"' in html
        assert "versions.js" in html
