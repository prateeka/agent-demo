---
name: destination-launch-grafana-dashboards
description: Grafana dashboards and alerts from RLG id and metric keys in epic.md.
---

# Step: grafana-dashboards

Create **Grafana dashboards and alerts** for the new destination.

## Read first — exact global keys

- `release.ticket_id`
- `platform.rlg_id`
- `grafana.metrics.streaming`, `grafana.metrics.taxonomy`

## Grafana MCP rules (when available)

- `get_dashboard_summary`, `patch_dashboard`, `generate_deeplink`

## Write to step task (local)

- Dashboard / alert URLs, panel list, verification

## Return global keys (orchestrator merges)

- `grafana.dashboard_urls`, `grafana.alert_rule_urls`

## Definition of done

- Dashboards/alerts created or documented; URLs on task file

## Typical panels

1. API latency (p50/p90/p99) by RLG
2. Error rate / 401 / 429
3. Delivery throughput
4. Taxonomy sync attempts
5. Kafka consumer lag for destination RLG
