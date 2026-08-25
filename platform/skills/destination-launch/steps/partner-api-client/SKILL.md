---
name: destination-launch-partner-api-client
description: Partner API client and constants for streaming delivery in dist.
---

# Step: partner-api-client

Implement the **partner API client** and shared constants in `dist` + `dist_types`.

## Repos

`dist`, `dist_types` — see `platform/config/repos.yaml`

## Detect prior work

If `## Details` is filled, diff repo against recorded file paths before re-implementing.

## Read first — exact global keys

- `release.ticket_id` — link step Jira and PRs to the release ticket
- `destination.api_family`, `thrift.streaming_format`, `thrift.streaming_endpoint_config`
- `oauth.type` (for client auth wiring)

## Ask the user

- Partner API base URL(s)?
- Auth headers beyond OAuth token?
- Rate limits or retry policy specifics?
- Client class naming convention for this destination?

## Internal sub-steps (skill-owned)

1. Partner API client class + constants
2. Base URL / environment config wiring
3. Auth header integration with OAuth client
4. Shared error / retry utilities if needed

## Write to step task (local)

- API URLs, file paths, test output, PR link (`[{release.ticket_id}] ...`)

## Return global keys (orchestrator merges)

- `streaming.api_base_urls`

## Definition of done

- Client compiles; constants and base URL wiring documented; unit tests for client setup pass

## Reference

Existing partner API client patterns in `dist` — constants, base URLs, auth headers. Read a comparable connector in the repo rather than assuming one.

## Verification

Unit tests for client initialization and auth header construction per repo conventions.
