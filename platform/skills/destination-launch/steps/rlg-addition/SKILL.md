---
name: destination-launch-rlg-addition
description: Add RLG record in platform DB — runbook/SQL today, API when available.
---

# Step: rlg-addition

Add or reuse an **RLG** record in the **platform DB** (not dist code).

## Execution mode

| Phase | Behavior |
|---|---|
| **Today** | **DB runbook** — SQL, internal tool, or documented insert steps; record `platform.rlg_id` on task file |
| **Future** | Platform team adds REST API — update this skill; **step id stays `rlg-addition`** |

Do **not** call a REST API until one is documented for this step.

## Detect prior work

Read `launches/{slug}/tasks/rlg-addition.md`. If `## Details` is not the stub sentinel, diff recorded id before re-inserting.

## Read first — exact global keys

- `release.ticket_id`
- `properties.delivery`, `properties.taxonomy`
- `destination.display_name`

## Ask the user

- RLG name / reuse existing?
- Target environment (dev/stage/prod)?
- Runbook only vs apply DB change now?

## Write to step task (local)

- DB runbook (table, fields, values) or tool steps
- Recorded `platform.rlg_id` after verification
- Verification notes (query or config build)

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.rlg_id: ...
```

## Definition of done

- Runbook complete and, if user asked for live DB work, RLG id recorded on task file and in `global_keys`
