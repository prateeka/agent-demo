---
name: destination-launch-dist-types
description: >-
  dist-types step: Thrift in dist_types, return global keys to orchestrator,
  update step Jira issue. Spawned by orchestrator child agent.
---

# Step: dist-types

Add **dist_types** Thrift definitions for a new destination API.

## Repo

`dist_types` — see `platform/config/repos.yaml`

## Detect prior work

If issue `## Details` is filled, check repo for existing Thrift structs/unions and `version.rb` before adding duplicate union fields.

## Read first — exact global keys

- `release.ticket_id` — PR title prefix once set
- `destination.api_family`, `destination.display_name`

## Ask the user

- Delivery property names and whether each is externally configurable
- Taxonomy-specific properties (if applicable)
- OAuth endpoint union variant needed?
- Streaming format struct name and endpoint config struct
- Union field numbers (next free id in each Thrift union)

## Internal sub-steps (skill-owned)

1. Streaming deliverer format + union field on `Format`
2. Streaming endpoint config + union field
3. Taxonomy config struct + union (if needed)
4. OAuth endpoint config variant (if needed)
5. Bump `version.rb` / codegen per repo convention
6. Tests / thrift compile

## Write to step task (local)

- Narrative handoff, file paths, verification output
- Status; PR URL; PR title `[JIRA-KEY] Add {destination} dist_types Thrift schemas`

## Return global keys (orchestrator merges)

- `properties.delivery`, `properties.taxonomy`
- `thrift.streaming_format`, `thrift.streaming_endpoint_config`, `thrift.taxonomy_config`, `thrift.oauth_endpoint_config`

Structured outputs only — not full questionnaires.

## Definition of done

- Thrift compiles; tests pass per repo convention
- PR opened/merged; union field numbers documented on issue

## Verification

Thrift lint, gradle generate, tests per `dist_types` repo conventions.
