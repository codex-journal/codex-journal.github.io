# Agent Instructions

This project uses **bd** (beads) for issue tracking.

## Session Start

1. Run `bd prime` to load the beads workflow context
2. Run `bd ready` to see available work
3. Check `docs/plans/` for any active implementation plans

## Quick Reference

```bash
bd prime              # Load workflow context (run at session start)
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Plans

When creating an implementation plan, copy it into the repository at `docs/plans/<descriptive-name>.md` and commit it. Plans live in the repo so other agents and sessions can find them. Reference the relevant beads issue IDs in the plan.

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

