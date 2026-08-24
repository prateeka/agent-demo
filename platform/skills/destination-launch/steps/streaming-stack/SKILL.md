---
name: destination-launch-streaming-stack
description: Streaming stack step — transposer, request builder, sender, partner APIs.
---

# Step: streaming-stack

Implement streaming delivery for the destination in `dist` + `dist_types`.

## Repos

`dist`, `dist_types` — see `platform/config/repos.yaml`

## Detect prior work

If `## Details` is filled, diff repo against recorded file paths before re-implementing.

## Read first — exact global keys

- `destination.api_family`, `thrift.streaming_format`, `thrift.streaming_endpoint_config`
- `oauth.type` (if needed for client wiring)

## Ask the user

- Audience ingestion mandatory headers?
- Request payload shape / operation types?
- Rate limits or retry policy specifics?
- Partner API base URL(s)?
- Metric names to record for Grafana (destination-specific)?
- Transposer / record handler naming (`*_MANAGER` config key)?

## Internal sub-steps (skill-owned)

1. Partner API client + constants
2. Request builder
3. Request sender
4. Transposer / record handler / relevant field selector
5. Config layer wiring
6. Error handling / invalid dataset cache if needed

## Write to step task (local)

- Header names, API URLs, file paths, test output

## Return global keys (orchestrator merges)

- `streaming.api_base_urls`
- `grafana.metrics.streaming`

## Definition of done

- Request builder/sender tests pass; transposer wired; metrics registered

## Amazon DM reference

Amazon DM [1/4]–[4/4], `RelevantFieldSelectorFactory`, `AmazonDMRequestBuilder`, `AmazonDMRequestSender`

## Verification

Unit tests for request builder/sender; relevant field selector tests per repo conventions.
