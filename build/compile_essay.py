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

    # Find the writing/essay document
    doc = manifest["documents"]["writing/essay"]
    frontmatter = dict(doc["frontmatter"])

    # Resolve markdown source
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

    # Build YAML frontmatter block
    yaml_lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, list):
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
        output_dir = repo_root / "essays" / args.essay_id
    if version:
        output_dir = output_dir / version
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"

    # Resolve build asset paths
    defaults_path = build_dir / "essay-defaults.yaml"
    template_path = build_dir / "essay-template.html"
    csl_path = build_dir / "chicago-author-date.csl"

    try:
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
    finally:
        tmp_path.unlink(missing_ok=True)

    print(output_path)


def _escape_yaml(s):
    """Escape characters that need quoting in YAML double-quoted strings."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    main()
