#!/usr/bin/env python3
"""Compile an essay from a knots publish ref into an HTML page.

Usage:
    python build/compile_essay.py <publish-dir> <essay-id> [--version v1.0]

Reads manifest.json from a checked-out knots publish ref, prepends YAML
frontmatter to the essay markdown, and runs Pandoc with citeproc to produce
essays/<essay-id>/index.html.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Compile essay from knots publish ref"
    )
    parser.add_argument("publish_dir", type=Path,
                        help="Path to checked-out knots publish ref")
    parser.add_argument("essay_id", help="Essay directory name")
    parser.add_argument("--version", dest="version",
                        help="Version label (default: manifest name)")
    parser.add_argument("--output-dir", dest="output_dir", type=Path,
                        help="Override output base directory")
    args = parser.parse_args()

    publish_dir = args.publish_dir.resolve()
    manifest_path = publish_dir / "manifest.json"

    if not manifest_path.exists():
        print(f"Error: {manifest_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    # Find the main document (first with a title in frontmatter)
    doc = None
    for _key, d in manifest["documents"].items():
        if d.get("frontmatter", {}).get("title"):
            doc = d
            break
    if not doc:
        print("Error: no document with title found in manifest", file=sys.stderr)
        sys.exit(1)
    frontmatter = dict(doc["frontmatter"])

    # Resolve markdown source (prefer "md" format artifact, fall back to first)
    md_artifact = None
    history_artifact = None
    knots_md_artifact = None
    for art in doc["artifacts"]:
        if art.get("format") == "md":
            md_artifact = art["path"]
        elif art.get("format") == "history":
            history_artifact = art["path"]
        elif art.get("format") == "knots_md":
            knots_md_artifact = art["path"]
    if not md_artifact:
        md_artifact = doc["artifacts"][0]["path"]
    md_path = publish_dir / md_artifact
    if not md_path.exists():
        print(f"Error: {md_path} not found", file=sys.stderr)
        sys.exit(1)

    # Resolve bibliography to absolute path
    if "bibliography" in frontmatter:
        bib_rel = frontmatter["bibliography"]
        bib_path = publish_dir / bib_rel
        if not bib_path.exists():
            print(f"Error: bibliography {bib_path} not found", file=sys.stderr)
            sys.exit(1)
        frontmatter["bibliography"] = str(bib_path)

    # Set version from --version flag or manifest name
    version = args.version or manifest.get("name")
    if version:
        frontmatter["version"] = version

    # Remove csl from frontmatter — we pass it as a CLI arg
    frontmatter.pop("csl", None)

    # Strip @ prefixes from author-links (citeproc parses @ as citations)
    if "author-links" in frontmatter:
        frontmatter["author-links"] = {
            k: v.lstrip("@") for k, v in frontmatter["author-links"].items()
        }

    # Build YAML frontmatter block
    yaml_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, dict):
            yaml_lines.append(f"{key}:")
            for k, v in value.items():
                yaml_lines.append(f"  {k}: \"{_escape_yaml(str(v))}\"")
        elif isinstance(value, list):
            yaml_lines.append(f"{key}:")
            for item in value:
                yaml_lines.append(f"  - \"{_escape_yaml(str(item))}\"")
        elif isinstance(value, str):
            yaml_lines.append(f"{key}: \"{_escape_yaml(value)}\"")
        else:
            yaml_lines.append(f"{key}: {value}")
    yaml_lines.append("---")
    yaml_block = "\n".join(yaml_lines) + "\n\n"

    # Read essay markdown
    md_content = md_path.read_text()

    # Write temp file with frontmatter + markdown
    build_dir = Path(__file__).resolve().parent
    repo_root = build_dir.parent

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", dir=str(publish_dir), delete=False
    ) as tmp:
        tmp.write(yaml_block)
        tmp.write(md_content)
        tmp_path = Path(tmp.name)

    # Ensure output directory exists
    if args.output_dir:
        output_dir = args.output_dir / args.essay_id
    else:
        output_dir = repo_root / args.essay_id
    if version:
        output_dir = output_dir / version
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"

    # Resolve build asset paths
    defaults_path = build_dir / "essay-defaults.yaml"
    template_path = build_dir / "essay-template.html"
    csl_path = build_dir / "chicago-author-date.csl"

    try:
        # Compile HTML
        cmd = [
            "pandoc", str(tmp_path),
            "--defaults", str(defaults_path),
            "--template", str(template_path),
            "--csl", str(csl_path),
            "-o", str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Pandoc error:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)

        # Render citeproc-resolved markdown
        md_out = output_dir / "essay.md"
        md_cmd = [
            "pandoc", str(tmp_path),
            "--citeproc",
            "--csl", str(csl_path),
            "-t", "markdown",
            "--metadata", "reference-section-title=References",
            "-o", str(md_out),
        ]
        md_result = subprocess.run(md_cmd, capture_output=True, text=True)
        if md_result.returncode != 0:
            print(f"Markdown warning:\n{md_result.stderr}", file=sys.stderr)
        else:
            print(f"  md: {md_out}", file=sys.stderr)

        # Generate epub
        epub_out = output_dir / "essay.epub"
        epub_cmd = [
            "pandoc", str(tmp_path),
            "--citeproc",
            "--csl", str(csl_path),
            "-o", str(epub_out),
        ]
        epub_result = subprocess.run(epub_cmd, capture_output=True, text=True)
        if epub_result.returncode != 0:
            print(f"EPUB warning:\n{epub_result.stderr}", file=sys.stderr)
        else:
            print(f"  epub: {epub_out}", file=sys.stderr)

        # Copy history.json and viewer if available
        if history_artifact:
            history_src = publish_dir / history_artifact
            if history_src.exists():
                history_out = output_dir / "history.json"
                shutil.copy2(str(history_src), str(history_out))
                # Copy history viewer
                viewer_src = build_dir / "history-viewer.html"
                if viewer_src.exists():
                    viewer_dir = output_dir / "history"
                    viewer_dir.mkdir(exist_ok=True)
                    shutil.copy2(str(viewer_src), str(viewer_dir / "index.html"))
                print(f"  history: {history_out}", file=sys.stderr)

        # Copy .knots.md if available
        if knots_md_artifact:
            knots_src = publish_dir / knots_md_artifact
            if knots_src.exists():
                knots_out = output_dir / "essay.knots.md"
                shutil.copy2(str(knots_src), str(knots_out))
                print(f"  knots: {knots_out}", file=sys.stderr)

        # Copy diff viewer if we have knots data
        diff_viewer_src = build_dir / "diff-viewer.html"
        if diff_viewer_src.exists():
            diff_dir = output_dir / "diff"
            diff_dir.mkdir(exist_ok=True)
            shutil.copy2(str(diff_viewer_src), str(diff_dir / "index.html"))
    finally:
        tmp_path.unlink(missing_ok=True)

    print(output_path)


def _escape_yaml(s):
    """Escape characters that need quoting in YAML double-quoted strings."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    main()
