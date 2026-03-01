# Plan: Essay Registry Updater (codex-ncm)

## Context

The essay publishing pipeline needs a script to stamp metadata into `_data/essays.json` after `compile_essay.py` produces HTML. The registry and index generator already exist:

- `_data/essays.json` — has one placeholder entry (`[Title]`, `[Author]`, `v0.0`)
- `build/build_index.py` — reads essays.json, renders `{{ESSAY_ENTRIES}}` on index.html + essays.html

The missing piece is `build/update_registry.py` — called by the GitHub Action after compile to write real metadata into the registry.

## File to create

### `build/update_registry.py`

```
Usage: python build/update_registry.py <publish-dir> <essay-id> [--version v1.0]
```

Same CLI signature as `compile_essay.py` so the Action can call them back-to-back with the same args.

**Steps:**
1. Read `manifest.json` from publish-dir
2. Extract frontmatter (title, author, date) from `documents["writing/essay"]`
3. Read `_data/essays.json`
4. Find existing entry by link `/essays/<essay-id>/`, or create new entry
5. Update fields: title, author, current_version, published_date
6. Write back `_data/essays.json` (pretty-printed, 2-space indent)
7. Print what changed (new vs updated, which fields)

**Field mapping:**

| Manifest frontmatter | essays.json field |
|----------------------|-------------------|
| `title` | `title` |
| `author` (join if list) | `author` |
| `date` | `published_date` |
| --version / manifest `name` | `current_version` |
| `<essay-id>` arg | `link` → `/essays/<essay-id>/` |

For `author`: if it's a list, join with ", " for the registry (the registry stores a single string; the Pandoc template handles list iteration separately).

**New entry** gets `id` set to `<essay-id>` and is appended to the essays array.

## No changes needed

- `build/build_index.py` — already works, reads the same format
- `_data/essays.json` — same schema, just gets real values
- Templates — no changes

## Verify

```bash
# Test with the mock publish dir from earlier
python build/update_registry.py /tmp/publish-test/ test_essay --version v1.0
cat _data/essays.json

# Rebuild index to confirm
python build/build_index.py --no-feed
# Check http://localhost:8787/ for updated listing

# Revert test data
git checkout _data/essays.json
```
