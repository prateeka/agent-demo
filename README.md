# LaunchPad — Team guide

Agent harness for **OPI streaming destination launches** at LiveRamp. **Share this repo** with anyone who wants to understand or try it.

**New here?** Clone **`master`** (default branch) and read **this file** — it is the only onboarding doc you need:

https://github.com/prateeka/agent-demo/blob/master/README.md

| | |
|---|---|
| **Repo** | https://github.com/prateeka/agent-demo |
| **Branch** | `master` (all work is here — no feature branch to check out) |
| **Record layer today** | `launches/{slug}/` files (`epic.md` + `tasks/*.md`) |
| **Record layer target** | Jira Epic + child issues (MCP) — same harness, swap later |
| **Hackathon connector spec** | `docs/connectors/amazon-dm-advertiser-spec.md` |
| **Reference launch** | `_template/` now; a completed-connector example **later** |

> **The harness does not need to be perfect** before the hackathon — we will fix gaps live. Feedback on direction and P0 demo blockers is welcome; polish is hackathon scope.

---

## What is LaunchPad?

Launching a new **OPI streaming destination** is **30+ manual steps** across code, Redpanda, deploys, ActFS, taxonomy, and backfill loops — mostly done from memory today.

**LaunchPad** encodes a completed streaming-destination launch as a **versioned template** so the next destination is faster:

| Capability | What it means |
|---|---|
| **Plan** | Shared workflow → launch checklist (like a Jira plan) |
| **Code** | Step skills scaffold Thrift / Java in `dist` / `dist_types` |
| **Infra** | Emit Redpanda topic YAML (e.g. `artifacts/redpanda-topics.yaml`); platform UI runbooks for RLG/endpoints/IG/DA |
| **Learn** | Skills and template improve after each launch (stretch goal during hackathon) |

This repo is the **initial agent harness** — orchestrator + workflow + step skills — not the full product. A CLI (`launchpad plan`, `launchpad scaffold`) may sit on top later.

---

## Try it in 5 minutes

### 0. Prerequisites

- **Cursor** (or Claude Code) recent enough to support **Agent Skills** — this repo is driven entirely from a chat window; there is no app or CLI to install.
- **GitHub access** to `prateeka/agent-demo`. If `git clone` fails with a permission error, ask for access rather than assuming the repo is broken.
- Implementation steps (`oauth`, streaming stack, taxonomy code, etc.) need local **`dist`** and **`dist_types`** checkouts — set env vars before running those steps.

### 1. Clone and open

```bash
git clone https://github.com/prateeka/agent-demo.git
cd agent-demo
# default branch is master — no checkout needed
```

Open the folder in **Cursor** (or Claude Code). On GitHub, open **`README.md` on the `master` branch** if you are browsing without cloning.

### 2. Link the orchestrator skill (optional)

Skills live in `platform/skills/` (committed). To show the orchestrator in the IDE skill picker, run **only this script** from the repo root:

```bash
./scripts/link-skills.sh
```

That creates a **symlink** (a pointer), not a runnable command. Do **not** paste paths like `.cursor/skills/destination-launch-orchestrator` into the terminal — zsh will report `permission denied` because it is not an executable.

Verify the link with:

```bash
ls -la .cursor/skills/
```

Expected (one launch skill; arrow is `ls` output, not something to type):

```text
destination-launch-orchestrator -> ../../platform/skills/destination-launch/orchestrator
```

Step skills stay in `platform/skills/destination-launch/steps/` — for child agents, not the picker.

### 3. Start a chat with the orchestrator

Use the IDE skill picker — **not** the terminal:

- **Cursor:** new chat → pick skill **destination-launch-orchestrator**
- **Claude Code:** same skill name (linked under `.claude/skills/`)

Then type your prompt in chat (e.g. *"Create a launch for amazon-dm-advertiser"*).

### 4. Create a launch

Example prompts:

- *"Create a launch for amazon-dm-advertiser"* — orchestrator reads `docs/connectors/amazon-dm-advertiser-spec.md`
- *"Create a launch using docs/connectors/amazon-dm-advertiser-spec.md"*

**Intake:** connector spec + epic narrative. **`release-ticket` appears on the checklist as done** after create (auto-run, files only). Pick other steps via checkboxes or presets (`taxonomy`, `minimal`, …).

The orchestrator scaffolds `launches/{slug}/` from `launches/_template/`:

| File | Purpose |
|---|---|
| `epic.md` | Launch summary + global context (YAML) |
| `tasks/{step_id}.md` | One task per workflow step (checklist) |
| `artifacts/` | Generated YAML (e.g. Redpanda topics) when steps run |

### 5. Run a step (optional)

- *"What's the status of my launch?"* — orchestrator shows all steps in **dependency order** with checkboxes (`[x]` = done, `[ ]` = pending / ready)
- *"Run taxonomy-connector-scaffold"* or *"Start taxonomy preset"*
- Steps with **`intake: questions`**: a child returns the questions; the orchestrator asks you those questions, then a second child runs with your answers (no `dist` edits before that)
- On **create launch**, pick steps by checking boxes (presets **`taxonomy`** · **`minimal`** · **`implementation`** · **`all`** pre-fill them)

The orchestrator spawns a **child agent** for step work — you stay in the orchestrator chat.

### 6. Verify

```bash
ls launches/
# e.g. launches/amazon-dm-advertiser/epic.md
ls launches/amazon-dm-advertiser/tasks/
```

Launch folders live under **`launches/{slug}/`** (connector specs stay in **`docs/connectors/`** — not created per launch).

### Code repos (for implementation steps)

Launch scaffolding works without them. To run steps that edit Thrift/Java:

```bash
export LAUNCHPAD_DIST=/path/to/dist
export LAUNCHPAD_DIST_TYPES=/path/to/dist_types
./scripts/resolve-repos.sh   # verify paths
```

See `platform/config/repos.yaml`.

---

## How the harness works

```text
You  →  destination-launch-orchestrator  (only skill in picker)
            │
            ├─ platform/workflow.yaml  (steps, deps, summaries)
            ├─ launches/{slug}/        (epic + tasks + artifacts)
            └─ spawns child agent per step
                  └─ platform/skills/destination-launch/steps/{name}/SKILL.md
```

- **You never invoke step skills directly** — orchestrator spawns children.
- **`release.ticket_id`** from `release-ticket` step (files only — user key or placeholder; no Jira API).
- **Platform UI (`*-ui`) / platform DB (RLG, OAuth) / Redpanda:** UI runbooks and YAML artifacts by default; live DB/UI/topic changes only if you explicitly ask.

---

## What we've built so far

| Phase | What we did |
|---|---|
| **1. Workflow design** | Sixteen steps in `platform/workflow.yaml` — release-ticket (files only); taxonomy before oauth |
| **2. Agent architecture** | Thin **orchestrator** routes; **fat step skills** do the work; child agents keep context clean |
| **3. Context model** | **Global** facts on `epic.md` (`## Global context` YAML); **local** detail on each `tasks/{step_id}.md` |
| **4. Files-first demo** | `launches/` folder layout and `_template/` — **no Jira MCP required for hackathon** |
| **5. Safety rules** | Confirm before release ticket (files only), platform DB (RLG, OAuth), platform UI, and Redpanda steps; plan/runbook by default; one launch folder per destination |

**Not done yet (expected hackathon work):** deeper step skills, validators, Jira swap-in, full code scaffolding, learning loop / template versioning, QA smoke step, multi-env keys.

---

## Files first, Jira later

**Jira is the long-term target** — one Epic per launch, child tickets per step, same shapes as our files.

**We start with files** so we can iterate on routing and skills without ticket overhead. When the harness is stable, we **swap the record layer** (orchestrator reads/writes Jira instead of `launches/`) — not a redesign.

| Phase | Record layer |
|---|---|
| **Hackathon / now** | `launches/{slug}/` |
| **After hackathon** | Jira MCP (see `platform/docs/JIRA-MODEL.md`) |

Details: `platform/docs/FILES-MODEL.md`.

---

## Workflow steps

**Authoritative order and dependencies:** `platform/workflow.yaml`.

| Step ID | What it covers | Depends on |
|---|---|---|
| *(auto)* `release-ticket` | Release ticket id on file — **auto on create**, shown as **done** on checklist | — |
| `taxonomy-connector-scaffold` | Taxonomy connector scaffold (dist_types + dist) | — |
| `taxonomy-partner-flow` | Taxonomy partner flow (hooks + segment body) | taxonomy-connector-scaffold |
| `taxonomy-ui` | Taxonomy endpoints via UI | taxonomy-connector-scaffold, taxonomy-partner-flow |
| `rlg-addition` | RLG DB addition | — |
| `partner-api-client` | Partner API client + constants | oauth |
| `request-builder-sender` | Request builder + sender | partner-api-client |
| `transposer-record-handler` | Transposer, record handler, field selector, metrics | request-builder-sender |
| `redpanda-topics` | Redpanda topic creation + YAML artifact | transposer-record-handler |
| `oauth` | OAuth client + endpoint config | — |
| `oauth-db-update` | OAuth integration DB update | oauth |
| `delivery-endpoints-ui` | Delivery endpoints via UI | rlg-addition, oauth-db-update |
| `ig-ui` | Integration group via UI | delivery-endpoints-ui, taxonomy-ui |
| `da-ui` | Destination account via UI | ig-ui |
| `grafana-dashboards` | Dashboards and alerts | rlg-addition, transposer-record-handler, taxonomy-partner-flow |
| `tech-discovery` | Confluence draft for QA | grafana-dashboards, transposer-record-handler |

**Presets:** `taxonomy` (scaffold + partner-flow + taxonomy-ui), `minimal` (scaffold + partner-flow), `implementation` (through redpanda-topics), `all`.

**Platform naming:** `*-ui` = platform UI runbooks (API later). `rlg-addition` / `oauth-db-update` = platform DB steps. **`taxonomy-connector-scaffold`** + **`taxonomy-partner-flow`** replace the old single taxonomy code step — scaffold writes Thrift/hook context; partner-flow writes `segment_body.*` for **`taxonomy-ui`**.

**Platform order:** `rlg-addition` → `delivery-endpoints-ui` (needs `oauth-db-update` after OAuth code); `taxonomy-connector-scaffold` → `taxonomy-partner-flow` → `taxonomy-ui`; then `ig-ui` (links endpoints + taxonomy) → `da-ui`.

**Reference launch** — planned; use `_template/` and create-new flow for now.

---

## What's in the repo

```
README.md                        # This file (team guide — start here on master)
docs/connectors/                 # Connector specs (e.g. amazon-dm-advertiser-spec.md)
platform/workflow.yaml           # Step DAG — source of truth
platform/config/repos.yaml       # dist / dist_types path resolution
platform/skills/destination-launch/   # Committed — orchestrator + step skills
.cursor/skills/                       # Orchestrator symlink only (picker)
.claude/skills/                       # Orchestrator symlink only
launches/
  _template/
```

---

## Demo paths

| Path | Good for |
|---|---|
| **Create new launch** | Scaffold folder + checklist from `_template/` |
| **Reference launch** (later) | Mid-launch resume demo when we add `launches/{reference-slug}/` |

---

## More detail

| Doc | When to read |
|---|---|
| `platform/docs/FILES-MODEL.md` | Files layout (today) |
| `platform/docs/JIRA-MODEL.md` | Jira layout (target) |
| `AGENTS.md` | Rules for Cursor/agents working in this repo |