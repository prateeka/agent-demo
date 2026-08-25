---
name: destination-launch-oauth-db-update
description: OAuth integration record in platform DB — runbook/SQL today, API when available.
---

# Step: oauth-db-update

Add or update the **OAuth integration** record in the **platform DB** (not dist code).

## Execution mode

| Phase | Behavior |
|---|---|
| **Today** | **DB runbook** — SQL, internal tool, or documented update steps; record `platform.oauth_integration_id` on task file |
| **Future** | Platform team adds REST API — update this skill; **step id stays `oauth-db-update`** |

Do **not** call a REST API until one is documented for this step.

## Detect prior work

Read `launches/{slug}/tasks/oauth-db-update.md`. If `## Details` is not the stub sentinel, diff recorded id before re-applying.

## Read first — exact global keys

- `release.ticket_id`
- `destination.slug`, `destination.display_name`
- `oauth.type`, `oauth.metadata_keys`
- `thrift.oauth_endpoint_config`

## Ask the user

- OAuth integration name / reuse existing?
- Target environment (dev/stage/prod)?
- Runbook only vs apply DB change now?

## Write to step task (local)

- DB runbook (table, fields, values) or tool steps
- Recorded `platform.oauth_integration_id` after verification
- Verification notes (query or config build)

## Return global keys (orchestrator merges)

```yaml
global_keys:
  platform.oauth_integration_id: ...
```

## Definition of done

- Runbook complete and, if user asked for live DB work, OAuth integration id recorded on task file and in `global_keys`
