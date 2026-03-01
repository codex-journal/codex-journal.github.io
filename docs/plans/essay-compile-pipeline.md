# Plan: Pandoc Template + Build Config + Compile Script (codex-um0)

## Context

The essay publishing pipeline compiles markdown from knots publish refs into full HTML essay pages. A knots publish ref contains a `manifest.json` with document metadata (frontmatter, artifact paths) plus the actual files (.md, .bib). This task creates the Pandoc template, defaults, and a compile script that reads the manifest and drives Pandoc.

Currently, `essays/.../index.html` was hand-built. This creates the tooling to generate it reproducibly from knots artifacts.

---

## Pipeline Architecture

```
knots publish ref (git ref: refs/knots/publish/{lineage}/{snapshot})
  ├── manifest.json          ← metadata: frontmatter, artifact paths
  ├── writing/essay.md       ← pre-processed markdown (sentence IDs done)
  └── bib/refs.bib           ← bibliography

    ↓  build/compile_essay.py reads manifest.json

    1. Extract frontmatter from manifest (title, author, date, bibliography, csl)
    2. Add version from manifest name or CLI override
    3. Prepend YAML frontmatter to essay.md → temp file
    4. Run pandoc with --defaults, --citeproc → essays/<id>/index.html

    ↓  (codex-ykf: GitHub Action calls compile_essay.py)
```

---

## Files Created

| File | Purpose |
|------|---------|
| `build/essay-template.html` | Pandoc HTML5 template (`--template`) |
| `build/essay-defaults.yaml` | Pandoc defaults file (`--defaults`) |
| `build/chicago-author-date.csl` | CSL citation style (downloaded) |
| `build/compile_essay.py` | Reads knots manifest, prepends frontmatter, runs Pandoc |

---

## Usage

```bash
python build/compile_essay.py <publish-dir> <essay-id> [--version v1.0]
```

**Arguments:**
- `<publish-dir>` — path to checked-out knots publish ref (contains `manifest.json`)
- `<essay-id>` — e.g. `source_engineering_intellectual_production_after_history`
- `--version` — override version label (default: manifest `name` field)

## What this unblocks

- `codex-ykf` (GitHub Action) — calls `compile_essay.py` as a step
- `codex-ncm` (registry updater) — runs after compile to stamp version/date into essays.json
