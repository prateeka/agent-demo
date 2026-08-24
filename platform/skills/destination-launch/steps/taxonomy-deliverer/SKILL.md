---
name: destination-launch-taxonomy-deliverer
description: Taxonomy deliverer implementation step for destination launches.
---

# Step: taxonomy-deliverer

Build taxonomy deliverer in `dist` + config in `dist_types`.

## Repos

`dist`, `dist_types`

## Read first

- epic.md ## Global context (launch files) — `properties.taxonomy[]`, `oauth.*`, `thrift.taxonomy_config`
- This step's Jira issue (from orchestrator)


## Ask the user

- Taxonomy mandatory headers for segment create/update/get?
- DSP vs AMC sharing rules?
- Template API vs custom deliverer path?
- Segment naming / id conventions?
- Taxonomy sync metrics to expose?

## Internal sub-steps (skill-owned)

1. Taxonomy config Thrift (if not in dist-types)
2. Deliverer class + request builders
3. Sharing rules (DSP/AMC etc.)
4. Unit + integration tests

## Write to step task (all answers)

- Update issue: per `JIRA-MODEL.md`
- **Body:** header details, endpoint paths, sharing rule narrative, test results
- Full header values and endpoint URLs → **task only**

## Return global keys (orchestrator merges)

- `properties.taxonomy` (if not already set)
- `grafana.metrics.taxonomy`

## Definition of done

- Taxonomy deliverer tests pass; sync smoke documented if available

## Amazon DM reference

`INTCORE-91` PR1/PR2, `AmazonDataManagerTaxonomyConfig`

## Verification

Taxonomy deliverer unit tests; taxonomy sync smoke in dev if available.
