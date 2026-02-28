# Plan: Archive Page for Historical Essays

## Context

Bead `codex-ck6`. The site's early days had prefatory/historical works linked from the old index.html. These were removed during the site redesign. We want a dedicated archive page listing them as external links, with `cypherdude.jpeg` as bottom art.

---

## Archive Items (from git history)

1. **"decadence, extinction, whites: allegory"** — John Michael
   - Subtitle: *Allegories of Crisis, Crises of Allegory*
   - URL: `https://drive.google.com/file/d/1oJ_P0u8HilloPNk2SQTdrPs6ZcHLE62v/view?usp=share_link`
   - Google Drive PDF

2. **"Autologist Fragments"** — John Michael
   - URL: `https://docs.google.com/document/d/e/2PACX-1vTmNiCaQ5J0M0ZA2IOgiK6p0xVGyY835ZfVo9Ay1YgZguZdLJdowvzFqubw3HsK5SgR9qINE7l7jWcx/pub`
   - Published Google Doc

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `archive.html` | Create — static archive page |
| `glossary.html` | Modify — add Archive nav link |
| `build/index-template.html` | Modify — add Archive nav link |
| `build/feeds-template.html` | Modify — add Archive nav link |

---

## 1. Create `archive.html`

Static HTML (no build script). Follows `glossary.html` pattern:
- Standard head (charset, viewport, site.css, favicons, theme-color)
- Nav with all links: Glossary, Feeds, Archive
- `<h1>Archive</h1>`
- Listing using `.essay-entry` / `.essay-entry-title` / `.essay-entry-meta` classes (reuse existing styles)
- Both links open in new tab (`target="_blank"`)
- Bottom art: `<div class="bottom-art"><img src="/resources/cypherdude.jpeg" alt="" class="bottom-art-img"></div>`
- Standard footer + sidebars.js

## 2. Add Archive Nav Link

Add `<a href="/archive.html">Archive</a>` to `.nav-links` in:
- `glossary.html`
- `build/index-template.html`
- `build/feeds-template.html`

Then rebuild index + feeds: `python3 build/build_index.py`

---

## Verification

- Archive page loads with two essay entries and cypherdude bottom art
- Both links open correct external documents in new tabs
- All pages (index, glossary, feeds, archive) have Archive in nav
- `python3 build/build_index.py` regenerates index.html and feeds.html with updated nav
