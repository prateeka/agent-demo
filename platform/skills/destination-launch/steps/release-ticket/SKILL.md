---
name: destination-launch-release-ticket
description: Create Release ticket first — all step Jira tickets and PRs reference it.
---

# Step: release-ticket

Create the **Release ticket first**. Every subsequent step Jira ticket and implementation PR must reference this release.

## PR convention

`[{release.ticket_id}] ...` in every implementation PR title once the release key exists.

## Step Jira convention

When creating step tickets (Jira mode) or noting linkage (files mode):

- Link each step ticket to the Release ticket
- Include `release.ticket_id` in task file body for traceability

## Read inputs (launch files)

- Launch epic summary from `launches/{slug}/epic.md`
- Destination display name, api_family, scope

## Write to step task (local)

- Release ticket key, URL, checklist stub for roll-up as steps complete
- List of step ids that will link to this release

## Return global keys (orchestrator merges)

```yaml
global_keys:
  release.ticket_id: ...
  release.ticket_url: ...
```

## Actions

Create Release issue (or document intended payload if Jira MCP unavailable). User already confirmed via orchestrator before spawn.

## Definition of done

- Release ticket created or documented with key/url in task file and `global_keys`
- Orchestrator and later steps can read `release.ticket_id` from `epic.md`
