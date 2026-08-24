---
name: destination-launch-deploy
description: >-
  Deploy step — service matrix and deploy plan in Jira. No Jenkins/ArgoCD triggers
  unless the user explicitly asks to run deployment in this session.
---

# Step: deploy

Document which services need redeploy for dist_types + dist changes. **Default: plan only.**

## Default behavior (no explicit deploy request)

1. Build service matrix (required vs optional)
2. List ArgoCD paths / Jenkins jobs **as references** — do **not** trigger
3. Document smoke checks a human should run after deploy
4. Record plan on Jira issue

## Only when user explicitly asks to deploy / trigger / run Jenkins / ArgoCD

- Trigger jobs or apply changes only after clear user instruction in this session
- Document what was triggered and results on the Jira issue

## Read first

- epic.md `## Global context` — RLG id, services from prior steps
- Prior step issues (argocd-artifacts, platform-config, redpanda-topics)

## Detect prior work

If `## Details` is filled, check whether plan exists or deploy already ran before re-triggering.

## Internal sub-steps

1. Service matrix
2. Jenkins/ArgoCD job names and paths (reference)
3. Image tag / helm updates from argocd-artifacts
4. Post-deploy smoke checklist (for human or after explicit trigger)

## Amazon DM deploy pattern (reference)

| Service | Required? | Why |
|---|---|---|
| `opi-temporal` | Often yes | Config validation |
| `delivery-records-consumer` | Per RLG | Streaming delivery |
| `record_transposer` | Per change | If transposer modified |
| Taxonomy service | If taxonomy changed | Taxonomy deliverer |

## Write to step task (local)

- Service matrix, job names, smoke checklist, trigger results (if user asked to deploy)
- Status; PR title `[JIRA-KEY] ...` if applicable

## Return global keys (orchestrator merges)

- `deploy.services` — services in the deploy plan (or actually deployed if user triggered)

## Definition of done

- **Plan-only:** matrix + jobs documented on issue; status Done when plan is complete
- **After explicit deploy:** triggers documented + smoke results recorded

## Verification (after explicit deploy only)

- DSJ config build for destination RLG
- Service logs / metrics check
