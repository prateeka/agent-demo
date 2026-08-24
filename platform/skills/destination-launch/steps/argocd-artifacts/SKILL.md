---
name: destination-launch-argocd-artifacts
description: ArgoCD / RLG helm artifacts for destination streaming deployment.
---

# Step: argocd-artifacts

Create ArgoCD deployment artifacts for the destination RLG.

## Repo

`dist` — `argocd-k8s-deployment/`

## Detect prior work

If issue `## Details` is filled, check helm values paths before duplicating RLG entries.

## Read first — exact global keys

- `platform.rlg_id` (if already set — else take from user)

## Ask the user

- RLG id for values file naming?
- Kafka `max.request.size` / transaction timeout needs?
- Image tag / profiler version updates?

## Internal sub-steps

1. RLG-specific values files (e.g. `values-{rlg_id}.yaml`)
2. Image tags / profiler versions
3. Kafka tuning in consumer values
4. delivery-records-consumer values for RLG

## Write to step task (local)

- File paths, PR link, helm diff summary

## Return global keys (orchestrator merges)

None required — record helm paths on the task file.

## Definition of done

- ArgoCD artifact PR merged or paths documented; values validated in review

## Amazon DM reference

RLG 1101 ArgoCD artifacts; `max.request.size` 200MB, transaction timeout 10min patterns.
