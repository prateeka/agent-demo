# Destination Launch — Jira model

**Live system:** Jira only. User → orchestrator → child agents.

## Epic scope

**One Epic per launch.** One destination rollout = one Epic. Do not create multiple Epics for the same launch. Environment-specific ids (dev/stage/prod) live on step issues and in `## Global context` keys, not as separate Epics.

## Issues

| Jira | Role |
|---|---|
| **Epic** | One per launch |
| **Epic description** | Business summary + `## Global context` YAML (**orchestrator writes only**) |
| **Release ticket** | Created in step `release-ticket` — **first**; all step tickets and PRs link to it |
| **Story/Task** | Per selected workflow step; label `dstep:{step_id}` |
| **Task description (stub)** | From `workflow.yaml` + Details sentinel |
| **Task description (full)** | Child writes step-local context when executed |
| **Comments** | Users only |

## Global context protocol

- **Children do not write Epic.** They return `global_keys` in summary; orchestrator merges into `## Global context`.
- **One child at a time** per Epic
- **`release.ticket_id`** — set by `release-ticket` step; later steps and PRs reference it

## Step issue identity

- Primary: Jira label `dstep:{step_id}`
- Fallback: `## Step` / `dstep:{step_id}` in description body

## Orchestrator routing

- `platform/workflow.yaml` — DAG, checklist, presets
- Jira status per step; `not_created` if no issue

## Status mapping

| Workflow | Typical Jira |
|---|---|
| `not_created` | No issue |
| `pending` | To Do |
| `in_progress` | In Progress |
| `done` | Done |
| `blocked` | Blocked |

## Approval gates

Explicit user confirm before spawning: `release-ticket`, `rlg-addition`, `delivery-endpoints-ui`, `taxonomy-ui`, `ig-ui`, `da-ui`, `redpanda-topics` (files mode and Jira target).

## PR convention

`[{release.ticket_id}] description`

## Jira MCP failure

Child prints intended payloads; orchestrator surfaces for manual paste.
