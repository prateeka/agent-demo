---
name: destination-launch-taxonomy-partner-flow
description: Partner taxonomy resource chain in scaffold hooks; segment-body JSON contract for UI.
---

# Step: taxonomy-partner-flow

Implements the **partner-specific resource chain** inside hooks emitted by **`taxonomy-connector-scaffold`**, and defines the **per-segment JSON contract** for the UI step.

**Skill dependency:** **`taxonomy-connector-scaffold`** — do not run until scaffold task is `done` and its `global_keys` are merged into `epic.md`. (Also stated in execution spec below.)

## Repos

`dist`, `dist_types` — run `./scripts/resolve-repos.sh` (requires `LAUNCHPAD_DIST`, `LAUNCHPAD_DIST_TYPES`).

## Detect prior work

1. Read `launches/{slug}/tasks/taxonomy-partner-flow.md`.
2. If `## Details` is not the stub sentinel — diff repo against recorded paths; ask resume or redo.
3. If any property in execution spec **Properties read from global context** is missing from `epic.md`, stop and re-run **`taxonomy-connector-scaffold`** (per execution spec).

## Read first — exact global keys

Read `epic.md` → `## Global context`. **Read; never re-derive** — per execution spec **Properties read from global context**.

| Execution spec property | epic.md path |
| --- | --- |
| `{{Connector}}` | `taxonomy.connector.name` |
| `{{connector_snake}}` | `taxonomy.connector.snake` |
| `{{connectorCamel}}` | `taxonomy.connector.camel` |
| `{{CONNECTOR_UPPER}}` | `taxonomy.connector.upper` |
| `{{tenant_id_field}}` / `{{tenantIdField}}` / `{{TENANT_UPPER}}` | `taxonomy.tenant_id_field` / `.tenant_id_field_camel` / `.tenant_id_field_upper` |
| Thrift config field list | `taxonomy.thrift.config_fields` |
| Segment body keys | `taxonomy.segment_body.keys` |
| Deliverer FQCN | `taxonomy.deliverer_fqcn` |
| Handler FQCN | `taxonomy.handler_fqcn` |
| Constants FQCN | `taxonomy.constants_fqcn` |
| Batch-scoped hook generated? | `taxonomy.hooks.ensure_account_scoped_generated` |
| Stored-override block generated? | `taxonomy.hooks.stored_override_generated` |

Also: `release.ticket_id`

## Ask the user

**Do not invent questions here.** Use the **five questions** in execution spec **Step 1 — Define the segment-body JSON properties**.

## Write to step task (local)

Update `launches/{slug}/tasks/taxonomy-partner-flow.md`:

- Partner API reference, segment-body property table, generated file paths, compile output, Step 3 checklist results
- Frontmatter `status`: `in_progress` while working; `done` when Definition of done met
- PR link; PR title `[{release.ticket_id}] ...`

## Return global keys (orchestrator merges)

Do **not** edit `epic.md`. Return the segment-body contract per execution spec **Write the property list to global context** (Step 1). Do not duplicate Thrift config fields from scaffold.

| Execution spec field | epic.md path |
| --- | --- |
| Property name | `segment_body.properties[].name` |
| Type | `segment_body.properties[].type` |
| Required | `segment_body.properties[].required` |
| Allowed values (if closed set) | `segment_body.properties[].allowed_values` |
| Partner field name | `segment_body.properties[].partner_field` |
| `segment_body_format` template | `segment_body.template` |

```yaml
global_keys:
  segment_body.properties:
    - name: ...
      type: ...
      required: ...
      # allowed_values, partner_field when applicable
  segment_body.template: |
    ...
```

## Definition of done

- Execution spec **Step 3 — Checklist** satisfied
- `./gradlew :taxonomy_service:compileJava` clean from `java/`
- Full `segment_body.properties` and `segment_body.template` returned in `global_keys`

## Verification

- `./gradlew :taxonomy_service:compileJava` from `java/`
- Per execution spec: `payload.validate()` first in per-segment hook; no property in both `taxonomy.thrift.config_fields` and `segment_body.properties`

---

## Execution spec
# taxonomy-partner-flow

**Skill name:** `taxonomy-partner-flow` — implements the partner-specific resource chain inside the hooks that
`taxonomy-connector-scaffold` emitted, and defines the per-segment JSON contract.

> **Dependency: `taxonomy-partner-flow` depends on `taxonomy-connector-scaffold`.**
> Do not run this skill until `taxonomy-connector-scaffold` has produced the Thrift struct, the deliverer skeleton, the
> constants class and the `TaxonomyToolsFactory` case. This skill never restructures that output — it fills in the two
> hooks and adds the request/response plumbing they need.

**Downstream consumer:** the UI taxonomy-creation step. It needs the segment-body JSON property list this skill
produces **plus** the global properties written by `taxonomy-connector-scaffold`. Both sets must live in global context by
the time this skill finishes.

## Scope

Applies to the same family as `taxonomy-connector-scaffold`: API-based taxonomy connectors for streaming destinations
under `java/s2s_data_syncer/.../handler/integration/`. Batch/file deliverers are out of scope.

What this skill generates:

1. The **segment-body JSON contract** — property names, types, required/optional, and the Gson POJO that mirrors it.
2. The **resource-chain skeleton** — a generic, ordered `ensure`/`create`/`verify` pipeline inside the two hooks, with
   idempotency, existence checks and per-step error attribution already wired.
3. The **partner request/response model classes and handler stubs** the chain calls.
4. The **global-context write-back** of the JSON property list for the UI step.

What it does not generate: HTTP calls, auth headers, retry policy, or anything already owned by
`{{Connector}}ApiServiceHandler` / `ApiServiceFactory`. It calls those; it does not reimplement them.

**Hard requirement (inherited):** everything generated must compile as emitted. Unimplemented partner calls throw
`UnsupportedOperationException`, every referenced symbol is imported, and every handler method the chain calls exists —
generate a stub on the handler if it does not. `./gradlew :taxonomy_service:compileJava` must be clean immediately after
generation.

**Not used:** JRuby macros. Values come from Thrift fields, the segment body JSON, OAuth metadata, or a Java lookup.

---

## Properties read from global context

These were written by `taxonomy-connector-scaffold`. **Read them; never re-derive them.** Re-deriving a name is how the
generated class ends up in a package the scaffold did not create.

| Property | Used for |
| --- | --- |
| `{{Connector}}`, `{{connector_snake}}`, `{{connectorCamel}}`, `{{CONNECTOR_UPPER}}` | class, package and enum names |
| `{{tenant_id_field}}` / `{{tenantIdField}}` / `{{TENANT_UPPER}}` | the account-scoped id the chain authenticates against |
| Thrift config field list | which values the hooks can read from a field instead of a parameter |
| Segment body keys | starting point for Step 1 below — extend, do not replace |
| Deliverer FQCN | file to edit |
| Handler FQCN | class to add stub methods to |
| Constants FQCN | where new lookups and application ids go |
| Whether the batch-scoped hook was generated | if `false`, do not invent `ensureAccountScopedResources()` — put everything in the per-segment hook |
| Whether the stored-override block was generated | if `true`, the per-segment hook may be skipped entirely for a field, so it must not be the only place a required resource is ensured |

If any of these is missing from global context, stop and re-run `taxonomy-connector-scaffold` rather than guessing.

---

## Step 1 — Define the segment-body JSON properties

### The rule to print for the developer

> **`taxonomy-connector-scaffold` already answered "where does this value live." This step only names and types the
> values that landed in the segment body.**
>
> A property belongs here only if it **differs between segments within a single sync**. If it is the same for every
> segment, it is a Thrift field — go back to `taxonomy-connector-scaffold`, do not add it here.
>
> | Property kind | Example | Name it | Type |
> | --- | --- | --- | --- |
> | Human-facing label the partner shows | segment name | `name` | `string`, required |
> | Free text | segment description | `description` | `string`, optional |
> | Bounded flag/policy the partner defines | id retention window | `idRetention` | `string` from a fixed set, required if the partner requires it |
> | Numeric per-segment setting | ttl days, cap | `ttlDays` | number, optional |
> | Boolean per-segment toggle | `isRealtime` | `isRealtime` | boolean, optional |
>
> Naming rules:
>
> - Use the **partner's own field name** verbatim when the value maps 1:1 onto a partner request field. A rename here
>   becomes a translation layer for every future reader.
> - `lowerCamelCase`, matching the partner's JSON. Do not snake_case body keys — the body is partner-shaped, unlike
>   Thrift which is `snake_case`.
> - No prefixes: `name`, not `segmentName` or `{{connectorCamel}}Name`.
> - No ids of things the account owns (advertiser, instance, seat, container). Those are batch-invariant by definition.
>
> Type rules:
>
> - Everything arrives as JSON text and is Gson-parsed. Prefer `string` for anything the partner treats as an opaque
>   token, including numeric ids.
> - Use a real `boolean`/number only when the partner's API rejects the string form.
> - Use a JSON **array** when the partner accepts several values for one segment. Never a comma-separated string —
>   that is the known account-level-ids-in-the-body defect, and it should not be in the body at all.
> - Required vs optional: required means the partner's create call fails without it. Optional values must be guarded
>   with a blank check before being set on the request, not defaulted to `""`.

### Questions to ask

1. **What does the partner's create-segment request require, field by field?** (Paste or link the API reference.)
2. **Which of those vary per segment?** Everything else is already a Thrift field — confirm against global context.
3. **Which are optional, and what does the partner do when they are omitted?** (Omit vs. send empty differ.)
4. **Any closed-set values?** (retention windows, segment types) — these become a constant set plus a validation
   precondition, not free strings.
5. **Any per-segment value that is a list?** — becomes a JSON array plus a `List<String>` field.

### Output of this step

The `segment_body_format` template:

```json
{
  "name": "<segment name>",
  "description": "<optional description>",
  "idRetention": "<retention window>"
}
```

And the matching POJO, replacing the `SegmentPayload` stub the scaffold emitted. Field names must match the keys exactly
— Gson binds by name, and a mismatch fails silently as `null` at runtime rather than at compile time.

```java
  /** Gson-deserialized shape of segment_body_format. Names must match the template keys exactly. */
  static final class SegmentPayload {
    String name;
    String description;   // optional
    String idRetention;   // required, closed set

    void validate() {
      Preconditions.checkArgument(StringUtils.isNotBlank(name), "segment body: name is required");
      Preconditions.checkArgument(StringUtils.isNotBlank(idRetention), "segment body: idRetention is required");
      Preconditions.checkArgument(SUPPORTED_ID_RETENTIONS.contains(idRetention),
          "segment body: unsupported idRetention: %s", idRetention);
    }
  }
```

Call `payload.validate()` as the first statement of the per-segment hook. A malformed body must fail that one field with
a clear message, not throw a `NullPointerException` from three calls deeper.

### Write the property list to global context

**Mandatory — the UI taxonomy-creation step consumes this.** For each property emit:

| Key | Value | Why the UI needs it |
| --- | --- | --- |
| `segment_body.properties[].name` | `idRetention` | form field key |
| `segment_body.properties[].type` | `string` / `number` / `boolean` / `array<string>` | input widget |
| `segment_body.properties[].required` | `true` / `false` | validation |
| `segment_body.properties[].allowed_values` | `["1_YEAR","2_YEARS"]` or absent | dropdown vs. free text |
| `segment_body.properties[].partner_field` | partner's field name | mapping documentation |
| `segment_body.template` | the JSON above | the `segment_body_format` to persist on the endpoint |

The UI step reads this list **together with** the `taxonomy-connector-scaffold` global properties (connector name, Thrift
config field list, tenant id field). Neither set alone is sufficient: the scaffold properties render the
endpoint/destination form, this list renders the per-segment form. Do not duplicate a value into both — a property that
appears in the Thrift config field list must not appear here.

---

## Step 2 — Generate the resource chain

Print this model before generating:

> Partner taxonomy setup is almost always a **chain of resources**, each depending on the previous one:
>
> | Shape | Account-scoped, once per sync | Per segment |
> | --- | --- | --- |
> | Container-first partners | a parent container (workspace, parent audience) | the segment plus its dependent resources (dataset, sharing rules) |
> | Flat partners | — | a single segment-equivalent object (DMP segment, customer list, user list) |
>
> Split the chain by the same batch-invariance test used for config: a resource whose identity does not depend on the
> segment goes in `ensureAccountScopedResources()`; everything else goes in `createOrVerifySegment(...)`.

### 2a. Account-scoped hook

Only if global context says the batch-scoped hook was generated. Replace the `UnsupportedOperationException` body.

```java
  /**
   * Ensures the account-scoped parent resource exists. Runs once per sync. Idempotent: it runs on
   * every sync, including syncs where nothing changed.
   */
  private void ensureAccountScopedResources() throws Exception {
    LOG.info("Ensuring account-scoped resources: {{tenantIdField}}={}", {{tenantIdField}});
    // Prefer an idempotent create over exists-then-create: one call, no race between the two.
    // Many partners return 201 for both new and existing on the container POST.
    apiService.createParentResourceIdempotent();
    LOG.info("Account-scoped resources ready: {{tenantIdField}}={}", {{tenantIdField}});
  }
```

Rules:

- Prefer an idempotent create. Fall back to `exists()` then `create()` only when the partner's create is not idempotent,
  and log which branch was taken.
- Take no arguments and read no per-segment state. If it needs a value it does not have, that value is batch-invariant
  and belongs in the Thrift config — go back to `taxonomy-connector-scaffold`.
- Throw on failure. The scaffold's `sync()` already attributes the failure to every field.
- Never call it from inside the per-field loop.

### 2b. Per-segment hook

```java
  /**
   * Creates the segment on the partner platform (or finds an equivalent one) and returns the
   * platform id persisted as the override. Idempotent: a retried sync must not create duplicates.
   */
  private String createOrVerifySegment(String bearerToken, SegmentPayload payload, String fieldContext)
      throws Exception {
    payload.validate();

    // Step 1 — the primary resource. Look up before create where the partner supports it, so a
    // retry after a partially failed sync converges instead of duplicating.
    String segmentId = apiService.findSegmentIdByName(payload.name);
    if (segmentId != null) {
      LOG.info("Found existing segment, skipping create: segmentId={}, {}", segmentId, fieldContext);
    } else {
      segmentId = apiService.createSegment(buildCreateSegmentRequest(payload));
      LOG.info("Created segment: segmentId={}, {}", segmentId, fieldContext);
    }

    // Step 2..N — dependent resources. Each is ensured, not blindly created. A failure here throws:
    // the segment exists but is unusable, so the field must be reported failed and retried.
    ensureDependentResources(segmentId, payload, fieldContext);

    return segmentId;
  }

  /**
   * Ensures every resource that hangs off the segment (e.g. sharing rules per target account or
   * instance). Idempotent per resource: check existence, then create only what is missing.
   *
   * TODO: implement per partner. Delete this method if the partner has no dependent resources.
   */
  private void ensureDependentResources(String segmentId, SegmentPayload payload, String fieldContext)
      throws Exception {
    throw new UnsupportedOperationException("ensureDependentResources not implemented");
  }

  /** TODO: map SegmentPayload plus Thrift config fields onto the partner's create request. */
  private {{Connector}}CreateSegmentRequest buildCreateSegmentRequest(SegmentPayload payload) {
    throw new UnsupportedOperationException("buildCreateSegmentRequest not implemented");
  }
```

Rules for the fan-out inside `ensureDependentResources`:

- One target per iteration, each with its own existence check, so a partial failure leaves the rest intact.
- Accumulate messages across targets and throw once at the end with all of them. Failing on the first target hides the
  other problems for a whole sync cycle.
- A dependent resource that is optional for the partner (no targets configured) logs a skip and continues; it does not
  fail the field.
- Every target list comes from a Thrift `list<string>` field, never from a comma-separated body string.

### 2c. Handler stubs and models

For each partner call above, add to `{{Connector}}ApiServiceHandler` (FQCN from global context) a method that compiles:

```java
  public String createSegment({{Connector}}CreateSegmentRequest request) throws Exception {
    throw new UnsupportedOperationException("createSegment not implemented");
  }

  public String findSegmentIdByName(String name) throws Exception {
    throw new UnsupportedOperationException("findSegmentIdByName not implemented");
  }

  public boolean dependentResourceExists(String segmentId, String targetId) throws Exception {
    throw new UnsupportedOperationException("dependentResourceExists not implemented");
  }
```

Generate one plain request class per partner call, in the handler's package, fields matching the partner's JSON, no
logic. Closed-set values and application ids (audience-type enums, product identifiers) go in
`{{Connector}}Constants`, not inline.

### 2d. Test additions

Extend `Test{{Connector}}TaxonomyDeliverer` (created by `taxonomy-connector-scaffold`) using the package-private
constructor and a stubbed handler:

- A body missing a required property fails that field with a message naming the property; other fields still succeed.
- An out-of-set closed value fails validation before any partner call is made.
- `findSegmentIdByName` returning a value skips `createSegment` and returns the found id.
- A dependent-resource failure fails the field even though the segment was created.
- Multiple targets: one failing target still attempts the others, and the thrown message names every failure.
- No-targets case logs a skip and succeeds.

---

## Step 3 — Checklist to print

- [ ] Every global property was read from context, not re-derived.
- [ ] No property appears both in the Thrift config field list and the segment body property list.
- [ ] Body keys are `lowerCamelCase` and match the partner's own field names.
- [ ] `SegmentPayload` field names match the `segment_body_format` keys exactly.
- [ ] `payload.validate()` is the first statement of the per-segment hook.
- [ ] Lists are JSON arrays, never comma-separated strings.
- [ ] Every partner create is idempotent, or is preceded by an existence check.
- [ ] The account-scoped hook takes no arguments and is never called from the per-field loop.
- [ ] Dependent-resource failures accumulate and throw once, naming every failed target.
- [ ] Hooks throw on failure; nothing returns `null` to signal an error.
- [ ] `sync()` was not restructured, hook signatures unchanged, token fetch still outside the loop.
- [ ] Every handler method called exists; unimplemented ones throw `UnsupportedOperationException`.
- [ ] **Generated code compiles as emitted** — verify with `./gradlew :taxonomy_service:compileJava` from `java/`.
- [ ] The full segment-body property list (name, type, required, allowed values, partner field) and the template are
      written to global context for the UI taxonomy-creation step.

## Smells to flag if seen

- A segment-body property that is identical for every segment → Thrift field, back to `taxonomy-connector-scaffold`.
- A comma-separated string standing in for a list.
- A create call with no existence check and no idempotency guarantee → duplicates on every retry.
- `ensureAccountScopedResources()` reading anything derived from a `ResolvedTaxonomyField`.
- The per-segment hook being the only place a required parent resource is ensured, when the stored-override block can
  skip that hook entirely.
- A `catch` inside a hook that returns `null` or an empty id instead of throwing.
- Application ids, marketplace ids or retention sets inlined as string literals instead of living in
  `{{Connector}}Constants`.
- A body property renamed away from the partner's own field name.
- Segment-body properties defined here but never written to global context — the UI step will silently miss them.
