# HappyRoom Requirements

更新时间：2026-05-06

## Active / Recent Requirements

1. Role visualization: PM/Builder/Reviewer must appear as visible pixel people in the room.
2. Drag summary: dragging a role to the computer should trigger a stable summary flow.
3. Role-specific summary: dragging a role now returns only that role's own daily work summary.
4. Yesterday Notes: one-click summaries should be recorded in Yesterday Notes, not buried in Team/Visitors notes.
5. Role movement: dropped roles should stay near the drop location and not snap back to sparse points.
6. Role skins:
   - Upload PNG/JPG sprite sheets.
   - Support 8 columns × 7 rows with square frames.
   - Tolerate real generated images with slight dimension drift and near-magenta backgrounds.
   - Support per-role apply and refresh persistence.
   - Provide usable tabs/single-card configuration UI.
7. Owner Status Cat: cat states have explicit owner-status meaning.
8. Fireplace board: feature is currently suspended/hidden by user request.
9. Project traceability: all requirements/tasks/acceptance/decisions should be recorded in `MyAIHappyRoom/docs/`.

## MVP Boundaries

- Uploaded skins are app-managed files under `uploads/role-skins/`, not committed to git.
- Fireplace board / PPT presenter is suspended until reprioritized.
- MATA gateway and private token-based flows are not copied directly.

## Backlog Candidates

- Pluggable chat / recent logs panel.
- Asset list export and memo generation scripts.
- Revisit fireplace board with UX-first redesign if Vivi reopens it.
