#!/usr/bin/env python3
"""Update _data/essays.json with metadata from a knots publish ref.

Usage:
    python build/update_registry.py <publish-dir> <essay-id> [--version v1.0]

Reads manifest.json from a checked-out knots publish ref, extracts frontmatter,
and writes/updates the essay entry in the registry.
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

    doc = manifest["documents"]["writing/essay"]
    fm = doc["frontmatter"]

    title = fm.get("title", "")
    author_raw = fm.get("author", "")
    if isinstance(author_raw, list):
        author = ", ".join(str(a) for a in author_raw)
    else:
        author = str(author_raw)
    date = fm.get("date", "")
    version = args.version or manifest.get("name", "")

    link = f"/essays/{args.essay_id}/"

    # Load registry
    registry_path = args.registry
    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)
    else:
        registry = {"essays": []}

    essays = registry.get("essays", [])

    # Find existing entry by link
    existing = None
    for entry in essays:
        if entry.get("link") == link:
            existing = entry
            break

    if existing:
        changes = []
        for field, value in [("title", title), ("author", author),
                             ("current_version", version),
                             ("published_date", date)]:
            if value and existing.get(field) != value:
                changes.append(f"  {field}: {existing.get(field)!r} -> {value!r}")
                existing[field] = value
        if changes:
            print(f"Updated {args.essay_id}:")
            for c in changes:
                print(c)
        else:
            print(f"No changes for {args.essay_id}")
    else:
        new_entry = {
            "id": args.essay_id,
            "title": title,
            "author": author,
            "current_version": version,
            "published_date": date,
            "link": link,
        }
        essays.append(new_entry)
        print(f"Added new entry: {args.essay_id}")

    registry["essays"] = essays
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
