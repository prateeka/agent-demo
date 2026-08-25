# Destination Launch — Jira model

**Live system:** Jira only. User → orchestrator → child agents.

## Epic scope

**One Epic per launch.** One destination rollout = one Epic. Do not create multiple Epics for the same launch. Environment-specific ids (dev/stage/prod) live on step issues and in `## Global context` keys, not as separate Epics.

## Issues

| Jira | Role |
|---|---|
| **Epic** | One per launch |
| **Epic description** | Business summary + `## Global context` YAML (**orchestrator writes only**) |
| **Release ticket** | Step `release-ticket` — **files only** (no Jira MCP); records `release.ticket_id` on task file + global context for PR linkage |
| **Story/Task** | Per selected workflow step; label `dstep:{step_id}` |
| **Task description (stub)** | From `workflow.yaml` + Details sentinel |
| **Task description (full)** | Child writes step-local context when executed |
| **Comments** | Users only |

## Global context protocol

- **Children do not write Epic.** They return `global_keys` in summary; orchestrator merges into `## Global context`.
- **One child at a time** per Epic
- **`release.ticket_id`** — set by `release-ticket` step (files mode: user key or placeholder; **no Jira API** until MCP swap-in)

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

Explicit user confirm before spawning: `rlg-addition`, `oauth-db-update`, `delivery-endpoints-ui`, `taxonomy-ui`, `ig-ui`, `da-ui`, `redpanda-topics`. **`release-ticket`** auto-runs after create launch (files only); confirm only on standalone re-run.

Steps with `intake: questions` in `workflow.yaml` run a **question relay**: intake child returns questions → user answers in the orchestrator chat → execute child. The orchestrator does not own the question list.

## PR convention

`[{release.ticket_id}] description`

## Jira MCP failure

Child prints intended payloads; orchestrator surfaces for manual paste.
