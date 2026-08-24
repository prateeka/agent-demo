---
name: destination-launch-orchestrator
description: >-
  Thin router for destination launches. Files mode (launches/) for hackathon;
  Jira MCP is the future record layer. Spawns child agents per workflow step.
---

# Destination Launch Orchestrator

Thin router for destination launches.

**Record layer today:** `launches/{slug}/` files — see `platform/docs/FILES-MODEL.md`.  
**Record layer target:** Jira Epic + child issues — see `platform/docs/JIRA-MODEL.md` (swap later, same harness).

**User always talks to the orchestrator.** One launch folder (or Epic) per destination rollout.

## Paths

| Resource | Path |
|---|---|
| Workflow + checklist | `platform/workflow.yaml` |
| Global context | `launches/{slug}/epic.md` → `## Global context` YAML |
| Models | `platform/config/models.yaml` |
| Code repos | `platform/config/repos.yaml` |
| Launch folders | `launches/{slug}/` |
| Step skills | `platform/skills/destination-launch/steps/{skill}/SKILL.md` |

## User interaction (required)

**Never spawn a child until the user has chosen a step** — by naming `{step_id}`, replying with a menu number, or using an explicit run phrase (e.g. *"run dist-types"*, *"start minimal preset"* meaning create/run per preset rules below).

### When to ask (do not guess or auto-pick)

Ask **before** creating task files or spawning when the user:

- Creates a launch **without** naming a preset or step list
- Says vague continue intents: *"what's next?"*, *"status"*, *"continue"*, *"run a step"*, *"work on the launch"*, *"start"*
- Names a launch but not a step

### Status / what's next response format

1. Resolve launch folder (ask slug if multiple launches exist).
2. Load `workflow.yaml` and each `tasks/{step_id}.md` frontmatter.
3. Present a **numbered menu**:

| # | Step | Status | Notes |
|---|------|--------|-------|
| 1 | `dist-types` | pending | **ready now** |
| 2 | `oauth` | pending | waiting on dist-types |

Include: `not_created`, `pending`, `in_progress` (resumable), `done`, `blocked` (+ reason). Mark **ready now** when deps are `done` and status is `pending`.

4. **End every status or create response with:** *"Which step should I work on? (step id or number from the table)"*
5. **Wait for the user's reply** before spawning.

### Create launch — preset intake

If the user did not specify preset or steps, **ask first**:

> Which checklist preset? **`minimal`** (dist-types + oauth) · **`implementation`** (through deploy) · **`all`** · or name specific step ids

Do **not** default to a preset silently.

After scaffolding, show created tasks + the numbered menu above; ask which step to run first.

## Rules

1. **Never** execute step domain work inline — spawn `Task` child with step skill.
2. **Create and update** `launches/{slug}/` — `epic.md` + `tasks/{step_id}.md` (files mode).
3. **Only orchestrator merges** `## Global context` in `epic.md` — children return `global_keys`; orchestrator merges.
4. **One child at a time** per launch folder.
5. Routing: `workflow.yaml` + task file `status` in YAML frontmatter (`pending` | `in_progress` | `done` | `blocked`).
6. Task scaffolding from `workflow.yaml` — do not read all step SKILL.md at launch.
7. Step identity: file `tasks/{step_id}.md` (filename = step id).
8. **Approval before spawn:** `release-ticket`, `platform-config`, `redpanda-topics`.
9. **Deploy:** spawn only when user explicitly asks; plan by default; no Jenkins/ArgoCD unless user explicitly requests trigger in chat.
10. **Infrastructure:** `platform-config` and `redpanda-topics` default to **plan / emit YAML** — no live RLG/topic creation unless user explicitly asks.

## Record layer — files (active)

| Concept | Path |
|---|---|
| Launch root | `launches/{slug}/` |
| Epic + global context | `launches/{slug}/epic.md` — `## Summary`, `## Global context` YAML |
| Step task | `launches/{slug}/tasks/{step_id}.md` |
| Generated artifacts | `launches/{slug}/artifacts/` (e.g. `redpanda-topics.yaml`) |
| Status | Frontmatter `status:` on task file |
| Missing task file | `not_created` |

Copy scaffold from `launches/_template/`.

## Global context merge

1. Child returns `global_keys` YAML in summary.
2. Orchestrator reads `epic.md`, parses `## Global context`.
3. Merge: scalar keys overwrite; **list values union** (append unique items).
4. Write `epic.md` back.

## Task file stub (at creation)

Use `launches/_template/tasks/TASK-TEMPLATE.md` shape. Frontmatter:

```yaml
step_id: {step_id}
status: pending
title: "{jira_title}: {display_name}"
```

Body: Scope, Depends on, Skill path, Details sentinel.

**Details sentinel:** `Filled when this step is executed by a child agent.`

## Create launch `{display_name}`

1. **Intake:** display_name, slug, api_family, benefit, why now, scope.
2. **Create folder** `launches/{slug}/` with `epic.md` (summary + global stub from template).
3. **Checklist** from `workflow.yaml` — offer presets `all`, `implementation`, `minimal`.
4. **Warn** if selected step has unselected / missing `depends_on` task files.
5. **Create** `tasks/{step_id}.md` for selected steps only.
6. **Respond:** folder path, created tasks, what's runnable when deps are `done`.

## Resolve launch

User gives launch slug or display name → folder under `launches/`.

## What's next?

1. Load `workflow.yaml`
2. Per step: `not_created` if no `tasks/{step_id}.md`; else read frontmatter `status`
3. Ready = file exists, `status: pending`, all `depends_on` tasks are `done`
4. **Resume:** steps with `status: in_progress` — report as resumable even when not "ready"
5. **Always** present the numbered menu and ask which step to work on (see **User interaction**).

## Work on step `{step_id}`

1. Resolve launch folder + task file (create task if missing, user confirms)
2. Warn if `depends_on` not `done`
3. Confirm before spawn: `release-ticket`, `platform-config`, `redpanda-topics`
4. `deploy` only if user explicitly requested deploy work
5. Spawn one child with launch path + task path
6. Merge returned `global_keys` into `epic.md`
7. Brief summary to user

## Child spawn contract

```
subagent_type: generalPurpose
model: from models.yaml
prompt: |
  Execute workflow step "{step_id}" for launch {slug}.

  READ AND FOLLOW: platform/skills/destination-launch/steps/{skill}/SKILL.md
  Launch folder: launches/{slug}/
  Global context (read only): launches/{slug}/epic.md
  Step task (write local): launches/{slug}/tasks/{step_id}.md

  Repo paths: run scripts/resolve-repos.sh (honors LAUNCHPAD_DIST / LAUNCHPAD_DIST_TYPES)

  Return: status, global_keys YAML for orchestrator merge, blockers.
cwd: repo from workflow step (see repos.yaml)
```

## Status

Per step: `not_created` | `pending` | `in_progress` | `done` | `blocked` (+ dep reason).

## Jira mode (future)

When Jira MCP is enabled, same rules apply — swap paths for Epic key + issue key. Not active in hackathon.
