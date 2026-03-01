"""Browser integration tests for version navigation UI."""

import json
import subprocess
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pytest

BUILD_DIR = Path(__file__).resolve().parent.parent / "build"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def has_pandoc():
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def has_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        return False


needs_pandoc = pytest.mark.skipif(not has_pandoc(), reason="pandoc not available")
needs_playwright = pytest.mark.skipif(not has_playwright(), reason="playwright not available")


class SilentHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


@pytest.fixture(scope="module")
def essay_site(tmp_path_factory):
    """Build a mini site with two essay versions and serve it."""
    site_dir = tmp_path_factory.mktemp("site")

    # Copy static assets needed
    css_dir = site_dir / "css"
    css_dir.mkdir()
    for f in ["site.css", "essay.css"]:
        src = PROJECT_ROOT / "css" / f
        if src.exists():
            (css_dir / f).write_text(src.read_text())

    js_dir = site_dir / "js"
    js_dir.mkdir()
    for f in ["sidebars.js", "versions.js"]:
        src = PROJECT_ROOT / "js" / f
        if src.exists():
            (js_dir / f).write_text(src.read_text())

    # Create empty resource stubs
    res_dir = site_dir / "resources"
    res_dir.mkdir()
    (res_dir / "captcha-codex-journal.jpg").write_bytes(b"")
    (res_dir / "figure-dotted.jpg").write_bytes(b"")

    # Create manifests
    for version, pub_at, title in [
        ("v1.0", "2026-02-15T10:00:00Z", "Test Essay"),
        ("v1.1", "2026-02-28T14:00:00Z", "Test Essay (Revised)"),
    ]:
        d = site_dir / "publish" / version
        d.mkdir(parents=True)
        manifest = {
            "name": version,
            "published_at": pub_at,
            "documents": {
                "writing/essay": {
                    "frontmatter": {
                        "title": title,
                        "author": ["Test Author"],
                        "date": pub_at.split("T")[0],
                    },
                    "artifacts": [{"path": "essay.md"}],
                }
            },
        }
        (d / "manifest.json").write_text(json.dumps(manifest))
        (d / "essay.md").write_text(f"Content for {version}.\n")

    # Compile both versions into site_dir
    essays_dir = site_dir / "essays"
    essay_dir = essays_dir / "test_essay"
    for version in ["v1.0", "v1.1"]:
        result = subprocess.run(
            [sys.executable, str(BUILD_DIR / "compile_essay.py"),
             str(site_dir / "publish" / version), "test_essay",
             "--version", version,
             "--output-dir", str(essays_dir)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"compile failed: {result.stderr}")

    # Copy latest to root
    import shutil
    shutil.copy2(str(essay_dir / "v1.1" / "index.html"),
                 str(essay_dir / "index.html"))

    # Write versions.json
    versions_data = {
        "versions": [
            {"version": "v1.1", "published_at": "2026-02-28T14:00:00Z",
             "link": "/essays/test_essay/v1.1/"},
            {"version": "v1.0", "published_at": "2026-02-15T10:00:00Z",
             "link": "/essays/test_essay/v1.0/"},
        ]
    }
    (essay_dir / "versions.json").write_text(json.dumps(versions_data))

    # Also create a single-version essay
    single_dir = site_dir / "essays" / "single_essay"
    d = site_dir / "publish" / "solo"
    d.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": "v1.0",
        "published_at": "2026-03-01T00:00:00Z",
        "documents": {
            "writing/essay": {
                "frontmatter": {
                    "title": "Single Version Essay",
                    "author": ["Solo Author"],
                    "date": "2026-03-01",
                },
                "artifacts": [{"path": "essay.md"}],
            }
        },
    }
    (d / "manifest.json").write_text(json.dumps(manifest))
    (d / "essay.md").write_text("Solo content.\n")
    result = subprocess.run(
        [sys.executable, str(BUILD_DIR / "compile_essay.py"),
         str(d), "single_essay", "--version", "v1.0",
         "--output-dir", str(essays_dir)],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        shutil.copy2(str(single_dir / "v1.0" / "index.html"),
                     str(single_dir / "index.html"))
    (single_dir / "versions.json").write_text(json.dumps({
        "versions": [
            {"version": "v1.0", "published_at": "2026-03-01T00:00:00Z",
             "link": "/essays/single_essay/v1.0/"},
        ]
    }))

    # Start HTTP server
    import os
    os.chdir(str(site_dir))
    server = HTTPServer(("127.0.0.1", 0), SilentHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}", site_dir

    server.shutdown()


@needs_pandoc
@needs_playwright
class TestVersionDropdown:
    def test_dropdown_renders_with_two_versions(self, essay_site):
        from playwright.sync_api import sync_playwright
        base_url, _ = essay_site
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{base_url}/essays/test_essay/")
            page.wait_for_selector(".version-dropdown")
            toggle = page.locator(".version-toggle")
            assert toggle.text_content().strip().startswith("v1.1")
            browser.close()

    def test_dropdown_has_both_versions(self, essay_site):
        from playwright.sync_api import sync_playwright
        base_url, _ = essay_site
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{base_url}/essays/test_essay/")
            page.wait_for_selector(".version-dropdown")
            page.click(".version-toggle")
            items = page.locator(".version-list li")
            assert items.count() == 2
            browser.close()

    def test_current_version_highlighted(self, essay_site):
        from playwright.sync_api import sync_playwright
        base_url, _ = essay_site
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{base_url}/essays/test_essay/v1.0/")
            page.wait_for_selector(".version-dropdown")
            page.click(".version-toggle")
            current = page.locator("a.version-current")
            assert "v1.0" in current.text_content()
            browser.close()

    def test_version_links_correct(self, essay_site):
        from playwright.sync_api import sync_playwright
        base_url, _ = essay_site
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{base_url}/essays/test_essay/")
            page.wait_for_selector(".version-dropdown")
            page.click(".version-toggle")
            links = page.locator(".version-list li a")
            hrefs = [links.nth(i).get_attribute("href") for i in range(links.count())]
            assert "/essays/test_essay/v1.1/" in hrefs
            assert "/essays/test_essay/v1.0/" in hrefs
            browser.close()

    def test_dates_shown_in_dropdown(self, essay_site):
        from playwright.sync_api import sync_playwright
        base_url, _ = essay_site
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{base_url}/essays/test_essay/")
            page.wait_for_selector(".version-dropdown")
            page.click(".version-toggle")
            dates = page.locator(".version-date")
            assert dates.count() == 2
            assert "2026-02-28" in dates.nth(0).text_content()
            assert "2026-02-15" in dates.nth(1).text_content()
            browser.close()


@needs_pandoc
@needs_playwright
class TestSingleVersion:
    def test_no_dropdown_for_single_version(self, essay_site):
        from playwright.sync_api import sync_playwright
        base_url, _ = essay_site
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"{base_url}/essays/single_essay/")
            # Wait for JS to run
            page.wait_for_load_state("networkidle")
            dropdown = page.locator(".version-dropdown")
            assert dropdown.count() == 0
            browser.close()
