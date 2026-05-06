# Vivi AI Development Team Workflow

## One-line Flow

Vivi request → PM scopes and writes acceptance → Builder implements → Release confirms runtime → Reviewer validates → PM posts main-channel conclusion → Watcher records context.

## Core Roles

| Role | Primary | Backup | Responsibility |
|---|---|---|---|
| PM | `@vPM` | `@PM` | Product + project scope, priority, task split, acceptance, main-channel summary. |
| Builder | `@vBuilder` | `@Builder` | Code implementation, bug fixes, self-test, commit handoff. |
| Reviewer | `@vReviewer` | `@Reviewer` | User-path QA, failure paths, blockers, acceptance recommendation. |
| Watcher | `@vWatcher` | `@InformationCollector` / `@ViviCycle` | Facts, decisions, status, risks, compressed context. |
| Release | `@vRelease` | `@vBuilder` → `@vPM` | Runtime commit, port/process/cache, health, links, rollback. |
| Architect | `@Architect` | — | Complex architecture, interfaces, data model, migration risk. |
| UX Writer | `@UXWriter` | — | Labels, empty states, errors, guidance, next-step copy. |

## Response / Escalation Rule

- Blocking work, test handoff, review, or environment issue: switch to backup after 1–2 minutes without response.
- Non-blocking collaboration: wait up to 10 minutes before escalation.
- Environment/experience issues (`link down`, `page unchanged`, `wrong version`) go directly to `@vRelease`.

## PM Task Template

```md
## Goal

## Scope

## Priority
P0 / P1 / P2

## Owner / Backup
- Owner:
- Backup:

## Acceptance Criteria
- 

## Release Fields
- Experience URL / port:
- Startup command + env/config:
- Health path:

## QA Focus
- Main path:
- Failure path:
- Regression risks:
```

## Builder Handoff Template

```md
## Commit / Branch

## Changes

## Validation

## Experience Entry

## Known Limits

## Rollback
```

## Release Baseline Template

```md
## Runtime Baseline
- Experience URL:
- Running commit:
- Port:
- Process / startup command:
- Health result:
- Cache / force-refresh note:
- Rollback point:
```

## Reviewer Output Template

```md
## Result
Pass / Fail / Conditional Pass

## Baseline
- Commit:
- URL:

## Coverage

## Findings

## Blockers

## Recommendation
Ready / Not ready for Vivi acceptance
```
