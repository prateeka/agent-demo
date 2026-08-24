---
name: destination-launch-tech-discovery
description: >-
  Prepare Confluence Tech Discovery page draft for QA handoff on a destination launch.
---

# Step: tech-discovery

Draft a **Tech Discovery** Confluence page so QA can write the Integration QA Test Plan.

## Template structure (Amazon DM)

- Tech Discovery example: https://liveramp.atlassian.net/wiki/spaces/Integratio/pages/5691998228/Amazon+Data+Manager+API
- QA Test Plan example (downstream): https://liveramp.atlassian.net/wiki/spaces/CI/pages/5712118624/Amazon+Data+Manager+API+Integration+QA+TestPlan

Do **not** write the QA test plan — only the tech discovery document.

## Read first — exact global keys

Read `launches/{slug}/epic.md` → `## Global context` (destination, properties, oauth, platform, redpanda, grafana keys as available).

## Write to step task (local)

- Confluence draft link or page content summary
- Status; Done when page published or draft ready for human publish

## Return global keys (orchestrator merges)

- `confluence.tech_discovery_url` (when published)

## With Confluence MCP (later)

Publish page; return URL in `global_keys`.

## Sections to include

1. Overview / business context
2. API authentication (OAuth flow)
3. Endpoints and operations
4. Configuration properties (delivery + taxonomy)
5. Data flows (taxonomy sync, audience ingestion)
6. RLG / infrastructure (topics, services)
7. Metrics and monitoring
8. Known limitations / edge cases
9. Dev/test environment access

## Definition of done

- Tech Discovery page draft complete and linked on Jira issue (or URL in global keys)
