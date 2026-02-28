# Plan: Create Essays Page + Add Nav Link Site-Wide

## Context

Bead `codex-jpl`. Essay pages only have "Glossary" in nav. The site needs a dedicated Essays listing page (`/essays.html`) and an "Essays" nav link on **every** page. Currently essays are listed on the index page but there's no standalone essays page.

---

## Files to Modify/Create

| File | Action |
|------|--------|
| `build/essays-template.html` | **Create** — template for essays page |
| `build/build_index.py` | **Modify** — generate essays.html from template |
| `build/index-template.html` | **Modify** — add Essays nav link |
| `build/feeds-template.html` | **Modify** — add Essays nav link |
| `glossary.html` | **Modify** — add Essays nav link |
| `archive.html` | **Modify** — add Essays nav link |
| `essays/.../index.html` | **Modify** — full nav (Essays, Glossary, Feeds, Archive) |

---

## 1. Create `build/essays-template.html`

Follow `feeds-template.html` pattern. Standard head, full nav, `<h1>Essays</h1>`, `{{ESSAY_ENTRIES}}` placeholder, footer, sidebars.js.

## 2. Update nav on all pages

Nav becomes (Essays first, then alphabetical):
```html
<div class="nav-links">
    <a href="/essays.html">Essays</a>
    <a href="/glossary.html">Glossary</a>
    <a href="/feeds.html">Feeds</a>
    <a href="/archive.html">Archive</a>
</div>
```

Update in: `build/index-template.html`, `build/feeds-template.html`, `glossary.html`, `archive.html`, `essays/.../index.html`

## 3. Modify `build/build_index.py`

Add essays page generation to `main()`:
- Add `--essays-template` and `--essays-output` CLI args (defaults: `build/essays-template.html`, `essays.html`)
- After rendering index, also render essays.html by replacing `{{ESSAY_ENTRIES}}` in the essays template
- Reuses existing `render_essay_entries()` and `load_essays()`

## 4. Rebuild

Run `python3 build/build_index.py` to generate `index.html`, `feeds.html`, and `essays.html`

---

## Verification

- `essays.html` generated with correct essay listing from `_data/essays.json`
- All pages have identical nav: Essays | Glossary | Feeds | Archive
- Close bead `codex-jpl`
