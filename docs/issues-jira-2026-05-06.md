# HappyRoom Issue / Jira Snapshot — 2026-05-06

> Source of truth for May 6 work items discussed in Slock. Task IDs refer to Slock task numbers; commit IDs refer to `Onlyaguest/MyAIHappyRoom`.

## Status Legend

- **Done**: implemented and either user-confirmed or superseded by a later accepted path.
- **In Review**: implemented and awaiting final user/QA acceptance.
- **Suspended**: intentionally hidden/paused by user request.
- **Backlog**: documented but not currently active.

## Current Experience Baseline

| Field | Value |
|---|---|
| Repository | <https://github.com/Onlyaguest/MyAIHappyRoom> |
| Branch | `main` |
| Latest local/runtime commit | `0154997` |
| Runtime URL | `http://127.0.0.1:19000/?ts=202605061933` |
| Runtime command | `/opt/anaconda3/envs/data-system/bin/python3 backend/app.py` from repo root/backend |
| Health path | `/health` |
| Runtime note | Must use Python 3.10+; Apple Python 3.9 crashes on `dict | None` syntax. |

## Issues / Jira Items

| ID | Type | Title | Status | Owner | Commit(s) | Notes |
|---|---|---|---|---|---|---|
| HR-001 | Epic | Bootstrap HappyRoom from Star-Office-UI into MyAIHappyRoom | Done | Builder | `771da45` | Initial app import, README/run path, health/smoke verified. |
| HR-002 | Feature | PM/Builder/Reviewer role-status UI | Done | Builder | `771da45` | `/team-status`, role cards, fallback data. |
| HR-003 | Feature | Drag role to computer one-click summary | Done | Builder | `771da45`, `509eeda`, `03833db` | Stabilized after hotzone and overlay fixes. |
| HR-004 | QA | Validate baseline role/status/summary flow | Done | Reviewer | `771da45` | Initial QA passed. |
| HR-005 | Bug | PM/Builder/Reviewer not visible as pixel people | In Review | Builder | `261221c` | Pixel actors visible in room with labels/state. |
| HR-006 | Bug | Drag-to-computer was hard to hit / got stuck / Notes not updated | Done | Builder/PM | `509eeda`, `d520b73`, `d71663f`, `03833db` | User later confirmed issue was refresh/old-process related and path became OK. |
| HR-007 | Feature | Fireplace presentation board / PPT / presenter slot | Suspended | Builder | `ae29194`, `dfeb6bf`, `98dbc1b` | Built MVP, then user said it blocked UX; hidden and paused. |
| HR-008 | Feature | Owner Status Cat four states | In Review | Builder | `fb4efe0` | Cat mapped to owner status semantics. |
| HR-009 | UX | Denser role movement and dropped-position persistence | In Review | Builder | `fb4efe0`, `5334e81`, `29b3155` | Role anchors stay near release point; visible drop frame reduced. |
| HR-010 | Feature | One-click summaries appear in Yesterday Notes | Done | Builder | `fb4efe0`, `d71663f`, `03833db` | Notes update path restored after runtime refresh issue. |
| HR-011 | Feature | Per-role skin configuration API/UI | In Review | Builder/PM | `fb4efe0`, `29b3155`, `b12b0a0` | Upload/apply/list/delete; delete fallback blocker fixed. |
| HR-012 | Bug | Uploaded Vivi sprite sheets fail strict validation | In Review | Builder/PM | `e99d041` | Real images now auto-crop near 8:7 and tolerant-clean near-magenta background. |
| HR-013 | UX | Skin config panel hard to continue using after one role | In Review | Builder | `0154997` | Tabs + single-role card + bounded results area. |
| HR-014 | Feature | Dragged role should return only its own daily work summary | In Review | Builder | `0154997` | Summary/Yesterday Notes title `【<Role> 今日工作总结】`; no full-project digest. |
| HR-015 | Ops | Latest local experience link not running | In Review | PM | runtime only | Root cause: started with Python 3.9; restarted with Python 3.11 and verified health/smoke. |
| HR-016 | Docs | Keep code + progress/requirements/tasks/decisions in MyAIHappyRoom | In Review | Builder/PM | `98a3844`, this doc | `MySlockRoom` paused as backup only. |
| HR-017 | Research | Compare MATAHappyRoom requirements | In Review | Builder | `481c25a` | See `docs/mata-gap-analysis.md`. |
| HR-018 | Feature | Generic external status bridge | In Review | Builder | `993bda1` | See `docs/external-status-bridge.md`; hardcoded MATA gateway not copied. |
| HR-019 | Backlog | Pluggable chat/recent logs panel | Backlog | TBD | — | Created from MATA gap analysis; not prioritized. |
| HR-020 | Backlog | Asset list export and memo generation scripts | Backlog | TBD | — | Created from MATA gap analysis; not prioritized. |

## User Preferences / Decisions Captured

1. Vivi-facing summaries, links, and acceptance conclusions must be posted in the main channel, not hidden only in task threads.
2. `MyAIHappyRoom` is the single repo for both code and progress docs; `MySlockRoom` is paused.
3. Fireplace board feature is suspended/hidden until reprioritized.
4. For real skin assets, upload should be tolerant of small dimension drift and near-magenta backgrounds; users should not manually pre-process every image.
5. For drag-to-computer summary, the expected semantic is now role-specific daily summary, not full-project summary.

## AI Team Workflow / Roles

See `docs/team-workflow.md` for the agreed operating workflow, role ownership, backups, and release baseline template.
