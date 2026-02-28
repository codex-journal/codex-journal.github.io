# CLAUDE.md

## Git Commits

- NEVER add "Co-Authored-By" lines to commits. No co-author trailers of any kind.
- Keep commit messages short and direct. No verbose bodies unless the change is genuinely complex.

## Project

- This is a static site: GitHub Pages at codex-journal.github.io (cyphernetics.io)
- NixOS environment. Tools accessed via `nix-shell` or `nix run`
- See `docs/plans/` for active implementation plans.

## Beads (Issue Tracking)

This project uses `bd` (beads) for issue tracking. You MUST follow this workflow:

1. Run `bd prime` at session start to load context
2. Run `bd ready` to see available work
3. Run `bd show <id>` to view issue details before starting work
4. Run `bd update <id> --status in_progress` to claim work
5. Run `bd close <id>` when work is complete
6. Run `bd sync` before pushing to sync beads state

Do NOT use `bd hooks install`. Hooks are uninstalled intentionally.
Do NOT set `sync.fork_protection` in `.beads/config.yaml`. Leave it alone.

See `AGENTS.md` for full session workflow and completion rules.

## Build

- `python3 build/build_index.py` generates `index.html` and `feeds.html` from templates
- `--no-feed` flag for offline/local dev
- Templates in `build/`, data in `_data/`
- Sidebars injected via `js/sidebars.js` on all pages

## Screenshots

```bash
nix run github:numtide/llm-agents.nix#agent-browser -- open <url>
nix run github:numtide/llm-agents.nix#agent-browser -- screenshot /tmp/out.png
nix run github:numtide/llm-agents.nix#agent-browser -- screenshot --full /tmp/out.png
```
