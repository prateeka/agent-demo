---
name: destination-launch-transposer-record-handler
description: Transposer, record handler, and field selector for streaming delivery.
---

# Step: transposer-record-handler

Implement **transposer**, **record handler**, and **relevant field selector** in `dist` + `dist_types`.

## Repos

`dist`, `dist_types` — see `platform/config/repos.yaml`

## Detect prior work

If `## Details` is filled, diff repo against recorded file paths before re-implementing.

## Read first — exact global keys

- `release.ticket_id`
- `destination.api_family`, `thrift.streaming_format`, `thrift.streaming_endpoint_config`
- `streaming.api_base_urls`

## Ask the user

- Transposer / record handler naming (`*_MANAGER` config key)?
- Metric names to record for Grafana (destination-specific)?
- Invalid dataset cache needed?

## Internal sub-steps (skill-owned)

1. Relevant field selector / factory
2. Transposer wiring
3. Record handler
4. Config layer wiring
5. Error handling / invalid dataset cache if needed
6. Destination-specific metrics registration

## Write to step task (local)

- Config keys, file paths, metric names, test output, PR link

## Return global keys (orchestrator merges)

- `grafana.metrics.streaming`

## Definition of done

- Transposer wired; record handler integrated; metrics registered; tests pass

## Amazon DM reference

Amazon DM [1/4]–[4/4], `RelevantFieldSelectorFactory`, transposer wiring

## Verification

Unit tests for relevant field selector and transposer per repo conventions.
