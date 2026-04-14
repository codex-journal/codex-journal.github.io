#!/usr/bin/env python3
"""Sync all versions of an essay from a knots lineage.

Usage:
    python build/sync_lineage.py <essay-id> <source-repo-url> <lineage>

Fetches refs/knots/publish-heads/<lineage> from the source repo, walks the
git log to enumerate publishes, compiles any new versions, updates the
registry, writes versions.json, and copies the latest version to the essay root.

Supports both V2 (per-publish commit refs with head tracking) and V0 (shared
tree) publish formats. Tries V2 first, falls back to V0.

Expects GIT_SSH_COMMAND to be set if the source repo requires SSH auth.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = PROJECT_ROOT / "_data" / "essays.json"


# ── V2 fetch: per-publish commit refs with head tracking ──

def fetch_publish_head(repo_url, git_dir, lineage):
    """Fetch refs/knots/publish-heads/<lineage>, return head SHA or None."""
    subprocess.run(["git", "init", str(git_dir)],
                   capture_output=True, check=True)
    subprocess.run(["git", "-C", str(git_dir), "remote", "add", "source", repo_url],
                   capture_output=True, check=True)
    result = subprocess.run(
        ["git", "-C", str(git_dir), "fetch", "source",
         f"refs/knots/publish-heads/{lineage}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None

    sha = subprocess.run(
        ["git", "-C", str(git_dir), "rev-parse", "FETCH_HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return sha


def list_versions_v2(git_dir, head_sha):
    """Walk git log from head to enumerate all publishes. Returns [(name, sha)]."""
    result = subprocess.run(
        ["git", "-C", str(git_dir), "log", "--format=%H", head_sha],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []

    versions = []
    for sha in result.stdout.strip().splitlines():
        manifest_raw = subprocess.run(
            ["git", "-C", str(git_dir), "show", f"{sha}:manifest.json"],
            capture_output=True, text=True,
        )
        if manifest_raw.returncode != 0:
            continue
        manifest = json.loads(manifest_raw.stdout)
        versions.append((manifest["name"], sha))

    versions.reverse()  # oldest first
    return versions


def extract_version_v2(git_dir, sha, dest_dir):
    """Extract all files from a publish commit to dest_dir."""
    archive = subprocess.run(
        ["git", "-C", str(git_dir), "archive", sha],
        capture_output=True,
    )
    if archive.returncode != 0:
        return False

    result = subprocess.run(
        ["tar", "-x", "-C", str(dest_dir)],
        input=archive.stdout, capture_output=True,
    )
    return result.returncode == 0


# ── V0 fallback: shared tree ──

def fetch_publish_tree(repo_url, git_dir):
    """Fetch refs/knots/publish (V0 tree), return tree SHA or None."""
    result = subprocess.run(
        ["git", "-C", str(git_dir), "fetch", "source", "refs/knots/publish"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None

    sha = subprocess.run(
        ["git", "-C", str(git_dir), "rev-parse", "FETCH_HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return sha


def list_versions_v0(git_dir, tree_sha, lineage):
    """List version names under a lineage in the V0 publish tree."""
    result = subprocess.run(
        ["git", "-C", str(git_dir), "ls-tree", tree_sha, f"{lineage}/"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []

    versions = []
    for line in result.stdout.strip().splitlines():
        _meta, path = line.split("\t", 1)
        version = path.rstrip("/").split("/")[-1]
        versions.append((version, None))  # no SHA for V0
    return versions


def extract_version_v0(git_dir, tree_sha, lineage, version, dest_dir):
    """Extract a version subtree from V0 tree to dest_dir."""
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


# ── Shared logic ──

def already_compiled(essay_id, version):
    """Check if a version directory already exists."""
    return (PROJECT_ROOT / essay_id / version / "index.html").exists()


def version_in_registry(essay_id, version):
    """Check if a version is already in the registry."""
    if not REGISTRY_PATH.exists():
        return False
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)
    for entry in registry.get("essays", []):
        if entry.get("id") == essay_id:
            return any(v.get("version") == version for v in entry.get("versions", []))
    return False


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
    """Copy the latest version's files to the essay root."""
    if not REGISTRY_PATH.exists():
        return

    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    for entry in registry.get("essays", []):
        if entry.get("id") == essay_id:
            current = entry.get("current_version", "")
            if not current:
                return
            version_dir = PROJECT_ROOT / essay_id / current
            for filename in ["index.html", "essay.md", "essay.epub", "history.json"]:
                src = version_dir / filename
                dst = PROJECT_ROOT / essay_id / filename
                if src.exists():
                    shutil.copy2(str(src), str(dst))
            print(f"  latest: {current} -> {PROJECT_ROOT / essay_id}/")
            return


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sync essay lineage")
    parser.add_argument("essay_id", help="Essay directory name")
    parser.add_argument("repo_url", help="Source repo URL")
    parser.add_argument("lineage", help="Knots lineage name")
    parser.add_argument("--force", action="store_true",
                        help="Force recompilation of all versions")
    args = parser.parse_args()

    essay_id = args.essay_id
    repo_url = args.repo_url
    lineage = args.lineage
    force = args.force

    print(f"Syncing {essay_id} from {lineage}")

    with tempfile.TemporaryDirectory() as git_dir:
        # Try V2 first (per-publish commit refs with head tracking)
        head_sha = fetch_publish_head(repo_url, git_dir, lineage)

        if head_sha:
            print(f"Using V2 publish refs (head: {head_sha[:12]})")
            versions = list_versions_v2(git_dir, head_sha)
            use_v2 = True
        else:
            # Fall back to V0 (shared tree)
            print("V2 head not found, falling back to V0 tree")
            tree_sha = fetch_publish_tree(repo_url, git_dir)
            if not tree_sha:
                print("Error: no publish refs found", file=sys.stderr)
                sys.exit(1)
            versions = list_versions_v0(git_dir, tree_sha, lineage)
            use_v2 = False

        if not versions:
            print("No versions found")
            return

        print(f"Found {len(versions)} version(s)")

        for version_name, version_sha in versions:
            compiled = already_compiled(essay_id, version_name)
            registered = version_in_registry(essay_id, version_name)

            if compiled and registered and not force:
                continue

            print(f"\n--- {version_name} ---")
            with tempfile.TemporaryDirectory() as dest:
                if use_v2:
                    ok = extract_version_v2(git_dir, version_sha, dest)
                else:
                    ok = extract_version_v0(git_dir, tree_sha, lineage, version_name, dest)

                if not ok:
                    print(f"  Error extracting {version_name}", file=sys.stderr)
                    continue
                if not compiled or force:
                    if not compile_version(dest, essay_id, version_name):
                        continue
                if not registered or force:
                    if not update_registry(dest, essay_id, version_name):
                        continue

    # Always rewrite versions.json and copy latest (handles reruns)
    write_versions_json(essay_id)
    copy_latest_to_root(essay_id)

    print(f"\nDone syncing {essay_id}")


if __name__ == "__main__":
    main()
