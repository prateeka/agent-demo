---
name: destination-launch-release-ticket
description: >-
  Record Release ticket id for the launch — files only; documents key/url in task
  file and global context. Does not call Jira.
---

# Step: release-ticket

Record the **Release ticket** for this launch so later steps and PR titles can reference one key.

## Files mode only — no Jira

**Do not call Jira MCP, Jira REST API, or any issue tracker.** Hackathon record layer is `launches/{slug}/` only.

| Do | Do not |
|---|---|
| Ask the user for an **existing** release key, or a **placeholder** to use until Jira exists | Create issues in Jira |
| Write key, URL (if known), and draft description to **`tasks/release-ticket.md`** | Use MCP tools named jira, atlassian, etc. |
| Return `release.ticket_id` / `release.ticket_url` in `global_keys` for orchestrator merge | Assume Jira MCP is available |

If the user has no key yet, use a documented placeholder (e.g. `RELEASE-{destination.slug}`) and note *"replace when real Jira ticket exists"* on the task file.

## PR convention

`[{release.ticket_id}] ...` in every implementation PR title once the release key is in global context.

## Read inputs (launch files)

- Launch epic `## Summary` from `launches/{slug}/epic.md`
- `destination.slug`, `destination.display_name` from global context

## Ask the user

- Existing release ticket key (e.g. `RLG-1234`) or OK to use a placeholder?
- Release ticket URL if they have one (optional)

## Write to step task (local)

Update `launches/{slug}/tasks/release-ticket.md` → `## Details`:

- Recorded `release.ticket_id` and `release.ticket_url` (if any)
- Draft release description (from epic summary) for manual Jira paste later
- Note: **files only — no Jira call made**
- List of in-scope step ids that should link to this release

Frontmatter `status`: `done` when id is recorded.

## Return global keys (orchestrator merges)

```yaml
global_keys:
  release.ticket_id: ...
  release.ticket_url: ...
```

Do **not** edit `epic.md` directly.

## Definition of done

- Release key documented on task file and returned in `global_keys`
- No Jira/API calls were made
- Orchestrator merged `release.ticket_id` into `epic.md` for downstream steps
