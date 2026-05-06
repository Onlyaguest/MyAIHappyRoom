# HappyRoom Decisions

## 2026-05-06

### D-001 Single repository tracking

- Code, progress, requirements, tasks, acceptance, and decisions live in `MyAIHappyRoom`.
- `MySlockRoom` is paused and retained only as historical backup.

### D-002 Main-channel visibility

- Conclusions, acceptance requests, and experience links for @ViviYang go in `#Happyroom` main channel.
- Threads are acceptable for execution details.

### D-003 Fireplace board suspended

- The fireplace board/PPT/presenter MVP was built but the user found it too blocking.
- It is hidden and suspended until reprioritized.

### D-004 Real user assets over strict validation

- Sprite upload must support good real generated images even if they differ slightly from exact machine constraints.
- Near-8:7 sheets should be auto-cropped to 8×7 square frames when safe.
- Edge-connected near-magenta backgrounds should be normalized/cleaned instead of hard-failing.

### D-005 Role-specific drag summary

- Dragging PM/Builder/Reviewer to the computer should return that role's own daily work summary only.
- It should not mix full-project digest or other roles' work unless a separate project-summary action is introduced.

### D-006 Release is part of the development loop

- Before user validation, the runtime commit, health, port, cache/force-refresh note, and rollback point must be known.
- Link-down/page-unchanged issues are Release-owned until environment is ruled out.
