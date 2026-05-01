# knots subdomain cutover plan (codex-qn5)

## Goal
Serve only the knots landing slice at `knots.cyphernetics.io` without changing the main `cyphernetics.io` Pages site.

## What is already done
- Landing page content is live at `https://cyphernetics.io/knots-project/` from `codex-journal.github.io`.
- A dedicated `gh-pages` branch was prepared in `codex-journal/knots` with:
  - `index.html` — standalone landing page
  - `CNAME` — `knots.cyphernetics.io`
- Current `gh-pages` branch tip in `codex-journal/knots`:
  - `449cb4f9e52a961e917ba49dac39d21645c786ac`

## Why this shape
Using the `knots` repo as the dedicated host avoids repointing the entire `cyphernetics.io` site. The apex site stays on `codex-journal.github.io`; the subdomain gets its own Pages host.

## Verified constraints
- `codex-journal.github.io` Pages currently has custom domain `cyphernetics.io` and HTTPS only for:
  - `cyphernetics.io`
  - `www.cyphernetics.io`
- `knots.cyphernetics.io` is currently `NXDOMAIN`.
- Pointing `knots.cyphernetics.io` at the current apex Pages host without a dedicated custom-domain binding returns GitHub 404s, so DNS alone is not enough.

## Remaining steps
1. Enable GitHub Pages on `codex-journal/knots`
   - Source: `gh-pages` branch, `/`
2. Set the Pages custom domain to:
   - `knots.cyphernetics.io`
3. Add DNS record:
   - `knots CNAME codex-journal.github.io`
4. Wait for Pages certificate issuance
5. Verify:
   - `http://knots.cyphernetics.io` redirects/serves correctly
   - `https://knots.cyphernetics.io` serves with valid cert
   - main `https://cyphernetics.io/` remains unchanged

## Current blocker
The available GitHub token can write branch contents but cannot administer Pages settings for the `knots` repo. Attempting to create or configure Pages via `gh api repos/codex-journal/knots/pages ...` returned HTTP 403.

## Fastest manual completion path
In GitHub repo settings for `codex-journal/knots`:
- Settings → Pages
- Build and deployment → Source: Deploy from a branch
- Branch: `gh-pages` / root
- Custom domain: `knots.cyphernetics.io`

Then in DNS:
- `knots CNAME codex-journal.github.io`

After that, re-run verification and close `codex-qn5`.
