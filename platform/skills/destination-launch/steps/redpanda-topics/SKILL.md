---
name: destination-launch-redpanda-topics
description: Redpanda topic design — emit YAML artifact; live creation only if user asks.
---

# Step: redpanda-topics

Design Redpanda/Kafka topics for the destination.

**Default:** emit `launches/{slug}/artifacts/redpanda-topics.yaml` — do **not** create live topics unless user explicitly asks.

## Read first — exact global keys

- `destination.slug`, `streaming.api_base_urls` (if set)

## Ask the user

- Publisher / consumer cluster?
- Topic names, partitions, retention?
- Live creation now, or YAML only?

## Internal sub-steps

1. Cluster layout (publisher vs consumer)
2. Topic naming for destination
3. Partition / retention rationale
4. **Generate** `artifacts/redpanda-topics.yaml` from global context

## Write to step task (local)

- Topic spec summary, artifact path, creation commands if user asked for live apply

## Return global keys (orchestrator merges)

- `redpanda.publisher_cluster`, `redpanda.consumer_cluster`, `redpanda.topics`

## Definition of done

- **YAML emitted** to `artifacts/redpanda-topics.yaml` and recorded on task file
- Live topics: only if user explicitly requested — document verification on task

## Example artifact

Emit to `launches/{slug}/artifacts/redpanda-topics.yaml` (see `_template/` layout).
