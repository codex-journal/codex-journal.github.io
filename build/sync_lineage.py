#!/usr/bin/env python3
"""Sync all versions of an essay from a knots lineage.

Usage:
    python build/sync_lineage.py <essay-id> <source-repo-url> <lineage>

Enumerates all refs/knots/publish/{lineage}/* snapshots via git ls-remote,
compiles any new versions, updates the registry, writes versions.json,
and copies the latest version to the essay root.

Expects GIT_SSH_COMMAND to be set if the source repo requires SSH auth.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = PROJECT_ROOT / "_data" / "essays.json"


def ls_remote_versions(repo_url, lineage):
    """List all snapshot names under refs/knots/publish/{lineage}/."""
    prefix = f"refs/knots/publish/{lineage}/"
    result = subprocess.run(
        ["git", "ls-remote", repo_url, f"{prefix}*"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error: git ls-remote failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    versions = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        _sha, ref = line.split(None, 1)
        name = ref.removeprefix(prefix)
        if name:
            versions.append((name, ref))
    return versions


def already_compiled(essay_id, version):
    """Check if a version directory already exists."""
    return (PROJECT_ROOT / essay_id / version / "index.html").exists()


def fetch_ref(repo_url, ref, dest_dir):
    """Fetch a single ref into dest_dir."""
    subprocess.run(["git", "init", str(dest_dir)],
                   capture_output=True, check=True)
    subprocess.run(["git", "-C", str(dest_dir), "remote", "add", "source", repo_url],
                   capture_output=True, check=True)
    result = subprocess.run(
        ["git", "-C", str(dest_dir), "fetch", "--depth=1", "source", ref],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error fetching {ref}:\n{result.stderr}", file=sys.stderr)
        return False
    subprocess.run(["git", "-C", str(dest_dir), "checkout", "FETCH_HEAD"],
                   capture_output=True, check=True)
    return True


def read_published_at(publish_dir):
    """Read published_at from manifest.json for sorting."""
    manifest_path = Path(publish_dir) / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f).get("published_at", "")
    return ""


def compile_version(publish_dir, essay_id, version):
    """Run compile_essay.py for one version."""
    cmd = [
        sys.executable, str(BUILD_DIR / "compile_essay.py"),
        str(publish_dir), essay_id, "--version", version,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error compiling {version}:\n{result.stderr}", file=sys.stderr)
        return False
    print(f"  compiled {version}: {result.stdout.strip()}")
    return True


def update_registry(publish_dir, essay_id, version):
    """Run update_registry.py for one version."""
    cmd = [
        sys.executable, str(BUILD_DIR / "update_registry.py"),
        str(publish_dir), essay_id, "--version", version,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error updating registry for {version}:\n{result.stderr}",
              file=sys.stderr)
        return False
    print(f"  registry: {result.stdout.strip()}")
    return True


def write_versions_json(essay_id):
    """Write essays/{id}/versions.json from registry data."""
    if not REGISTRY_PATH.exists():
        return

    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    for entry in registry.get("essays", []):
        if entry.get("id") == essay_id:
            versions = entry.get("versions", [])
            out_path = PROJECT_ROOT / essay_id / "versions.json"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as f:
                json.dump({"versions": versions}, f, indent=2)
                f.write("\n")
            print(f"  wrote {out_path}")
            return

    print(f"Warning: {essay_id} not found in registry", file=sys.stderr)


def copy_latest_to_root(essay_id):
    """Copy the latest version's index.html to the essay root."""
    if not REGISTRY_PATH.exists():
        return

    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    for entry in registry.get("essays", []):
        if entry.get("id") == essay_id:
            current = entry.get("current_version", "")
            if not current:
                return
            src = PROJECT_ROOT / essay_id / current / "index.html"
            dst = PROJECT_ROOT / essay_id / "index.html"
            if src.exists():
                shutil.copy2(str(src), str(dst))
                print(f"  latest: {current} -> {dst}")
            return


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <essay-id> <source-repo-url> <lineage>",
              file=sys.stderr)
        sys.exit(1)

    essay_id = sys.argv[1]
    repo_url = sys.argv[2]
    lineage = sys.argv[3]

    print(f"Syncing {essay_id} from {lineage}")

    # Enumerate remote versions
    remote_versions = ls_remote_versions(repo_url, lineage)
    if not remote_versions:
        print("No publish refs found")
        return

    print(f"Found {len(remote_versions)} remote version(s)")

    # Filter to new versions
    new_versions = [
        (name, ref) for name, ref in remote_versions
        if not already_compiled(essay_id, name)
    ]

    if not new_versions:
        print("All versions already compiled")
    else:
        print(f"Compiling {len(new_versions)} new version(s)")

        # Sort by version name for deterministic order
        new_versions.sort(key=lambda x: x[0])

        for name, ref in new_versions:
            print(f"\n--- {name} ---")
            with tempfile.TemporaryDirectory() as tmp:
                if not fetch_ref(repo_url, ref, tmp):
                    continue
                if not compile_version(tmp, essay_id, name):
                    continue
                if not update_registry(tmp, essay_id, name):
                    continue

    # Always rewrite versions.json and copy latest (handles reruns)
    write_versions_json(essay_id)
    copy_latest_to_root(essay_id)

    print(f"\nDone syncing {essay_id}")


if __name__ == "__main__":
    main()
