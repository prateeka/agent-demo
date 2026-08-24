---
name: destination-launch-ig-ui
description: Integration group via platform UI — runbook today, REST API when available.
---

# Step: ig-ui

Create **integration group (IG)** via the **platform UI**. Links **delivery endpoints** and **taxonomy endpoints** created in prior UI steps.

## Execution mode

| Phase | Behavior |
|---|---|
| **Today** | **UI runbook** — operator creates IG in UI; id on task file |
| **Future** | REST API — update skill; **step id stays `ig-ui`** |

Do **not** call a REST API until one is documented for this step.

## Detect prior work

Read `launches/{slug}/tasks/ig-ui.md`. If `## Details` is not the stub sentinel, diff recorded id before re-creating.

## Read first — exact global keys

- `release.ticket_id`
- `platform.delivery_endpoint_ids`
- `platform.taxonomy_endpoint_ids`

## Ask the user

- IG naming / grouping rules?
- Runbook only vs live UI creation now?

## Write to step task (local)

- UI runbook (screens, fields, linkage to delivery endpoints)
- Recorded id after operator confirmation

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.integration_group_id: ...
```

## Definition of done

- Runbook complete; id in `global_keys` when live UI work is done
