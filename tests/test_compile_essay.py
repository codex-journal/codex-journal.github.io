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

    def test_author_links_rendered(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0", author_links={"instagram": "codexjournal", "twitter": "testhandle"})
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", "v1.0", out)
        html = output_path.read_text()
        assert "instagram.com/codexjournal" in html
        assert "x.com/testhandle" in html

    def test_no_author_links_when_absent(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0")
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", "v1.0", out)
        html = output_path.read_text()
        assert "instagram.com" not in html
        assert "x.com" not in html

    def test_output_contains_version_nav_placeholder(self, tmp_publish_dir, tmp_path):
        d = tmp_publish_dir(version="v1.0")
        out = tmp_path / "out"
        output_path = compile(d, "test_essay", "v1.0", out)
        html = output_path.read_text()
        assert 'id="essay-versions"' in html
        assert "versions.js" in html


@needs_pandoc
class TestTableOfContents:
    def _make_sectioned_essay(self, tmp_path):
        """Create a publish dir with multiple top-level sections."""
        d = tmp_path / "pub"
        d.mkdir()
        manifest = {
            "name": "v1.0",
            "published_at": "2026-02-28T00:00:00Z",
            "documents": {
                "writing/essay": {
                    "frontmatter": {
                        "title": "Sectioned Essay",
                        "author": ["Author"],
                        "date": "2026-02-28",
                    },
                    "artifacts": [{"path": "essay.md"}],
                }
            },
        }
        (d / "manifest.json").write_text(__import__("json").dumps(manifest))
        (d / "essay.md").write_text(
            "Intro.\n\n# First\n\nContent.\n\n# Second\n\nMore.\n"
        )
        return d

    def test_toc_generated_with_sections(self, tmp_path):
        d = self._make_sectioned_essay(tmp_path)
        out = tmp_path / "out"
        output_path = compile(d, "toc_essay", "v1.0", out)
        html = output_path.read_text()
        assert 'id="essay-toc"' in html
        assert "First" in html
        assert "Second" in html
        assert 'class="toc-dropdown"' in html

    def test_no_toc_without_sections(self, tmp_publish_dir, tmp_path):
        """Default fixture has only ## headings which become H3, below toc-depth."""
        d = tmp_publish_dir(version="v1.0")
        out = tmp_path / "out"
        output_path = compile(d, "notoc_essay", "v1.0", out)
        html = output_path.read_text()
        assert 'id="essay-toc"' not in html
