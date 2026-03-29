"""Tests for build/update_registry.py."""

import json
import subprocess
import sys
from pathlib import Path

BUILD_DIR = Path(__file__).resolve().parent.parent / "build"


def run_update_registry(publish_dir, essay_id, version=None, registry=None):
    cmd = [sys.executable, str(BUILD_DIR / "update_registry.py"),
           str(publish_dir), essay_id]
    if version:
        cmd += ["--version", version]
    if registry:
        cmd += ["--registry", str(registry)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"update_registry failed: {result.stderr}"
    return result.stdout


def load_registry(path):
    return json.loads(path.read_text())


class TestNewEntry:
    def test_creates_entry_with_versions_array(self, tmp_publish_dir, registry_path):
        d = tmp_publish_dir(version="v1.0")
        run_update_registry(d, "test_essay", "v1.0", registry_path)
        reg = load_registry(registry_path)
        assert len(reg["essays"]) == 1
        entry = reg["essays"][0]
        assert entry["id"] == "test_essay"
        assert entry["current_version"] == "v1.0"
        assert entry["published_date"] == "2026-02-15"
        assert entry["link"] == "/test_essay/"
        assert len(entry["versions"]) == 1
        assert entry["versions"][0]["version"] == "v1.0"
        assert entry["versions"][0]["link"] == "/test_essay/v1.0/"

    def test_uses_manifest_name_as_default_version(self, tmp_publish_dir, registry_path):
        d = tmp_publish_dir(version="v2.0")
        run_update_registry(d, "test_essay", registry=registry_path)
        reg = load_registry(registry_path)
        assert reg["essays"][0]["current_version"] == "v2.0"


class TestMultiVersion:
    def test_appends_second_version(self, tmp_publish_dir, registry_path):
        d1 = tmp_publish_dir(version="v1.0", date="2026-02-15")
        d2 = tmp_publish_dir(version="v1.1", date="2026-02-28",
                             title="Revised Title")
        run_update_registry(d1, "test_essay", "v1.0", registry_path)
        run_update_registry(d2, "test_essay", "v1.1", registry_path)
        reg = load_registry(registry_path)
        entry = reg["essays"][0]
        assert len(entry["versions"]) == 2
        assert entry["current_version"] == "v1.1"
        assert entry["published_date"] == "2026-02-28"
        assert entry["title"] == "Revised Title"

    def test_versions_sorted_desc_by_published_at(self, tmp_publish_dir, registry_path):
        d1 = tmp_publish_dir(version="v1.0", date="2026-02-15")
        d2 = tmp_publish_dir(version="v1.1", date="2026-02-28")
        run_update_registry(d1, "test_essay", "v1.0", registry_path)
        run_update_registry(d2, "test_essay", "v1.1", registry_path)
        reg = load_registry(registry_path)
        versions = reg["essays"][0]["versions"]
        assert versions[0]["version"] == "v1.1"
        assert versions[1]["version"] == "v1.0"

    def test_top_level_fields_from_latest(self, tmp_publish_dir, registry_path):
        # Add v1.1 first (later date), then v1.0 (earlier date)
        d2 = tmp_publish_dir(version="v1.1", date="2026-02-28",
                             title="Latest Title", author="Latest Author")
        d1 = tmp_publish_dir(version="v1.0", date="2026-02-15",
                             title="Old Title", author="Old Author")
        run_update_registry(d2, "test_essay", "v1.1", registry_path)
        run_update_registry(d1, "test_essay", "v1.0", registry_path)
        reg = load_registry(registry_path)
        entry = reg["essays"][0]
        # Top-level should reflect latest (v1.1), not most recently added (v1.0)
        assert entry["current_version"] == "v1.1"
        assert entry["published_date"] == "2026-02-28"


class TestIdempotency:
    def test_skips_duplicate_version(self, tmp_publish_dir, registry_path):
        d = tmp_publish_dir(version="v1.0")
        run_update_registry(d, "test_essay", "v1.0", registry_path)
        output = run_update_registry(d, "test_essay", "v1.0", registry_path)
        assert "already registered" in output
        reg = load_registry(registry_path)
        assert len(reg["essays"][0]["versions"]) == 1


class TestMatchById:
    def test_matches_existing_entry_by_id(self, tmp_publish_dir, registry_path):
        # Pre-populate with an entry that has id but old link format
        registry_path.write_text(json.dumps({
            "essays": [{
                "id": "test_essay",
                "title": "Old",
                "author": "Old",
                "current_version": "v0.1",
                "published_date": "2026-01-01",
                "link": "/test_essay/",
            }]
        }))
        d = tmp_publish_dir(version="v1.0")
        run_update_registry(d, "test_essay", "v1.0", registry_path)
        reg = load_registry(registry_path)
        assert len(reg["essays"]) == 1  # updated, not duplicated
        assert reg["essays"][0]["versions"][0]["version"] == "v1.0"
