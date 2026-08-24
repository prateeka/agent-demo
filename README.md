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
| **Reference launch** | `_template/` now; Amazon DM example **later** |

> **The harness does not need to be perfect** before the hackathon — we will fix gaps live. Feedback on direction and P0 demo blockers is welcome; polish is hackathon scope.

---

## What is LaunchPad?

Launching a new **OPI streaming destination** is **30+ manual steps** across code, Redpanda, deploys, ActFS, taxonomy, and backfill loops — mostly done from memory today.

**LaunchPad** encodes the **Amazon Data Manager (RLG 1101)** launch as a **versioned template** so the next destination is faster:

| Capability | What it means |
|---|---|
| **Plan** | Shared workflow → launch checklist (like a Jira plan) |
| **Code** | Step skills scaffold Thrift / Java in `dist` / `dist_types` |
| **Infra** | Emit Redpanda / deploy YAML patterns (e.g. `artifacts/redpanda-topics.yaml`) |
| **Learn** | Skills and template improve after each launch (stretch goal during hackathon) |

This repo is the **initial agent harness** — orchestrator + workflow + step skills — not the full product. A CLI (`launchpad plan`, `launchpad scaffold`) may sit on top later.

---

## Try it in 5 minutes

### 0. Prerequisites

- **Cursor** (or Claude Code) recent enough to support **Agent Skills** — this repo is driven entirely from a chat window; there is no app or CLI to install.
- **GitHub access** to `prateeka/agent-demo`. If `git clone` fails with a permission error, ask for access rather than assuming the repo is broken.
- Implementation steps (`dist-types`, `oauth`, etc.) need local **`dist`** and **`dist_types`** checkouts — set env vars before running those steps.

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

Then type your prompt in chat (e.g. *"Create a new launch for MyDestination API"*).

### 4. Create a launch

Example prompts:

- *"Create a new launch for MyDestination API"*
- *"Create a launch for TestPartner — api family streaming"*

The orchestrator scaffolds `launches/{slug}/` from `launches/_template/`:

| File | Purpose |
|---|---|
| `epic.md` | Launch summary + global context (YAML) |
| `tasks/{step_id}.md` | One task per workflow step (checklist) |
| `artifacts/` | Generated YAML (e.g. Redpanda topics) when steps run |

### 5. Run a step (optional)

- *"What's the status of my launch?"*
- *"Run the dist-types step"* or *"Start minimal preset"*
- *"Show me the checklist"*

The orchestrator spawns a **child agent** for step work — you stay in the orchestrator chat.

### 6. Verify

```bash
ls launches/
# e.g. launches/my-destination-api/epic.md
ls launches/my-destination-api/tasks/
```

**Your launch will not show up in `git status` — that is intentional.** `.gitignore` excludes `launches/*` (except `_template/`) because active launches can contain internal URLs and partner detail. Nothing is broken; the files are on disk, just untracked.

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
- **Deploy:** plan only unless you explicitly ask to trigger Jenkins/ArgoCD.
- **Platform config / Redpanda:** plan or emit YAML by default; live infra only if you ask.

---

## What we've built so far

| Phase | What we did |
|---|---|
| **1. Workflow design** | Eleven steps in `platform/workflow.yaml` — DAG, dependencies, human summaries for checklists |
| **2. Agent architecture** | Thin **orchestrator** routes; **fat step skills** do the work; child agents keep context clean |
| **3. Context model** | **Global** facts on `epic.md` (`## Global context` YAML); **local** detail on each `tasks/{step_id}.md` |
| **4. Files-first demo** | `launches/` folder layout and `_template/` — **no Jira MCP required for hackathon** |
| **5. Safety rules** | Deploy / infra plan-only unless user explicitly asks; one launch folder per destination |

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
| `release-ticket` | Release ticket — **run first**; all Jira/PRs reference it | — |
| `dist-types` | Thrift in `dist_types` | release-ticket |
| `oauth` | OAuth client + endpoint config | dist-types |
| `taxonomy-deliverer` | Taxonomy on destination (code in dist) | dist-types, oauth |
| `partner-api-client` | Partner API client + constants | dist-types, oauth |
| `request-builder-sender` | Request builder + sender | partner-api-client |
| `transposer-record-handler` | Transposer, record handler, field selector, metrics | request-builder-sender |
| `rlg-addition` | RLG DB addition | release-ticket |
| `delivery-endpoints-ui` | Delivery endpoints via UI | rlg-addition, dist-types, oauth |
| `taxonomy-ui` | Taxonomy endpoints via UI | taxonomy-deliverer |
| `ig-ui` | Integration group via UI | delivery-endpoints-ui, taxonomy-ui |
| `da-ui` | Destination account via UI | ig-ui |
| `redpanda-topics` | Redpanda topic creation + YAML artifact | transposer-record-handler |
| `grafana-dashboards` | Dashboards and alerts | rlg-addition, transposer-record-handler, taxonomy-deliverer |
| `tech-discovery` | Confluence draft for QA | grafana-dashboards, transposer-record-handler |

**Presets:** `minimal` (release-ticket + dist-types + oauth), `implementation` (through redpanda-topics), `all`.

**Platform naming:** `*-ui` = platform UI runbooks (API later). `rlg-addition` = DB insert for RLG. `taxonomy-deliverer` = destination taxonomy code (not `taxonomy-ui`).

**Platform UI order:** `rlg-addition` → `delivery-endpoints-ui`; `taxonomy-deliverer` → `taxonomy-ui`; then `ig-ui` (links endpoints + taxonomy) → `da-ui`.

**Amazon DM reference launch** (RLG 1101) — planned; use `_template/` and create-new flow for now.

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
| **Amazon DM reference** (later) | Mid-launch resume demo when we add `launches/amazon-dm-reference/` |

---

## More detail

| Doc | When to read |
|---|---|
| `platform/docs/FILES-MODEL.md` | Files layout (today) |
| `platform/docs/JIRA-MODEL.md` | Jira layout (target) |
| `AGENTS.md` | Rules for Cursor/agents working in this repo |