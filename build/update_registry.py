#!/usr/bin/env python3
"""Update _data/essays.json with metadata from a knots publish ref.

Usage:
    python build/update_registry.py <publish-dir> <essay-id> [--version v1.0]

Reads manifest.json from a checked-out knots publish ref, extracts frontmatter,
and writes/updates the essay entry in the registry. Tracks all versions per essay.
"""

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = PROJECT_ROOT / "_data" / "essays.json"


def main():
    parser = argparse.ArgumentParser(
        description="Update essay registry from knots publish ref"
    )
    parser.add_argument("publish_dir", type=Path,
                        help="Path to checked-out knots publish ref")
    parser.add_argument("essay_id", help="Essay directory name")
    parser.add_argument("--version", dest="version",
                        help="Version label (default: manifest name)")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY,
                        help="Path to essays.json")
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
    fm = doc["frontmatter"]

    title = fm.get("title", "")
    author_raw = fm.get("author", "")
    if isinstance(author_raw, list):
        author = ", ".join(str(a) for a in author_raw)
    else:
        author = str(author_raw)
    version = args.version or manifest.get("name", "")
    published_at = fm.get("date", "") or manifest.get("published_at", "")

    link = f"/{args.essay_id}/"
    version_link = f"/{args.essay_id}/{version}/" if version else link

    # Load registry
    registry_path = args.registry
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = {"essays": []}

    essays = registry.get("essays", [])

    # Find existing entry by id
    existing = None
    for entry in essays:
        if entry.get("id") == args.essay_id:
            existing = entry
            break

    if existing:
        versions = existing.get("versions", [])

        # Check if this version already registered (immutable)
        for v in versions:
            if v.get("version") == version:
                print(f"{args.essay_id} {version} already registered, skipping")
                return

        # Append new version
        versions.append({
            "version": version,
            "published_at": published_at,
            "link": version_link,
        })

        # Sort by published_at descending
        versions.sort(key=lambda v: v.get("published_at", ""), reverse=True)
        existing["versions"] = versions

        # Recompute top-level fields from latest version
        latest = versions[0]
        existing["current_version"] = latest["version"]
        existing["published_date"] = latest["published_at"]
        existing["title"] = title
        existing["author"] = author

        print(f"Added {version} to {args.essay_id} ({len(versions)} versions)")
    else:
        version_entry = {
            "version": version,
            "published_at": published_at,
            "link": version_link,
        }
        new_entry = {
            "id": args.essay_id,
            "title": title,
            "author": author,
            "current_version": version,
            "published_date": published_at,
            "link": link,
            "versions": [version_entry],
        }
        essays.append(new_entry)
        print(f"Added new entry: {args.essay_id} {version}")

    registry["essays"] = essays
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
