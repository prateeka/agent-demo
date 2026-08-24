---
name: destination-launch-request-builder-sender
description: Request builder and request sender for streaming delivery in dist.
---

# Step: request-builder-sender

Implement **request builder** and **request sender** in `dist` + `dist_types`.

## Repos

`dist`, `dist_types` — see `platform/config/repos.yaml`

## Detect prior work

If `## Details` is filled, diff repo against recorded file paths before re-implementing.

## Read first — exact global keys

- `release.ticket_id`
- `destination.api_family`, `thrift.streaming_format`, `thrift.streaming_endpoint_config`
- `streaming.api_base_urls`
- `oauth.type`

## Ask the user

- Audience ingestion mandatory headers?
- Request payload shape / operation types?
- Batch vs single-record send semantics?

## Internal sub-steps (skill-owned)

1. Request builder — payload assembly from delivery properties
2. Request sender — HTTP send path, response handling
3. Unit tests for builder and sender

## Write to step task (local)

- Header names, operation types, file paths, test output, PR link

## Return global keys (orchestrator merges)

Return only keys listed above unless the user explicitly asks to add more to global context.

## Definition of done

- Request builder/sender tests pass; send path wired to partner API client

## Amazon DM reference

`AmazonDMRequestBuilder`, `AmazonDMRequestSender`

## Verification

Unit tests for request builder/sender per repo conventions.
