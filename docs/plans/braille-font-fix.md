# Fix: Cross-Browser Braille Rendering

## Problem

The site uses braille unicode characters (U+2800-U+28FF) for decorative art: the masthead background behind the CODEX logo, the CAPTCHA sidebars, and bottom-art on essay pages. The CSS specifies `font-family: 'IBM Plex Mono', monospace` for these elements, and IBM Plex Mono is loaded from Google Fonts.

**IBM Plex Mono has no braille glyphs.** So every browser must fall back to a system font for those characters. Chromium and Firefox pick different fallback fonts, producing drastically different visual results.

## Root Cause

A visual comparison of every braille-capable font on the system:

| Font | Braille rendering |
|------|------------------|
| Adwaita Mono | Sparse tiny dots (matches Chromium's look) |
| DejaVu Sans/Serif | Sparse tiny dots |
| Noto Sans/Mono | Sparse tiny dots |
| **FreeMono** | **Dense filled blocks (Firefox's fallback)** |
| Unifont | Invisible/blank |

Chromium's fallback chain picks a sparse-dot font (likely Adwaita Mono or DejaVu Sans). Firefox picks **FreeMono**, which renders every braille character — including U+2800 (braille blank) — as a dense blocky glyph. This turns the sidebars into a solid wall instead of the intended delicate dot art.

## Fix

**File:** `fonts/braille-mono.woff2` (1.2KB)

A subset of Adwaita Mono containing only U+2800-U+28FF (the braille range), generated with:

```bash
nix-shell -p "python3.withPackages(ps: [ps.fonttools ps.brotli])" --run \
  "pyftsubset /path/to/AdwaitaMono-Regular.ttf \
    --output-file=fonts/braille-mono.woff2 \
    --flavor=woff2 \
    --unicodes=U+2800-28FF \
    --no-hinting --desubroutinize"
```

**CSS** (in `site.css`, after the Google Fonts `@import`):

```css
@font-face {
    font-family: 'IBM Plex Mono';
    src: url('/fonts/braille-mono.woff2') format('woff2');
    unicode-range: U+2800-28FF;
    font-display: block;
}
```

This extends the `IBM Plex Mono` font family with braille glyphs via `unicode-range`. The browser treats it as if IBM Plex Mono natively supports braille — no fallback occurs, no font stack changes needed anywhere in the codebase.

## Why Adwaita Mono

- Monospace (consistent character widths with IBM Plex Mono)
- Braille glyphs render as sparse tiny dots, matching the intended aesthetic
- Same advance width (600/1000 UPM) as other monospace braille fonts
- Permissive license (GNOME/Adwaita, SIL Open Font License)

## Failed Approaches

1. **FreeMono subset** — Renders braille as dense blocks, completely wrong visual style
2. **DejaVu Sans subset** — Proportional font, braille glyphs too dense/blocky at small sizes
3. **Separate font-family name (`'Braille'`)** — Required modifying every font-family declaration; broke Chromium when FreeMono was the source
4. **`mix-blend-mode: multiply`** (unrelated but concurrent fix) — Unreliable on mobile browsers for bottom-art images; replaced with `filter: contrast(0.8)`
