---
name: destination-launch-delivery-endpoints-ui
description: Delivery endpoints via platform UI — runbook today, REST API when available.
---

# Step: delivery-endpoints-ui

Create **delivery endpoints** via the **platform UI**.

## Execution mode

| Phase | Behavior |
|---|---|
| **Today** | **UI runbook** — operator creates endpoints in UI; ids on task file |
| **Future** | REST API — update skill; **step id stays `delivery-endpoints-ui`** |

Do **not** call a REST API until one is documented for this step.

## Detect prior work

Read `launches/{slug}/tasks/delivery-endpoints-ui.md`. If `## Details` is not the stub sentinel, diff recorded ids before re-creating.

## Read first — exact global keys

- `release.ticket_id`
- `platform.rlg_id`
- `platform.oauth_integration_id`
- `properties.delivery`
- `oauth.type`, `oauth.metadata_keys`
- `thrift.streaming_endpoint_config`

## Ask the user

- Endpoint names / URLs per environment?
- Runbook only vs live UI creation now?

## Write to step task (local)

- UI runbook per endpoint
- Recorded ids after operator confirmation

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.delivery_endpoint_ids: [...]
```

## Definition of done

- Runbook complete; ids in `global_keys` when live UI work is done
