# Destination Launch — Files model (hackathon demo)

**Demo system of record:** `launches/{slug}/` — Jira MCP not required.

Live swap-in: same shapes map to Jira Epic + child issues (`platform/docs/JIRA-MODEL.md`).

## Layout

```
launches/{slug}/
  epic.md                 # Summary + ## Global context (YAML)
  tasks/
    {step-id}.md          # One per workflow step (e.g. oauth.md)
  artifacts/              # Generated YAML/specs (optional)
    redpanda-topics.yaml
```

## epic.md

- Title line: `# Launch: {display_name}`
- `## Summary` — business benefit, why now, scope (user/epic narrative at create time)
- `## Global context` — fenced YAML block; orchestrator **seeds** `destination.*` from an **existing** `docs/connectors/*-spec.md` when one matches; otherwise manual slug/`api_family` with **no invented spec path**; later merges child `global_keys` here

## tasks/{step-id}.md

```yaml
---
step_id: oauth
status: pending   # pending | in_progress | done | blocked
title: "OAuth client and endpoint config: {display_name}"
---

## Scope
{from workflow.yaml summary at creation}

## Depends on

taxonomy-connector-scaffold

## Details
Filled when this step is executed by a child agent.
```

**Sentinel:** `## Details` stub line means not yet executed — child runs "Detect prior work."

## Status mapping (files ↔ Jira)

| Files `status` | Jira equivalent |
|---|---|
| `pending` | To Do |
| `in_progress` | In Progress |
| `done` | Done |
| `blocked` | Blocked |

## Step identity

- Filename = `tasks/{step-id}.md` (primary)
- Optional frontmatter `step_id` must match filename

## Reference launch

Planned: `launches/amazon-dm-reference/` (Amazon DM / RLG 1101). Use `_template/` until added.
