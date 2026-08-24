---
name: destination-launch-taxonomy-ui
description: Taxonomy endpoints via platform UI — runbook today, REST API when available.
---

# Step: taxonomy-ui

Create **taxonomy endpoint objects** via the **platform UI**.

## Execution mode

| Phase | Behavior |
|---|---|
| **Today** | **UI runbook** — operator creates taxonomy endpoints in UI; ids on task file |
| **Future** | REST API — update skill; **step id stays `taxonomy-ui`** |

Requires **`taxonomy-deliverer`** (destination taxonomy code) to be done first.

Do **not** call a REST API until one is documented for this step.

## Detect prior work

Read `launches/{slug}/tasks/taxonomy-ui.md`. If `## Details` is not the stub sentinel, diff recorded ids before re-creating.

## Read first — exact global keys

- `release.ticket_id`
- `properties.taxonomy`
- `thrift.taxonomy_config`
- `grafana.metrics.taxonomy` (from taxonomy-deliverer, if set)

## Ask the user

- Taxonomy endpoint names / sync URLs?
- Runbook only vs live UI creation now?

## Write to step task (local)

- UI runbook per taxonomy endpoint
- Recorded ids after operator confirmation

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.taxonomy_endpoint_ids: [...]
```

## Definition of done

- Runbook complete; ids in `global_keys` when live UI work is done
