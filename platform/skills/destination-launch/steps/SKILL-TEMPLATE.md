# Step skill template (files mode)

Copy into `steps/{name}/SKILL.md`.

---

## Detect prior work

1. Read `launches/{slug}/tasks/{step_id}.md`.
2. If `## Details` is not the stub sentinel — diff repo / prior artifacts; ask resume or redo.
3. Do not re-apply destructive changes without checking prior state.

## Read first — global context

Read `launches/{slug}/epic.md` → `## Global context`. List the keys this step needs in the skill itself.

## Ask the user

If `platform/workflow.yaml` has `intake: questions` for this step:

- **`phase: intake`:** return `user_questions` YAML from this skill; write `## Questions` on the task file; **do not** answer them; **do not** edit code repos or create git branches.
- **`phase: execute`:** read `## Answers (user-confirmed)`. If missing → `blocked`, no repo edits.

The orchestrator relays questions to the user. Do not expect the user to see questions asked only inside this child.

Otherwise (no `intake` flag): step-specific questions only, knowing they may never reach the user.

## Write to step task (local context)

Update `launches/{slug}/tasks/{step_id}.md`:

- Body: narrative, paths, verification, PR link
- Frontmatter `status`: `in_progress` while working; `done` when Definition of done met

## Return global keys (orchestrator merges epic.md)

Do **not** edit `epic.md` yourself. Return only keys documented in this skill:

```yaml
global_keys:
  key.path: value
```

## Definition of done

Explicit checklist before `status: done`.

## Code work

Repos from `workflow.yaml`. Run `./scripts/resolve-repos.sh` — requires `LAUNCHPAD_DIST` and `LAUNCHPAD_DIST_TYPES`.

---

## Adding a new step (authors)

1. `platform/workflow.yaml` entry (`intake: questions` if the step needs user answers before code repos)
2. Copy sections above into `steps/{name}/SKILL.md` — document read/return keys inline
3. On rename/remove: delete the old skill folder, empty parent dirs, and grep for stale step ids in README, `models.yaml`, `generate-reference-tasks.py`, and orchestrator rules

See `platform/docs/FILES-MODEL.md`.
