---
name: destination-launch-oauth
description: OAuth client, endpoint config, validation — launch files + dist/dist_types code.
---

# Step: oauth

Implement OAuth for the destination in `dist` + `dist_types`.

## Detect prior work

If issue `## Details` is filled, check repo for existing OAuth client before re-implementing.

## Read first — exact global keys

- `destination.slug`, `destination.api_family`
- `thrift.oauth_endpoint_config`

## Ask the user

- OAuth token URL?
- Mandatory headers for token request?
- Metadata keys returned (e.g. `clientId`)?
- Sandbox vs prod token URLs?

## Write to step task (local)

- Token URL, headers, validation results, file paths
- Status, PR link; PR title `[JIRA-KEY] ...`

## Return global keys (orchestrator merges)

- `oauth.type`
- `oauth.metadata_keys`

Return only keys listed above unless the user explicitly asks to add more to global context.

## Definition of done

- OAuth client implemented; validation run documented
- PR opened/merged per team convention

## Verification

OAuth validation per repo conventions after implementation.
