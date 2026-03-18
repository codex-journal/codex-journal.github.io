#!/usr/bin/env python3
"""Sync all versions of an essay from a knots lineage.

Usage:
    python build/sync_lineage.py <essay-id> <source-repo-url> <lineage>

Fetches refs/knots/publish (a tree object) from the source repo, walks
the tree to find {lineage}/{version}/ subtrees, compiles any new versions,
updates the registry, writes versions.json, and copies the latest version
to the essay root.

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


def fetch_publish_tree(repo_url, git_dir):
    """Fetch refs/knots/publish into git_dir, return tree SHA."""
    subprocess.run(["git", "init", str(git_dir)],
                   capture_output=True, check=True)
    subprocess.run(["git", "-C", str(git_dir), "remote", "add", "source", repo_url],
                   capture_output=True, check=True)
    result = subprocess.run(
        ["git", "-C", str(git_dir), "fetch", "source", "refs/knots/publish"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Error fetching publish tree:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    sha = subprocess.run(
        ["git", "-C", str(git_dir), "rev-parse", "FETCH_HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return sha


def list_versions(git_dir, tree_sha, lineage):
    """List version names under a lineage in the publish tree."""
    result = subprocess.run(
        ["git", "-C", str(git_dir), "ls-tree", tree_sha, f"{lineage}/"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []

    versions = []
    for line in result.stdout.strip().splitlines():
        # format: <mode> <type> <sha>\t<path>
        _meta, path = line.split("\t", 1)
        version = path.rstrip("/").split("/")[-1]
        versions.append(version)
    return versions


def extract_version(git_dir, tree_sha, lineage, version, dest_dir):
    """Extract a version subtree to dest_dir."""
    prefix = f"{lineage}/{version}/"
    archive = subprocess.run(
        ["git", "-C", str(git_dir), "archive", tree_sha, "--", prefix],
        capture_output=True,
    )
    if archive.returncode != 0:
        return False

    strip = prefix.count("/")
    result = subprocess.run(
        ["tar", "-x", "-C", str(dest_dir), f"--strip-components={strip}"],
        input=archive.stdout, capture_output=True,
    )
    return result.returncode == 0


def already_compiled(essay_id, version):
    """Check if a version directory already exists."""
    return (PROJECT_ROOT / essay_id / version / "index.html").exists()


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
    """Write {id}/versions.json from registry data."""
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

    with tempfile.TemporaryDirectory() as git_dir:
        tree_sha = fetch_publish_tree(repo_url, git_dir)

        versions = list_versions(git_dir, tree_sha, lineage)
        if not versions:
            print("No versions found")
            return

        print(f"Found {len(versions)} version(s)")

        new_versions = [v for v in versions if not already_compiled(essay_id, v)]

        if not new_versions:
            print("All versions already compiled")
        else:
            print(f"Compiling {len(new_versions)} new version(s)")
            new_versions.sort()

            for version in new_versions:
                print(f"\n--- {version} ---")
                with tempfile.TemporaryDirectory() as dest:
                    if not extract_version(git_dir, tree_sha, lineage, version, dest):
                        print(f"  Error extracting {version}", file=sys.stderr)
                        continue
                    if not compile_version(dest, essay_id, version):
                        continue
                    if not update_registry(dest, essay_id, version):
                        continue

    # Always rewrite versions.json and copy latest (handles reruns)
    write_versions_json(essay_id)
    copy_latest_to_root(essay_id)

    print(f"\nDone syncing {essay_id}")


if __name__ == "__main__":
    main()
