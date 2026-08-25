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
| Connector specs | `docs/connectors/*-spec.md` — seed `destination.*` on create |
| Step skills | `platform/skills/destination-launch/steps/{skill}/SKILL.md` |

## User interaction (required)

**Never spawn a child until the user has chosen a step** — by naming `{step_id}`, toggling checkboxes, or an explicit run phrase (e.g. *"run taxonomy-connector-scaffold"*, *"start taxonomy preset"*). **Exception:** **`release-ticket` auto-runs** after create launch (rule 8).

### Dependency-ordered checklist (required format)

Whenever the orchestrator shows workflow steps — **create launch**, **status**, **what's next** — use this format. Do **not** use a numbered-only table.

**Build the list**

1. Load all steps from `platform/workflow.yaml` (`id`, `jira_title`, `summary`, `depends_on`).
2. **Sort in dependency order:** topological sort on `depends_on` (every dependency before its dependents). **Tie-break:** order steps appear in `workflow.yaml`.
3. Render **one markdown task-list line per step** — **every** workflow step, always (never omit rows).

**Setup block** (show after create launch and on status when relevant — always **include**, never skip):

```markdown
Setup:

- [x] Connector context — **done** · `amazon-dm-advertiser-spec.md`
- [x] `release-ticket` — Release ticket (files only) — **done** · auto on create
```

- **Connector context:** always **`[x]` … **done**** once `epic.md` exists. Label **`· {spec-filename}`** when seeded from an existing `docs/connectors/*-spec.md`; else **`· slug {slug}`** (no error, no invented spec path).
- **`release-ticket`:** **`[x]` … **done** · auto on create** after auto-run; **`[x]` … **auto on create**** on scope selection before run completes.

**Scope selection** (create launch — boxes = selected for this launch):

```markdown
Setup:

- [x] Connector context — **done** · `amazon-dm-advertiser-spec.md`
- [x] `release-ticket` — Release ticket (files only) — **auto on create**

Select steps for this launch:

- [ ] `taxonomy-connector-scaffold` — Taxonomy connector scaffold
- [ ] `taxonomy-partner-flow` — Taxonomy partner flow · depends on: taxonomy-connector-scaffold
…
```

**Status / execute** (every workflow step + setup block):

```markdown
Setup:

- [x] Connector context — **done** · slug `mac-apple`
- [x] `release-ticket` — Release ticket (files only) — **done** · auto on create

Launch checklist (dependency order):

- [x] `taxonomy-connector-scaffold` — Taxonomy connector scaffold — **done**
- [ ] `taxonomy-partner-flow` — Taxonomy partner flow — pending · **ready now**
- [ ] `oauth` — OAuth client and endpoint config — skipped
…
```

**Line rules**

| Mode | `[x]` means | `[ ]` means |
|---|---|---|
| Setup / connector | Context seeded in `epic.md` — always show **done** once launch exists | N/A before create |
| Scope selection | User selected — create `tasks/{step_id}.md` | Not selected — no task file yet |
| Status / execute | `status: done` | not done — `pending`, `in_progress`, `not_created`, `blocked`, or **`skipped`** |
| **`release-ticket`** | Always **`[x]`** after create | Before auto-run: **`[x]` auto on create** only |

- Append **`· **ready now**`** when the step has a task file, `status: pending`, and every `depends_on` task is `done`.
- Append **`· resumable`** when `status: in_progress`.
- **`skipped`** when no task file was created for this step (not selected at create) — **do not** use *not in scope*, *excluded*, or missing-spec error lines.
- Append **`· depends on: id1, id2`** only when `depends_on` is **non-empty**.
- When blocked/waiting, add **`· waiting on: id`**.

**Presets** (`workflow.yaml` → `presets:`) pre-check scope boxes for **other** steps only — **`release-ticket` stays `[x]` fixed**. Presets: **`taxonomy`**, **`minimal`**, **`implementation`**, **`all`**.

**Accept scope replies:** preset name · list of step ids · *"all except …"* · pasted checklist with toggled `[x]`/`[ ]`.

**Dependency warning:** if user selects a step but not all of its `depends_on`, list missing deps and ask to add them or confirm anyway.

### When to ask (do not guess or auto-pick)

Ask **before** creating task files or spawning when the user:

- Creates a launch **without** naming a preset or step list
- Says vague continue intents: *"what's next?"*, *"status"*, *"continue"*, *"run a step"*, *"work on the launch"*, *"start"*
- Names a launch but not a step

### Status / what's next response format

1. Resolve launch folder (ask slug if multiple launches exist).
2. Load `workflow.yaml` and each `tasks/{step_id}.md` frontmatter (if any).
3. Present the **dependency-ordered checklist** (status mode above) for **every** workflow step, including `release-ticket` as **`[x]` done** when auto-run completed or task `status: done`.
4. **End with:** *"Which step should I run next? (step id from the list). To add steps to scope, name step ids."*
5. **Wait for the user's reply** before spawning.

If the user names **multiple ready steps**, confirm the ordered list, then run **one child at a time** in dependency order (rule 4).

### Create launch — scope intake

**`release-ticket` stays on the checklist** — always `[x]`, fixed, labeled **`auto on create`**. Not toggled by presets or user checkboxes. Always create `tasks/release-ticket.md` and **spawn it immediately** after scope confirm (files only, no Jira).

If the user did not specify other steps, show the scope-selection checklist with **`release-ticket` already `[x]`**. Offer presets for other steps:

> Presets: **`taxonomy`** · **`minimal`** · **`implementation`** · **`all`**

Do **not** default a full preset silently without showing the checklist.

**After scope confirm:** create tasks, auto-run `release-ticket`, merge `global_keys`, then show the **status checklist** with **`release-ticket` as `[x]` done · auto on create** and ask what to run next.

## Rules

1. **Never** execute step domain work inline — spawn `Task` child with step skill.
2. **Create and update** `launches/{slug}/` — `epic.md` + `tasks/{step_id}.md` (files mode).
3. **Only orchestrator merges** `## Global context` in `epic.md` — children return `global_keys`; orchestrator merges.
4. **One child at a time** per launch folder.
5. Routing: `workflow.yaml` + task file `status` in YAML frontmatter (`pending` | `in_progress` | `done` | `blocked`).
6. Task scaffolding from `workflow.yaml` — do not read all step SKILL.md at launch.
7. Step identity: file `tasks/{step_id}.md` (filename = step id).
8. **`release-ticket`:** always on checklist — **`[x]` fixed** on scope selection (**auto on create**); after auto-run show **`[x]` done · auto on create**. Always create task + spawn on new launch (files only, no Jira). Not toggled by presets. Taxonomy steps do not depend on it.
9. **Approval before spawn:** `rlg-addition`, `oauth-db-update`, `delivery-endpoints-ui`, `taxonomy-ui`, `ig-ui`, `da-ui`, `redpanda-topics`. **`release-ticket`:** bundled into create-launch confirm — no separate gate when auto-running after create; confirm if re-run standalone.
10. **Platform UI steps (`*-ui`):** default to **textual UI runbook** — no REST API until platform team documents one; record ids on task file after operator confirms live UI work.
11. **`rlg-addition` / `oauth-db-update`:** platform DB steps — runbook/SQL today, not dist code.
12. **PR linkage:** remind children that PR titles use `[{release.ticket_id}]` once `release.ticket_id` is in global context.
13. **End-of-iteration cleanup (harness edits):** before finishing any turn that renames, removes, or splits steps/docs, delete redundant files and empty directories. Step folders must match `workflow.yaml` ids; remove stale step symlinks from `.cursor/skills/` and `.claude/skills/`; grep the repo for removed step ids and fix or delete dead references. Briefly note cleanup in the user summary when anything was removed.

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

## Connector spec → global context (create launch)

**Do not ask the user for `api_family`.** It is connector-specific machine metadata, not epic narrative.

### Discover specs (required — no invented paths)

Before mentioning any connector spec path:

1. **List only files that exist** under `docs/connectors/` matching `*-spec.md` (read the directory — do not guess filenames from the user's launch name or slug).
2. When offering a connector choice, show **only** discovered specs (slug + path that exists).
3. **Never** display, suggest, or error with a constructed path like `docs/connectors/{slug}-spec.md` unless that file is present on disk.
4. If the user's launch name has **no** matching spec file: seed `destination.slug` / `api_family` from what they asked for (slug; `api_family` = slug with `-` → `_`); show **`[x] Connector context — **done** · slug {slug}`** in the Setup block — **never** error, block, or cite a non-existent spec path.

**Example — only spec in repo today:**

| Slug | File |
|---|---|
| `amazon-dm-advertiser` | `docs/connectors/amazon-dm-advertiser-spec.md` |

If exactly one spec exists and the user did not name another connector, use it without asking.

### Resolve and seed

When a spec file **exists**:

1. Read the **Summary block** fenced YAML near the top
2. Seed `## Global context` from spec `destination:` — `slug`, `display_name`, `api_family`
3. Copy other top-level spec keys only if defined in the spec and steps need them later (do not invent keys)
4. User may override `display_name` in epic text only — do not re-interview for `api_family` or slug when the spec is authoritative

**Ask the user only for epic narrative + connector choice (when multiple specs exist or name is ambiguous):**

| Ask | Goes to |
|---|---|
| Which connector? — **only from discovered `docs/connectors/*-spec.md` list** | resolves existing spec → global context |
| Benefit, why now, scope (optional if user gives one epic paragraph) | `epic.md` → `## Summary` |
| Step checklist (presets or checkboxes) | which `tasks/*.md` to create |

## Create launch

1. **Intake** per **Connector spec → global context** above — not `api_family` as a separate question.
2. **Create folder** `launches/{slug}/` with `epic.md` (`## Summary` + seeded `## Global context` YAML).
3. **Scope checklist** — full dependency-ordered list; **`release-ticket` row fixed `[x]`**; presets pre-check other boxes.
4. **Warn** if a checked step has unchecked / missing `depends_on` task files.
5. **Create** `tasks/release-ticket.md` **always**, plus `tasks/{step_id}.md` for each checked step.
6. **Auto-run `release-ticket`** — spawn child, merge `global_keys`; respond with folder path, **Setup block** (connector + release-ticket both **`[x]` done**), full step checklist, what's **ready now**.

## Resolve launch

User gives launch slug or display name → folder under `launches/`.

## What's next?

1. Load `workflow.yaml`
2. Per step: `not_created` if no `tasks/{step_id}.md`; else read frontmatter `status`
3. Ready = file exists, `status: pending`, all `depends_on` tasks are `done`
4. **Resume:** steps with `status: in_progress` — report as resumable even when not "ready"
5. **Always** present the dependency-ordered checklist and ask which step to work on (see **User interaction**).

## Work on step `{step_id}`

1. Resolve launch folder + task file (create task if missing, user confirms)
2. Warn if `depends_on` not `done`
3. Confirm before spawn: `rlg-addition`, `oauth-db-update`, `delivery-endpoints-ui`, `taxonomy-ui`, `ig-ui`, `da-ui`, `redpanda-topics` (`release-ticket` only if re-run standalone — not when auto-run after create launch)
4. Spawn one child with launch path + task path
5. Merge returned `global_keys` into `epic.md`
6. Brief summary to user
7. If the child renamed/removed harness files (skills, workflow, docs): run **end-of-iteration cleanup** (rule 13)

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

  release-ticket: files only — do NOT call Jira MCP or any issue tracker API.
cwd: repo from workflow step (see repos.yaml)
```

## Status

Per step: `not_created` | `pending` | `in_progress` | `done` | `blocked` (+ dep reason).

## Jira mode (future)

When Jira MCP is enabled, same rules apply — swap paths for Epic key + issue key. Not active in hackathon.
