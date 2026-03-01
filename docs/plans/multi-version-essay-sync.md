# Plan: Multi-Version Essay Sync (codex-7pf)

## Context

The single-shot publish workflow (codex-ykf) compiles one snapshot at a time. This reworks the pipeline to sync an entire knots lineage — compiling all versions, serving them at versioned URLs, and providing in-page version navigation via JavaScript (matching the existing `js/sidebars.js` pattern of runtime UI injection).

## Registry Schema Change

`_data/essays.json` gains a `versions` array per essay. Top-level fields stay for backward compat with `build_index.py`:

```json
{
  "essays": [{
    "id": "source_engineering_intellectual_production_after_history",
    "title": "...",
    "author": "...",
    "current_version": "v1.1",
    "published_date": "2026-02-28T14:00:00Z",
    "link": "/essays/source_engineering_intellectual_production_after_history/",
    "versions": [
      {"version": "v1.1", "published_at": "2026-02-28T14:00:00Z", "link": "/essays/.../v1.1/"},
      {"version": "v1.0", "published_at": "2026-02-15T10:00:00Z", "link": "/essays/.../v1.0/"}
    ]
  }]
}
```

Top-level `published_date` = `published_at` of latest version (not frontmatter `date`).

## URL Structure

```
/essays/{id}/              → latest version (file copy)
/essays/{id}/v1.0/         → v1.0
/essays/{id}/v1.1/         → v1.1 (also latest)
/essays/{id}/versions.json → version list for JS nav
```

## Files to Change

### 1. `build/compile_essay.py` — versioned output path

When `--version` is provided, output to `essays/{id}/{version}/index.html` instead of `essays/{id}/index.html`. Currently lines 100-102:

```python
output_dir = repo_root / "essays" / args.essay_id
```

Becomes:

```python
output_dir = repo_root / "essays" / args.essay_id
if version:
    output_dir = output_dir / version
```

### 2. `build/update_registry.py` — multi-version writes

- Read `published_at` from manifest
- Match entry by `id` (not `link`)
- Append to `versions` array (skip if version already exists — immutable)
- Sort versions by `published_at` desc
- Recompute top-level fields from latest version

### 3. `build/sync_lineage.py` — **new** orchestrator

```
Usage: python build/sync_lineage.py <essay-id> <source-repo-url> <lineage>
```

Steps:
1. `git ls-remote` to enumerate `refs/knots/publish/{lineage}/*`
2. Check which versions already compiled (filesystem check)
3. For each new version: fetch ref to temp dir, call compile_essay.py, call update_registry.py
4. Write `essays/{id}/versions.json` from registry data
5. Copy latest version's `index.html` to essay root

Expects `GIT_SSH_COMMAND` already set (workflow handles SSH setup).

### 4. `build/essay-template.html` + `css/essay.css` — version nav

Add `<nav id="essay-versions">` placeholder in essay header. Add `<script>` before `</body>` that:
- Fetches `versions.json` relative to essay root
- Renders version links if 2+ versions exist
- Highlights current version
- Does nothing for single-version essays

CSS: minimal styles matching site aesthetic (IBM Plex Mono, dotted underlines).

### 5. `build/build_index.py` — format ISO dates

In `render_essay_entries()`, truncate ISO timestamps to date:
```python
if "T" in date:
    date = date.split("T")[0]
```

### 6. `.github/workflows/publish-essay.yml` — use sync_lineage

- Remove `snapshot_name` input
- Replace compile+update steps with single `sync_lineage.py` call
- Keep SSH setup, Pandoc install, commit+push steps

## Implementation Order

1. `compile_essay.py` — versioned output path
2. `update_registry.py` — multi-version registry logic
3. `sync_lineage.py` — new orchestrator
4. `essay-template.html` + `css/essay.css` — version nav UI
5. `build_index.py` — date formatting
6. `publish-essay.yml` — workflow switch

## Verify

```bash
# Test versioned compile
python build/compile_essay.py /tmp/publish-test/ test_essay --version v1.0
ls essays/test_essay/v1.0/index.html

# Test multi-version registry
python build/update_registry.py /tmp/publish-test/ test_essay
cat _data/essays.json  # should have versions array

# Test idempotency
python build/update_registry.py /tmp/publish-test/ test_essay
# "already registered, skipping"

# Check version nav in browser
python3 -m http.server 8787
# Browse /essays/test_essay/ and /essays/test_essay/v1.0/

# Clean up
git checkout _data/essays.json
rm -rf essays/test_essay/
```
