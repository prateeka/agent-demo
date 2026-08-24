---
name: destination-launch-da-ui
description: Destination account via platform UI — runbook today, REST API when available.
---

# Step: da-ui

Create **destination account (DA)** via the **platform UI**.

## Execution mode

| Phase | Behavior |
|---|---|
| **Today** | **UI runbook** — operator creates DA in UI; id on task file |
| **Future** | REST API — update skill; **step id stays `da-ui`** |

Do **not** call a REST API until one is documented for this step.

## Detect prior work

Read `launches/{slug}/tasks/da-ui.md`. If `## Details` is not the stub sentinel, diff recorded id before re-creating.

## Read first — exact global keys

- `release.ticket_id`
- `platform.rlg_id`
- `platform.integration_group_id`

## Ask the user

- DA naming / account linkage?
- Runbook only vs live UI creation now?

## Write to step task (local)

- UI runbook (screens, fields, linkage to IG)
- Recorded id after operator confirmation

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.destination_account_id: ...
```

## Definition of done

- Runbook complete; id in `global_keys` when live UI work is done
