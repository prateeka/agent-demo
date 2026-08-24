---
name: destination-launch-platform-config
description: Platform config runbook — RLG, endpoints, IG, destination account.
---

# Step: platform-config

Configure platform objects (RLG, endpoints, IG, DA). **Default: plan/runbook on task file** — create live objects only if user explicitly asks.

## Detect prior work

Read `launches/{slug}/tasks/platform-config.md`. If `## Details` is not the stub sentinel, diff recorded ids before re-creating.

## Read first — exact global keys

- `properties.delivery`, `properties.taxonomy`
- `oauth.type`, `oauth.metadata_keys`
- `thrift.streaming_endpoint_config`, `thrift.taxonomy_config`
- `streaming.api_base_urls`

## Ask the user

- RLG name / reuse existing?
- Plan-only vs create live objects now?

## Internal sub-steps (runbook-first)

1. RLG → `platform.rlg_id`
2. Delivery endpoints → `platform.delivery_endpoint_ids`
3. Taxonomy endpoints → `platform.taxonomy_endpoint_ids`
4. IG → `platform.integration_group_id`
5. DA → `platform.destination_account_id`

Mark manual vs automated on task file.

## Write to step task (local)

- Object ids or runbook steps, field values, verification notes

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.rlg_id: ...
  platform.delivery_endpoint_ids: [...]
  platform.taxonomy_endpoint_ids: [...]
  platform.integration_group_id: ...
  platform.destination_account_id: ...
```

## Definition of done

- All required platform objects exist in target environment
- Ids recorded on Jira issue and returned in `global_keys`
- Smoke: config build or UI verification documented

## Code work

Runbook-first; API automation when available. No code repo required unless team adds scripts in `agent-demo`.
