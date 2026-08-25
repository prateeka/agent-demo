---
step_id: release-ticket
status: done
title: "Release ticket: Chevrolet"
---

## Scope

Record Release ticket id for the launch (files only — no Jira API). All step tickets and PR titles reference release.ticket_id from global context.

## Depends on

(none)

## Skill

platform/skills/destination-launch/steps/release-ticket/SKILL.md

## Details

**Files only — no Jira call made.**

### Recorded release ticket

| Field | Value |
|---|---|
| `release.ticket_id` | `RELEASE-chevrolet` |
| `release.ticket_url` | _(none — replace when Jira ticket exists)_ |

**Placeholder:** `RELEASE-chevrolet` — replace when real Jira ticket exists.

### Draft release description (manual Jira paste)

Destination launch for Chevrolet connector rollout.

**Destination:** Chevrolet (`chevrolet`)
**API family:** `chevrolet`

### In-scope step ids (link to this release)

All workflow steps for this launch reference `release.ticket_id` in PR titles and step tickets:

- `release-ticket`
- `taxonomy-connector-scaffold`
- `taxonomy-partner-flow`
- `taxonomy-ui`
- `rlg-addition`
- `oauth`
- `oauth-db-update`
- `partner-api-client`
- `request-builder-sender`
- `transposer-record-handler`
- `redpanda-topics`
- `delivery-endpoints-ui`
- `ig-ui`
- `da-ui`
- `grafana-dashboards`
- `tech-discovery`

### PR title convention

`[RELEASE-chevrolet] ...` until replaced with the real Jira key.
