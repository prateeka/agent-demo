---
name: destination-launch-release-ticket
description: Create Release ticket linked to launch Epic and step Jira issues via launch files.
---

# Step: release-ticket

Create a **Release ticket** linked to the launch Epic and all step Jira tickets.

## PR convention

`[JIRA-KEY] ...` in every implementation PR title.

## Read inputs (launch files)

- Launch Epic and all linked step issues
- PR links from each step issue description
- Deploy step status

## Write to step task (local)

Update this step's issue with release checklist, linked tickets, release ticket key when created.

## Return global keys (orchestrator merges)

- `release.ticket_id`, `release.ticket_url`

## Actions (launch files)

Create Release issue; link to Epic and child tickets. User already confirmed via orchestrator before spawn.
