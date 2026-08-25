---
step_id: taxonomy-connector-scaffold
status: pending
title: "Taxonomy connector scaffold: Chevrolet"
---

## Scope

Scaffold API taxonomy connector in dist_types + dist — Thrift config, deliverer skeleton, factory wiring, compile-clean hooks. Writes scaffold global context.

## Depends on

(none)

## Skill

platform/skills/destination-launch/steps/taxonomy-connector-scaffold/SKILL.md

## Derived (not asked)

- **Connector name:** `Chevrolet` — derived from `destination.slug` (`chevrolet`) in PascalCase; do not ask the user.

## Questions

```yaml
user_questions:
  - id: dist_types_fields
    prompt: >-
      Which values are fixed for the whole destination account — identifying,
      routing, or naming the targets segments are shared with? These become
      Thrift fields in dist_types.
    type: multi_select
    required: true
    allow_multiple: true
    options:
      - id: oauth_integration_id
        label: "OAuth integration id — include whenever the connector uses OAuth"
      - id: account_id
        label: "Account / seat / manager id — the tenant this endpoint delivers as"
      - id: target_id
        label: "Target id the segments are shared with (advertiser, instance)"
      - id: region
        label: "Region — routes to a base URL"
      - id: country
        label: "Country / marketplace"
      - id: none_other
        label: "None of these — I'll name the fields in chat"
    guidance: |
      Anything constant across one sync() qualifies. Existing connectors carry
      one to three such fields.
      Types: prefer string for ids (even numeric); enum for a closed set you
      control; list<string> for several targets — never a comma-separated
      string, and never a map<string,string> config bag.
      Tick the kinds that apply, then give the partner's actual field name for
      each if it differs from the label.
  - id: dist_fields
    prompt: >-
      Which values live in dist? Java constants, lookups, OAuth metadata, and
      the per-segment keys of the create-segment request body.
    type: multi_select
    required: true
    allow_multiple: true
    options:
      - id: api_url_constant
        label: "Base API URL as a Java constant (single-region partner)"
      - id: region_lookup
        label: "Region to base-URL lookup (multi-region partner)"
      - id: derived_lookup
        label: "Another derived lookup (e.g. country to marketplace id)"
      - id: oauth_metadata
        label: "OAuth handshake metadata (client id, tokens)"
      - id: segment_name
        label: "Segment body: name"
      - id: segment_description
        label: "Segment body: description"
      - id: segment_other
        label: "Segment body: other per-segment keys — I'll name them in chat"
    guidance: |
      Java constant: same for all customers of this partner (application ids,
      API paths, page sizes).
      OAuth metadata: returned by the handshake.
      Segment body: only what genuinely differs per segment. If the partner
      accepts the body verbatim, no POJO is needed.
      Nothing batch-invariant belongs here. Account-level ids rendered into
      every segment body as comma-separated strings are a known anti-pattern
      in older connectors — do not copy it.
  - id: oauth
    prompt: "Does it use OAuth? If yes, which integration — new or existing?"
    type: select
    required: true
    options:
      - id: existing
        label: "Yes — existing OAuth integration"
      - id: new
        label: "Yes — new OAuth flow (adds an OAuthEndpointConfig struct)"
      - id: none
        label: "No OAuth"
    guidance: >-
      Yes adds oauth_integration_id and wires OAuthService.Iface. The value
      acting as the OAuth seat must be a required Thrift field.
  - id: parent_resource
    prompt: >-
      Does the partner require a container/parent resource to exist before
      segments can be created?
    type: select
    required: true
    options:
      - id: "no"
        label: "No — segments are created directly"
      - id: "yes"
        label: "Yes — a container must exist first (generates the batch-scoped hook)"
    guidance: >-
      This is the one structural branch in the generated skeleton. Yes emits
      ensureAccountScopedResources(), which runs once per sync and which
      taxonomy-partner-flow then implements; no omits the method and its call
      site entirely. It is recorded as taxonomy.hooks.ensure_account_scoped_generated.
```

## Details

Filled when this step is executed by a child agent.
