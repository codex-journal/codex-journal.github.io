"""Tests for build/build_index.py date formatting."""

import sys
from pathlib import Path

# Import render_essay_entries directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "build"))
from build_index import render_essay_entries


class TestDateFormatting:
    def test_iso_timestamp_truncated_to_date(self):
        essays = [{"title": "T", "link": "/x/", "author": "A",
                    "current_version": "v1", "published_date": "2026-02-28T14:00:00Z"}]
        html = render_essay_entries(essays)
        assert "2026-02-28" in html
        assert "T14:00:00Z" not in html

    def test_plain_date_preserved(self):
        essays = [{"title": "T", "link": "/x/", "author": "A",
                    "current_version": "v1", "published_date": "2026-02-28"}]
        html = render_essay_entries(essays)
        assert "2026-02-28" in html

    def test_empty_date_no_error(self):
        essays = [{"title": "T", "link": "/x/", "author": "A",
                    "current_version": "v1", "published_date": ""}]
        html = render_essay_entries(essays)
        assert "T" in html  # title renders

    def test_year_only_preserved(self):
        essays = [{"title": "T", "link": "/x/", "author": "A",
                    "current_version": "v1", "published_date": "2026"}]
        html = render_essay_entries(essays)
        assert "2026" in html
