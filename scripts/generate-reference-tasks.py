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
    "release-ticket": "done",
    "taxonomy-connector-scaffold": "done",
    "taxonomy-partner-flow": "done",
    "taxonomy-ui": "done",
    "rlg-addition": "done",
    "oauth": "done",
    "oauth-db-update": "done",
    "partner-api-client": "done",
    "request-builder-sender": "done",
    "transposer-record-handler": "done",
    "delivery-endpoints-ui": "done",
    "ig-ui": "pending",
    "da-ui": "pending",
    "redpanda-topics": "done",
    "grafana-dashboards": "pending",
    "tech-discovery": "pending",
}

DETAILS = {
    "release-ticket": "Filled when this step is executed by a child agent.",
    "taxonomy-connector-scaffold": "Filled when this step is executed by a child agent.",
    "taxonomy-partner-flow": "Filled when this step is executed by a child agent.",
    "taxonomy-ui": "Filled when this step is executed by a child agent.",
    "rlg-addition": "Filled when this step is executed by a child agent.",
    "oauth": "Filled when this step is executed by a child agent.",
    "oauth-db-update": "Filled when this step is executed by a child agent.",
    "partner-api-client": "Filled when this step is executed by a child agent.",
    "request-builder-sender": "Filled when this step is executed by a child agent.",
    "transposer-record-handler": "Filled when this step is executed by a child agent.",
    "delivery-endpoints-ui": "Filled when this step is executed by a child agent.",
    "ig-ui": "Filled when this step is executed by a child agent.",
    "da-ui": "Filled when this step is executed by a child agent.",
    "redpanda-topics": "Emit launches/{slug}/artifacts/redpanda-topics.yaml when run.",
    "grafana-dashboards": "Filled when this step is executed by a child agent.",
    "tech-discovery": "Filled when this step is executed by a child agent.",
}

STEPS = [
    ("release-ticket", "Release ticket",
     "Record Release ticket id (files only — no Jira API); PRs reference release.ticket_id.",
     "(none)"),
    ("taxonomy-connector-scaffold", "Taxonomy connector scaffold",
     "Scaffold API taxonomy connector in dist_types + dist — Thrift, deliverer skeleton, factory wiring.",
     "(none)"),
    ("taxonomy-partner-flow", "Taxonomy partner flow",
     "Partner resource chain in scaffold hooks; segment-body JSON contract for taxonomy-ui.",
     "taxonomy-connector-scaffold"),
    ("taxonomy-ui", "Taxonomy endpoints (UI)",
     "Create taxonomy endpoints via UI. Textual runbook today; REST API later.",
     "taxonomy-connector-scaffold, taxonomy-partner-flow"),
    ("rlg-addition", "RLG (DB addition)",
     "Add RLG record in platform DB. Runbook/SQL today; API when platform ships it.",
     "release-ticket"),
    ("partner-api-client", "Partner API client",
     "Partner API client and constants in dist — base URLs, auth wiring.",
     "oauth"),
    ("request-builder-sender", "Request builder and sender",
     "Request builder and request sender in dist — payload shape, send path, tests.",
     "partner-api-client"),
    ("transposer-record-handler", "Transposer, record handler, field selector",
     "Transposer, record handler, field selector, config wiring, metrics.",
     "request-builder-sender"),
    ("redpanda-topics", "Redpanda topics",
     "Topic design; emit artifacts/redpanda-topics.yaml. Live creation only if user explicitly asks.",
     "transposer-record-handler"),
    ("oauth", "OAuth client and endpoint config",
     "Implement OAuth in dist + dist_types — token URL, headers, metadata keys, client, validation.",
     "(none)"),
    ("oauth-db-update", "OAuth (DB update)",
     "Add or update OAuth integration record in platform DB. Runbook/SQL today; API when platform ships it.",
     "oauth"),
    ("delivery-endpoints-ui", "Delivery endpoints (UI)",
     "Create delivery endpoints via UI. Textual runbook today; REST API later.",
     "rlg-addition, oauth-db-update"),
    ("ig-ui", "Integration group (UI)",
     "Create IG via UI. Textual runbook today; REST API later.",
     "delivery-endpoints-ui, taxonomy-ui"),
    ("da-ui", "Destination account (UI)",
     "Create DA via UI. Textual runbook today; REST API later.",
     "ig-ui"),
    ("grafana-dashboards", "Grafana dashboards and alerts",
     "Dashboards and alerts — needs RLG id and metric names from prior steps.",
     "rlg-addition, transposer-record-handler, taxonomy-partner-flow"),
    ("tech-discovery", "Tech Discovery (Confluence)",
     "Confluence Tech Discovery draft for QA — not the test plan.",
     "grafana-dashboards, transposer-record-handler"),
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
