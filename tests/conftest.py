"""Shared fixtures for essay pipeline tests."""

import json
import shutil
from pathlib import Path

import pytest


@pytest.fixture
def tmp_publish_dir(tmp_path):
    """Create a mock publish directory with manifest and essay markdown."""

    def _make(version="v1.0", published_at="2026-02-15T10:00:00Z",
              title="Test Essay", author="Test Author", date="2026-02-15",
              author_links=None):
        d = tmp_path / version
        d.mkdir()
        frontmatter = {
            "title": title,
            "author": [author],
            "date": date,
        }
        if author_links:
            frontmatter["author-links"] = author_links
        manifest = {
            "name": version,
            "published_at": published_at,
            "documents": {
                "writing/essay": {
                    "frontmatter": frontmatter,
                    "artifacts": [{"path": "essay.md"}],
                }
            },
        }
        (d / "manifest.json").write_text(json.dumps(manifest))
        (d / "essay.md").write_text("Test paragraph.\n\n## Section\n\nContent.\n")
        return d

    return _make


@pytest.fixture
def registry_path(tmp_path):
    """Path to a temporary essays.json registry."""
    p = tmp_path / "essays.json"
    p.write_text('{"essays": []}\n')
    return p


@pytest.fixture
def project_root():
    """The real project root."""
    return Path(__file__).resolve().parent.parent
