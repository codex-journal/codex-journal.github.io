# Plan: build_index.py — Static Index Generator

**Beads:** `codex-ncm` (essay registry + index generator), `codex-k7y` (GitHub activity feed)

## Context

The Codex Journal index page is currently hand-edited HTML with placeholder essay entries (`[Title]`, `[Author]`). We want a Python script that generates `index.html` from two data sources: an essay registry (`_data/essays.json`) and the GitHub org Atom feed (`https://github.com/codex-journal.atom`). This makes the landing page a build artifact — rebuilt daily by a cron Action, or on-demand after an essay publish.

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `build/build_index.py` | Create — the generator script |
| `build/index-template.html` | Create — HTML template with `{{PLACEHOLDERS}}` |
| `_data/essays.json` | Create — essay registry |
| `css/site.css` | Modify — add `.activity-feed` / `.activity-entry` CSS |
| `index.html` | Overwritten by the script (generated output) |

---

## 1. Template (`build/index-template.html`)

Copy current `index.html` verbatim, replacing only two sections:

- The essay entry `<div>` blocks → `{{ESSAY_ENTRIES}}`
- Insert `{{ACTIVITY_SECTION}}` between `</section>` (essay listing) and `<footer>`

Everything else stays: masthead braille art, ASCII CODEX/JOURNAL, nav (keep Glossary link for now), footer with GitHub/IG links, `sidebars.js` script tag.

---

## 2. Essay Registry (`_data/essays.json`)

```json
{
  "essays": [
    {
      "id": "source_engineering_intellectual_production_after_history",
      "title": "Intellectual Production After History: Source Engineering and the Real Subsumption of Knowledge Work",
      "author": "[Author]",
      "current_version": "v0.0",
      "published_date": "2026",
      "link": "/essays/source_engineering_intellectual_production_after_history/"
    }
  ]
}
```

Script handles missing file or empty list gracefully — renders empty essay section.

---

## 3. Script (`build/build_index.py`)

Python stdlib only. Functions:

- `load_essays(path)` — reads `_data/essays.json`, returns list of dicts
- `fetch_activity_feed(url, max_items=10, timeout=10)` — fetches `https://github.com/codex-journal.atom`, parses with `xml.etree.ElementTree`, returns list of `{title, link, published}`
  - Filters out entries containing "beads-sync" or "bd sync" in title
  - On failure (no internet, timeout), returns `[]` with a stderr warning
- `render_essay_entries(essays)` — returns HTML using `.essay-entry` / `.essay-entry-title` / `.essay-entry-meta` classes, `&middot;`-separated meta (author, version, date)
- `render_activity_section(entries)` — returns the full `<section class="activity-feed">` block, or empty string if no entries
- `render_template(template, essay_html, activity_html)` — replaces `{{ESSAY_ENTRIES}}` and `{{ACTIVITY_SECTION}}`
- `write_output(html, path)` — writes only if content differs (avoids unnecessary git diffs)

CLI:
```
python build/build_index.py [--no-feed] [--feed-url URL] [--output PATH]
```

`--no-feed` for offline/local dev. All paths default relative to project root.

---

## 4. Activity Feed CSS (add to `site.css`)

New classes paralleling the existing `.essay-listing` / `.essay-entry` pattern:

```css
/* --- Activity Feed (Index Page) --- */

.activity-feed {
    padding: 1rem 0;
}

.activity-feed-label {
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 1.5rem;
}

.activity-entry {
    padding: 0.8rem 0;
    border-bottom: 1px dotted #ccc;
}

.activity-entry:first-of-type {
    border-top: 1px dotted #ccc;
}

.activity-entry-title {
    font-size: 13px;
    line-height: 1.5;
    margin: 0 0 0.2rem 0;
}

.activity-entry-title a {
    color: #111;
}

.activity-entry-title a:hover {
    color: #7d9bca;
}

.activity-entry-meta {
    font-size: 11px;
    color: #888;
    letter-spacing: 0.02em;
}
```

---

## 5. Implementation Order

1. Create `_data/essays.json`
2. Create `build/index-template.html` from current `index.html`
3. Write `build/build_index.py`
4. Add activity feed CSS to `css/site.css`
5. Test: `python build/build_index.py --no-feed` — diff output against current `index.html`, should match essay section
6. Test: `python build/build_index.py` — verify activity section appears
7. Test: run twice, confirm idempotent

---

## Verification

- `python build/build_index.py --no-feed` produces `index.html` matching current essay listing
- `python build/build_index.py` adds activity section with recent GitHub org events, no beads-sync noise
- Running twice with no data changes produces no diff
- Open in browser on local dev server (port 8787), verify layout matches current site
- Screenshot with agent-browser to confirm visual appearance
