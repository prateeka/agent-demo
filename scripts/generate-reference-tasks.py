#!/usr/bin/env python3
"""Generate task files for a reference launch folder (e.g. amazon-dm-reference).

Usage (when reference launch is added):
  python3 scripts/generate-reference-tasks.py --slug amazon-dm-reference --display "Amazon Data Manager API"

Not used until a reference launch folder exists under launches/.
"""
from pathlib import Path
import argparse

DISPLAY_DEFAULT = "Amazon Data Manager API"
SLUG_DEFAULT = "amazon-dm-reference"

# status per step for a mid-launch demo snapshot
STATUSES = {
    "dist-types": "done",
    "oauth": "done",
    "taxonomy-deliverer": "done",
    "streaming-stack": "done",
    "platform-config": "done",
    "redpanda-topics": "done",
    "argocd-artifacts": "pending",
    "grafana-dashboards": "pending",
    "deploy": "pending",
    "tech-discovery": "pending",
    "release-ticket": "pending",
}

DETAILS = {
    "dist-types": "Filled when this step is executed by a child agent.",
    "oauth": "Filled when this step is executed by a child agent.",
    "taxonomy-deliverer": "Filled when this step is executed by a child agent.",
    "streaming-stack": "Filled when this step is executed by a child agent.",
    "platform-config": "Filled when this step is executed by a child agent.",
    "redpanda-topics": "Emit launches/{slug}/artifacts/redpanda-topics.yaml when run.",
    "argocd-artifacts": "Filled when this step is executed by a child agent.",
    "grafana-dashboards": "Filled when this step is executed by a child agent.",
    "deploy": "Filled when this step is executed by a child agent.",
    "tech-discovery": "Filled when this step is executed by a child agent.",
    "release-ticket": "Filled when this step is executed by a child agent.",
}

STEPS = [
    ("dist-types", "Dist types (Thrift schemas)",
     "Add dist_types Thrift definitions — streaming format, endpoint config, taxonomy config, OAuth endpoint union.",
     "(none)"),
    ("oauth", "OAuth client and endpoint config",
     "Implement OAuth in dist + dist_types — token URL, headers, metadata keys, client, validation.",
     "dist-types"),
    ("taxonomy-deliverer", "Taxonomy deliverer",
     "Build taxonomy deliverer in dist — sync flow, mandatory headers, taxonomy endpoint wiring, tests.",
     "dist-types, oauth"),
    ("streaming-stack", "Streaming stack",
     "Audience ingestion — partner API client, request builder/sender, transposer, record handler, metrics.",
     "dist-types, oauth"),
    ("platform-config", "Platform config (RLG, endpoints, IG, DA)",
     "Platform objects — RLG, endpoints, IG, DA. Plan/runbook by default; live creation only if user asks.",
     "taxonomy-deliverer, streaming-stack"),
    ("argocd-artifacts", "ArgoCD / RLG helm artifacts",
     "ArgoCD helm values for destination RLG — requires platform.rlg_id.",
     "streaming-stack, platform-config"),
    ("redpanda-topics", "Redpanda topics",
     "Topic design; emit artifacts/redpanda-topics.yaml. Live creation only if user explicitly asks.",
     "streaming-stack"),
    ("grafana-dashboards", "Grafana dashboards and alerts",
     "Dashboards and alerts — needs RLG id and metric names from prior steps.",
     "platform-config, streaming-stack, taxonomy-deliverer"),
    ("deploy", "Deploy services",
     "Deploy plan — service matrix, job references, smoke checklist. No triggers unless user asks.",
     "argocd-artifacts, platform-config, redpanda-topics"),
    ("tech-discovery", "Tech Discovery (Confluence)",
     "Confluence Tech Discovery draft for QA — not the test plan.",
     "deploy, grafana-dashboards"),
    ("release-ticket", "Release ticket",
     "Release ticket + PR aggregation. Requires explicit user approval.",
     "deploy"),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", default=SLUG_DEFAULT)
    p.add_argument("--display", default=DISPLAY_DEFAULT)
    args = p.parse_args()
    out = Path("launches") / args.slug / "tasks"
    out.mkdir(parents=True, exist_ok=True)
    for step_id, jira_title, summary, deps in STEPS:
        details = DETAILS[step_id].replace("{slug}", args.slug)
        content = f"""---
step_id: {step_id}
status: {STATUSES[step_id]}
title: "{jira_title}: {args.display}"
---

## Scope

{summary}

## Depends on

{deps}

## Skill

platform/skills/destination-launch/steps/{step_id}/SKILL.md

## Details

{details}
"""
        out.joinpath(f"{step_id}.md").write_text(content)
        print("ok", step_id)


if __name__ == "__main__":
    main()
