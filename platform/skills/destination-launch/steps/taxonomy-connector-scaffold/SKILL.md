---
name: destination-launch-taxonomy-connector-scaffold
description: Scaffolds API taxonomy connector in dist_types and dist — Thrift, deliverer skeleton, factory wiring.
---

# Step: taxonomy-connector-scaffold

Scaffolds a new **API-based taxonomy connector** across `dist_types` and `dist`. Downstream **`taxonomy-partner-flow`** implements the partner hooks this step emits.

**Skill dependency:** none — this step does not depend on `taxonomy-partner-flow`. (Also stated in execution spec below.)

## Repos

`dist`, `dist_types` — run `./scripts/resolve-repos.sh` (requires `LAUNCHPAD_DIST`, `LAUNCHPAD_DIST_TYPES`).

## Detect prior work

1. Read `launches/{slug}/tasks/taxonomy-connector-scaffold.md`.
2. If `## Details` is not the stub sentinel — diff repo against recorded paths; ask resume or redo.
3. Do not re-apply destructive changes without checking prior state.

## Read first — exact global keys

Read `launches/{slug}/epic.md` → `## Global context`:

- `release.ticket_id`
- `destination.slug`, `destination.api_family`
- `oauth.type`, `oauth.metadata_keys`
- `thrift.oauth_endpoint_config`
- `thrift.taxonomy_config` (if set by `dist-types`)

## Ask the user

**Do not invent questions here.** Use the **five questions** in execution spec **Step 1** (after the batch-invariance rule). Those drive Thrift fields, hook generation, and segment-body keys.

## Write to step task (local)

Update `launches/{slug}/tasks/taxonomy-connector-scaffold.md`:

- Step 1 answers, generated file paths, compile output, Step 4 checklist results
- Frontmatter `status`: `in_progress` while working; `done` when Definition of done met
- PR link; PR title `[{release.ticket_id}] ...`

## Return global keys (orchestrator merges)

Do **not** edit `epic.md`. Return every property in execution spec **Shared properties — move these to global context**, using the epic.md paths below. Values come from Step 1 answers and generated code — **no baked-in example connector**.

| Execution spec property | epic.md path |
| --- | --- |
| `{{Connector}}` | `taxonomy.connector.name` |
| `{{connector_snake}}` | `taxonomy.connector.snake` |
| `{{connectorCamel}}` | `taxonomy.connector.camel` |
| `{{CONNECTOR_UPPER}}` | `taxonomy.connector.upper` |
| `{{tenant_id_field}}` | `taxonomy.tenant_id_field` |
| `{{tenantIdField}}` | `taxonomy.tenant_id_field_camel` |
| `{{TENANT_UPPER}}` | `taxonomy.tenant_id_field_upper` |
| `{{partner}}` | `taxonomy.partner` |
| `{{NEXT_TAG}}` | `taxonomy.thrift.next_tag` |
| `{{NEXT_OAUTH_TAG}}` | `taxonomy.thrift.next_oauth_tag` |
| Thrift config field list | `taxonomy.thrift.config_fields` |
| Segment body keys (question 5) | `taxonomy.segment_body.keys` |
| Batch-scoped hook generated? | `taxonomy.hooks.ensure_account_scoped_generated` |
| Stored-override block generated? | `taxonomy.hooks.stored_override_generated` |
| Deliverer FQCN | `taxonomy.deliverer_fqcn` |
| Handler FQCN | `taxonomy.handler_fqcn` |
| Constants FQCN | `taxonomy.constants_fqcn` |

```yaml
global_keys:
  taxonomy.connector.name: ...
  # one entry per row above — values from this run, not placeholders
```

**Partitioning (from execution spec):** Thrift config fields and the two hook booleans live here only. Per-segment JSON properties and `segment_body.template` are written by **`taxonomy-partner-flow`**. Do not duplicate a value in both sets.

## Definition of done

- Execution spec **Step 4 — Final checklist** satisfied
- `./gradlew :taxonomy_service:compileJava` clean from `java/`
- Every row in the mapping table returned in `global_keys`

## Verification

- `./gradlew :taxonomy_service:compileJava` from `java/`
- Per execution spec hard requirement: compile-clean output, hooks throw `UnsupportedOperationException` until implemented

---

## Execution spec
# taxonomy-connector-scaffold

**Skill name:** `taxonomy-connector-scaffold` — scaffolds a new taxonomy connector across `dist_types` and `dist`.

**Downstream skill:** `taxonomy-partner-flow` — implements the partner-specific resource chain in the hooks this skill
emits. It depends on `taxonomy-connector-scaffold`; this skill depends on nothing.

## Scope

Applies to **API-based taxonomy connectors for streaming destinations** — destinations that have (or will have) an integration under
`java/s2s_data_syncer/src/main/java/com/liveramp/streaming_deliverer/handler/integration/`.
Current members of this family with a taxonomy deliverer: `amazon_dm`, `criteo`, `doubleclick`, `facebook`,
`google_customer_match`, `linkedin`, `pinterest`, `ttd`, `twitter`.

**Does not apply to** batch/file taxonomy deliverers (S3, SFTP, FTP, GCS, email, Netflix, IndexExchange). Those take
`FileOperator` + `BatchDelivererService` and generate files instead of calling a segment-creation API — different skeleton entirely.

The skill does four things, in order:

1. Ask five questions to decide which values belong in `dist_types` (Thrift) vs. elsewhere.
2. Generate the `dist_types` struct + union tag.
3. Generate the shared `dist` boilerplate: constants/lookup class, deliverer skeleton, `TaxonomyToolsFactory` case, `main()` test harness, unit test skeleton.
4. Print a checklist, and hand off the partner-specific API calls to `taxonomy-partner-flow` (see the last section).

**Out of scope (never generate):** the destination-specific API calls. For Amazon DM that is the dataroom / dataset /
sharing-rule sequence; for Pinterest it is the customer-list name-fallback chain. The skill generates the sequencing,
error accumulation and idempotency scaffolding around those calls, and leaves two hook methods for the developer to
implement — one batch-scoped, one per-segment.

**Hard requirement:** everything generated must compile as emitted. Unimplemented hooks throw
`UnsupportedOperationException` rather than being left as empty bodies or bare comments, all referenced symbols are
imported, and any partner client the deliverer calls is either already present or generated as a stub alongside it. A
developer should be able to run `./gradlew :taxonomy_service:compileJava` immediately after generation and get a clean
build.

**Not used:** JRuby macros. All dynamic values come from literal Thrift fields, the segment body JSON, OAuth metadata,
or a Java lookup table in `dist`. Do not propose macro-based population.

---

## Shared properties — move these to global context

**When this skill's contents are pasted into the host project, the properties below must be lifted into the host's
global context rather than kept local to this skill.** The downstream `taxonomy-partner-flow` skill resolves the same
identifiers, and if each skill keeps its own copy they will drift — `taxonomy-partner-flow` will generate a class name or package
path that does not match what this skill emitted.

Promote to global context:

| Property | Example | Derived from |
| --- | --- | --- |
| `{{Connector}}` | `AcmeDsp` | question 1 |
| `{{connector_snake}}` | `acme_dsp` | `{{Connector}}` |
| `{{connectorCamel}}` | `acmeDsp` | `{{Connector}}` |
| `{{CONNECTOR_UPPER}}` | `ACME_DSP` | `{{Connector}}` |
| `{{tenant_id_field}}` / `{{tenantIdField}}` / `{{TENANT_UPPER}}` | `seat_id` / `seatId` / `SEAT_ID` | question 2 |
| `{{partner}}` | `acmedsp` | partner API hostname |
| `{{NEXT_TAG}}`, `{{NEXT_OAUTH_TAG}}` | `53`, `13` | next free union tag at generation time |
| Thrift config field list | `oauth_integration_id`, `seat_id`, `region` | questions 2–4 |
| Segment body keys | `name`, `description` | question 5 |
| Whether the batch-scoped hook was generated | `true` / `false` | question 4 |
| Whether the stored-override block was generated | `true` / `false` | developer answer in 3b |
| Deliverer FQCN | `com.liveramp.taxonomy_service.deliverer.acme_dsp.AcmeDspTaxonomyDeliverer` | derived |
| Handler FQCN | `com.liveramp.partner_apis.clients.acme_dsp.AcmeDspApiServiceHandler` | derived |
| Constants FQCN | `com.liveramp.partner_apis.clients.acme_dsp.AcmeDspConstants` | derived |

The two booleans matter most: `taxonomy-partner-flow` needs them to know whether
`ensureAccountScopedResources()` exists to be implemented and whether its per-segment hook may be short-circuited by a
stored id.

**This table is only the first half of the global contract.** `taxonomy-partner-flow` writes a second set — the
segment-body JSON property list (name, type, required, allowed values, partner field) plus the `segment_body_format`
template. The later UI taxonomy-creation step reads **both** sets: the properties above render the endpoint/destination
form, the segment-body list renders the per-segment form. So do not treat this skill's write as complete on its own, and
do not let a value appear in both sets — anything in the Thrift config field list must not also appear as a segment-body
property.

Keep local to this skill (not global): the Thrift/Java templates themselves, the Step 1 decision rule, and the
checklist.

---

## Step 1 — The only rule the developer needs

Print this and nothing more elaborate:

> **One question decides it: does this value differ between segments within a single sync?**
>
> If **no**, it belongs in `dist_types` (Thrift). If **yes**, it belongs in the segment body.
>
> | If the value... | It goes in |
> | --- | --- |
> | is the same for every segment in the sync (account/seat/manager id, advertiser id, AMC instance id, region, country) | **`dist_types` Thrift field** |
> | genuinely differs per segment (segment name, description, retention flag) | **segment body JSON** (`segment_body_format`), parsed in `dist` |
> | comes back from the OAuth handshake (client id, tokens, account metadata) | **OAuth metadata**, read in `dist` |
> | is derivable from another field (region → base URL, country → marketplace id) | **Java lookup in `dist`** |
> | is the same for all customers of this partner (application ids, API paths, page sizes) | **Java constant in `dist`** |
>
> **Why the test is batch-invariance and not "does it feel like account identity."** `TaxonomyJoblet` loads exactly one
> `TaxonomyExchangeConfig` per `taxonomy_endpoint_id` and hands every field of that request to one deliverer instance, so
> anything scoped to the endpoint is constant across the whole `sync()`. `segment_body_format` is *also* a single
> per-endpoint template, so putting an endpoint-level constant in the body does not buy per-segment flexibility — it just
> renders the same value into N identical payloads as an untyped string that gets re-parsed and re-validated on every
> field. Thrift gives you one constructor-time validation and a real type.
>
> Existing examples: `NewLinkedInTaxonomyConfig` has one field (`oauth_integration_id`),
> `PinterestTaxonomyConfig` has two (`advertiser_id`, `oauth_integration_id`), `AmazonDataManagerTaxonomyConfig` has
> three (`oauth_integration_id`, `region`, `manager_account_id`).
>
> **Known deviation — do not copy it.** `AmazonDataManagerTaxonomyConfig` reads `advertiserAccountIds`,
> `amcInstanceIds` and `countryCode` out of the segment body as comma-separated strings, even though all three are
> constant per endpoint. By the rule above they should be Thrift fields (`list<string>` if multi-target support is
> wanted). Treat this as debt to migrate, not a pattern. Only `name`, `description` and `idRetention` are legitimately
> per-segment there.
>
> The one real argument for the body is release cost: editing a template is a config change, while a new Thrift field is
> a `dist_types` release plus a coordinated `dist` deploy. That is a one-time cost — pay it.

Then ask **five questions** (no more):

1. **Connector name?** (e.g. `AcmeDsp`) — drives struct name, package, class names.
2. **Which values are fixed for the whole destination account — identifying, routing, or naming the targets segments are shared with?** (e.g. advertiser / seat / manager account id, instance id, region, country) — all of these become Thrift fields.
3. **Does it use OAuth?** If yes, which OAuth integration — new or existing? (yes → adds `oauth_integration_id` and wires `OAuthService.Iface`)
4. **Does the partner require a container/parent resource to exist before segments can be created?** (Amazon DM: a dataroom. LinkedIn, Pinterest: nothing.) If yes → generate the batch-scoped hook in 3b; if no → omit it.
5. **What varies per segment in the partner's create-segment request body?** The answer becomes the `segment_body_format`
   template plus a Gson POJO. If the partner accepts the body verbatim, the deliverer can pass
   `get_resolved_segment_body()` straight through (see `NewLinkedInTaxonomyDeliverer`) and no POJO is needed.

Type guidance, stated briefly:

- Prefer `string` for ids, even numeric ones — partner ids overflow and change format. Parse to `long`/`int` in the deliverer constructor.
- Use an **enum** for a closed set you control (region). Use `string` only if the partner may add values without warning.
- `required` if every call fails without it. `optional` with a default if the partner documents a default. Never `required` for a feature only some customers use.
- Never add a `map<string,string>` of freeform config. Name each value as its own typed field; an untyped bag defeats the point of putting it in Thrift.
- Use `list<string>` when the partner accepts several targets (advertisers, instances). Do not encode a list as a comma-separated `string`.

Field numbering: append the next unused number in the struct; append the next unused tag in the
`TaxonomyProtocolConfig` union. Never renumber or reuse a tag, even a deleted one.

---

## Step 2 — Generate `dist_types`

File: `dist_types/src/main/thrift/taxonomy_service.thrift`

```thrift
struct {{Connector}}TaxonomyConfig {
  1: required string oauth_integration_id;   // only if OAuth
  2: required string {{tenant_id_field}};    // seat / manager / advertiser account
  3: required string region;                 // only if the endpoint varies by region
}
```

Append to the union (use the next free tag, `{{NEXT_TAG}}`):

```thrift
union TaxonomyProtocolConfig {
  // ... existing
  {{NEXT_TAG}}: {{Connector}}TaxonomyConfig {{connector_snake}}_taxonomy_config;
}
```

If a new OAuth flow is needed, also append to `dist_types/src/main/thrift/oauth_service.thrift`:

```thrift
struct {{Connector}}OAuthEndpointConfig {
  1: required string region;
}

union OAuthEndpointConfig {
  // ... existing
  {{NEXT_OAUTH_TAG}}: {{Connector}}OAuthEndpointConfig {{connector_snake}};
}
```

**Rule:** the value that acts as the OAuth *seat* during credential validation must be a `required` Thrift field. If the
OAuth seat and the taxonomy tenant id disagree, the connector authenticates as the wrong account.

---

## Step 3 — Generate `dist` boilerplate

### 3a. Constants + lookups

`java/partner_apis/src/main/java/com/liveramp/partner_apis/clients/{{connector_snake}}/{{Connector}}Constants.java`

Generate this class always — even a single-region connector needs somewhere for `API_URL` and the manual-test ids.

```java
package com.liveramp.partner_apis.clients.{{connector_snake}};

import java.util.Map;
import com.google.common.collect.ImmutableMap;

public final class {{Connector}}Constants {

  private {{Connector}}Constants() {}

  public static final String API_URL = "https://api.{{partner}}.com";

  // Only generate the region map when the developer said the endpoint varies by region.
  private static final Map<String, String> REGION_TO_API_URL = ImmutableMap.of(
      "NA", "https://api.{{partner}}.com",
      "EU", "https://api-eu.{{partner}}.com"
  );

  public static String get{{Connector}}ApiUrlForRegion(String region) {
    if (region == null) {
      return null;
    }
    String override = System.getenv("{{CONNECTOR_UPPER}}_API_URL_" + region.toUpperCase());
    return override != null ? override : REGION_TO_API_URL.get(region.toUpperCase());
  }

  // For the main() manual-test harness.
  public static final String TEST_{{TENANT_UPPER}} = "";
}
```

Generate one `Map` + accessor per "derivable" value from Step 1 (region → URL, country → marketplace, etc.). Each
accessor returns `null` for unknown input so the caller can raise a clear precondition failure.

### 3b. Deliverer skeleton

`java/taxonomy_service/src/main/java/com/liveramp/taxonomy_service/deliverer/{{connector_snake}}/{{Connector}}TaxonomyDeliverer.java`

This shape is shared by every streaming-destination taxonomy deliverer: accumulate two lists, acquire the bearer token
once before the loop, ensure any account-scoped parent resource once, iterate fields, deserialize the segment body, call
the partner, record `set_override(...)` on success and `set_failure_message(...)` on failure, and finish with
`TaxonomyUtils.buildTaxonomyExchangeResult`.

There are exactly two hooks. `ensureAccountScopedResources()` runs once per sync and takes no per-segment argument —
everything it needs is a Thrift config field by the Step 1 rule. `createOrVerifySegment(...)` runs per field. Amazon
DM's dataroom fits the first; its dataset and sharing rules fit the second. Connectors with no parent resource leave the
first hook out entirely.

```java
package com.liveramp.taxonomy_service.deliverer.{{connector_snake}};

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import com.google.common.base.Preconditions;
import com.google.common.collect.ImmutableSet;
import com.google.gson.Gson;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.liveramp.java_support.logging.LoggingHelper;
import com.liveramp.partner_apis.api_service.ApiServiceFactory;
import com.liveramp.partner_apis.clients.{{connector_snake}}.{{Connector}}ApiServiceHandler;
import com.liveramp.partner_apis.clients.{{connector_snake}}.{{Connector}}Constants;
import com.liveramp.s2s_distribution_lib.service_clients.OAuthServiceClient;
import com.liveramp.s2s_distribution_lib.util.OAuthUtils;
import com.liveramp.taxonomy_service.deliverer.TaxonomyDeliverer;
import com.liveramp.taxonomy_service.util.TaxonomyUtils;
import com.liveramp.types.oauth_service.OAuthService;
import com.liveramp.types.taxonomy_service.FailedExchangedTaxonomyField;
import com.liveramp.types.taxonomy_service.ResolvedTaxonomyField;
import com.liveramp.types.taxonomy_service.SuccessfullyExchangedTaxonomyField;
import com.liveramp.types.taxonomy_service.TaxonomyExchangeResult;
import com.liveramp.types.taxonomy_service.TaxonomyExchangeResultFailure;
import com.liveramp.types.taxonomy_service.TaxonomyField;
import com.liveramp.types.taxonomy_service.{{Connector}}TaxonomyConfig;

public class {{Connector}}TaxonomyDeliverer implements TaxonomyDeliverer {

  private static final Logger LOG = LoggerFactory.getLogger({{Connector}}TaxonomyDeliverer.class);

  private final {{Connector}}ApiServiceHandler apiService;
  private final OAuthService.Iface oAuthClient;
  private final int oAuthIntegrationId;
  private final String {{tenantIdField}};

  public {{Connector}}TaxonomyDeliverer({{Connector}}TaxonomyConfig config, OAuthService.Iface oAuthClient) {
    String oauthIntegrationId = config.get_oauth_integration_id();
    Preconditions.checkArgument(StringUtils.isNotBlank(oauthIntegrationId), "oauth_integration_id is required");
    int parsedIntegrationId;
    try {
      parsedIntegrationId = Integer.parseInt(oauthIntegrationId.trim());
    } catch (NumberFormatException e) {
      throw new IllegalArgumentException(
          String.format("oauth_integration_id must be a valid integer: %s", oauthIntegrationId), e);
    }
    this.oAuthIntegrationId = parsedIntegrationId;
    this.oAuthClient = oAuthClient;

    Preconditions.checkArgument(StringUtils.isNotBlank(config.get_{{tenant_id_field}}()),
        "{{tenant_id_field}} is required");
    this.{{tenantIdField}} = config.get_{{tenant_id_field}}();

    // Single-region connector: use {{Connector}}Constants.API_URL.
    // Region-scoped connector: resolve and null-check, as below.
    String apiUrl = {{Connector}}Constants.get{{Connector}}ApiUrlForRegion(config.get_region());
    Preconditions.checkNotNull(apiUrl, String.format("Region %s is not supported.", config.get_region()));
    this.apiService = ApiServiceFactory.{{connectorCamel}}(apiUrl);
  }

  // Visible for testing: inject a stubbed handler.
  {{Connector}}TaxonomyDeliverer(
      {{Connector}}ApiServiceHandler apiService, OAuthService.Iface oAuthClient,
      int oAuthIntegrationId, String {{tenantIdField}}) {
    this.apiService = apiService;
    this.oAuthClient = oAuthClient;
    this.oAuthIntegrationId = oAuthIntegrationId;
    this.{{tenantIdField}} = {{tenantIdField}};
  }

  @Override
  public TaxonomyExchangeResult sync(Set<ResolvedTaxonomyField> fields) {
    LOG.info("Starting {{Connector}} sync: fieldCount={}", fields.size());

    // Token is fetched once per sync. A failure here is endpoint-wide, not per-field,
    // so it returns result_failure rather than failing every field individually.
    String bearerToken;
    try {
      bearerToken = OAuthUtils.getBearerToken(oAuthClient, oAuthIntegrationId);
    } catch (Exception e) {
      LOG.error("Failed to get access token for oAuthIntegrationId={}", oAuthIntegrationId, e);
      return TaxonomyExchangeResult.result_failure(
          new TaxonomyExchangeResultFailure("Failed to get access token."));
    }

    List<SuccessfullyExchangedTaxonomyField> successfullySyncedFields = new ArrayList<>();
    List<FailedExchangedTaxonomyField> failedSyncedFields = new ArrayList<>();

    // Omit this block entirely when the partner has no parent/container resource.
    // Runs once: the resources it creates are account-scoped, so retrying per field would only
    // repeat the same call. A failure is attributed to every field, since none can proceed.
    String setupFailure = null;
    try {
      ensureAccountScopedResources();
    } catch (Exception e) {
      setupFailure = String.format("{{Connector}} account setup failed: %s", formatErrorCause(e));
      LOG.error(setupFailure, e);
    }

    for (ResolvedTaxonomyField resolvedField : fields) {
      if (setupFailure != null) {
        failedSyncedFields.add(
            new FailedExchangedTaxonomyField(resolvedField).set_failure_message(setupFailure));
        continue;
      }
      String fieldContext = formatFieldContext(resolvedField);
      try {
        SegmentPayload payload =
            new Gson().fromJson(resolvedField.get_resolved_segment_body(), SegmentPayload.class);

        // ---- CONNECTOR-SPECIFIC HOOK: implement this method by hand. ----
        String overrideId = createOrVerifySegment(bearerToken, payload, fieldContext);
        // ----------------------------------------------------------------

        successfullySyncedFields.add(
            new SuccessfullyExchangedTaxonomyField(resolvedField).set_override(overrideId));
      } catch (Exception e) {
        String message = String.format("{{Connector}} sync failed for %s: %s", fieldContext, formatErrorCause(e));
        LOG.error(message, e);
        failedSyncedFields.add(
            new FailedExchangedTaxonomyField(resolvedField).set_failure_message(message));
      }
    }

    return TaxonomyUtils.buildTaxonomyExchangeResult(successfullySyncedFields, failedSyncedFields);
  }

  /**
   * Ensures the account-scoped parent resource the partner requires before any segment can be
   * created (Amazon DM: the dataroom). Runs once per sync, not once per field. Takes no arguments:
   * everything it needs is a Thrift config field.
   *
   * TODO: implement, or delete this method and its call site if the partner has no such resource.
   * Must be idempotent — it runs on every sync, including syncs where nothing has changed.
   */
  private void ensureAccountScopedResources() throws Exception {
    throw new UnsupportedOperationException("ensureAccountScopedResources not implemented");
  }

  /**
   * Creates the segment on the partner platform (or finds an equivalent one) and returns the
   * platform id persisted as the override.
   *
   * TODO: implement. This is the only destination-specific method; everything else in this class
   * is shared scaffolding. Must be idempotent — a retried sync must not create duplicates.
   */
  private String createOrVerifySegment(String bearerToken, SegmentPayload payload, String fieldContext)
      throws Exception {
    throw new UnsupportedOperationException("createOrVerifySegment not implemented");
  }

  private static String formatFieldContext(ResolvedTaxonomyField field) {
    TaxonomyField tf = field.get_taxonomy_field();
    return String.format("fieldId=%d valueId=%d fieldLabel=%s valueLabel=%s",
        tf.get_field_id(), tf.get_value_id(), tf.get_field_label(), tf.get_value_label());
  }

  private static String formatErrorCause(Exception e) {
    return e.getMessage() != null ? e.getMessage() : e.getClass().getSimpleName();
  }

  /** Gson-deserialized shape of segment_body_format. Field names must match the template keys. */
  static final class SegmentPayload {
    String name;
    // TODO: add the per-segment fields identified in Step 1.
  }

  // Manual end-to-end harness against the partner sandbox. Every connector in this family has one.
  public static void main(String[] args) {
    LoggingHelper.configureConsoleLogger();
    if (args.length != 1) {
      System.out.println("Usage: oAuthIntegrationId");
      return;
    }
    String resolvedSegmentBody = "{\"name\":\"test segment 1\"}";
    Set<ResolvedTaxonomyField> fields = ImmutableSet.of(
        new ResolvedTaxonomyField(new TaxonomyField(), resolvedSegmentBody));

    TaxonomyDeliverer deliverer = new {{Connector}}TaxonomyDeliverer(
        new {{Connector}}TaxonomyConfig({{Connector}}Constants.TEST_{{TENANT_UPPER}}).set_oauth_integration_id(args[0]),
        OAuthServiceClient.PRODUCTION.reconnectingClient());

    LOG.info(deliverer.sync(fields).toString());
  }
}
```

**Optional block — only generate when the developer says repeat syncs must reuse an existing platform id.**
Amazon DM does this; Pinterest and LinkedIn do not. Add the helper as a class member, and insert the loop fragment
immediately *after* the `fieldContext` assignment and *before* the `try` — it reads `fieldContext`, so placing it above
that line will not compile.

If **both** this block and the batch-scoped hook are generated, the stored-id check must come first: a field that
already has a platform id needs no parent resource, so it should succeed even when `ensureAccountScopedResources()`
failed. Guard the setup call with `fields.stream().anyMatch(f -> StringUtils.isEmpty(getStoredSegmentId(f)))` and move
the `setupFailure` check below the stored-id short-circuit. This is what Amazon DM does.

```java
  private static final String OVERRIDE_ID_PROPERTY = "platform_integration_segment_id";

  private static String getStoredSegmentId(ResolvedTaxonomyField field) {
    TaxonomyField tf = field.get_taxonomy_field();
    if (tf.is_set_metadata() && tf.get_metadata().is_set_properties()) {
      return tf.get_metadata().get_properties().get(OVERRIDE_ID_PROPERTY);
    }
    return null;
  }
```

```java
      String storedId = getStoredSegmentId(resolvedField);
      if (StringUtils.isNotEmpty(storedId)) {
        LOG.info("Using stored platform segment id, skipping create: id={}, {}", storedId, fieldContext);
        successfullySyncedFields.add(
            new SuccessfullyExchangedTaxonomyField(resolvedField).set_override(storedId));
        continue;
      }
```

### 3c. Factory wiring

`java/taxonomy_service/src/main/java/com/liveramp/taxonomy_service/deliverer/TaxonomyToolsFactory.java` — add imports
and one case to `newDeliverer`, before `default:`:

```java
import com.liveramp.taxonomy_service.deliverer.{{connector_snake}}.{{Connector}}TaxonomyDeliverer;
import com.liveramp.types.taxonomy_service.{{Connector}}TaxonomyConfig;
```

```java
      case {{CONNECTOR_UPPER}}_TAXONOMY_CONFIG:
        return new {{Connector}}TaxonomyDeliverer(
            ({{Connector}}TaxonomyConfig) config.getFieldValue(setField), oAuthClient);
```

Drop the `oAuthClient` argument if the connector does not use OAuth. Do not touch `newFileGenerator` — that is only for
batch/file deliverers, which are out of scope here.

### 3d. Documented segment body

Emit the `segment_body_format` template the endpoint config must use, built **only** from the values that differ per
segment (question 5). Anything batch-invariant belongs in the Thrift struct, not here. Keep its keys in sync with
`SegmentPayload`:

```json
{
  "name": "<segment name>"
}
```

### 3e. Test skeleton

`java/taxonomy_service/src/test/java/com/liveramp/taxonomy_service/deliverer/{{connector_snake}}/Test{{Connector}}TaxonomyDeliverer.java`

Generate tests for the boilerplate only, using the package-private constructor with a stubbed handler:

- Constructor rejects a blank or non-numeric `oauth_integration_id`, and a blank `{{tenant_id_field}}`.
- Each generated lookup returns the expected value for known input and `null` for unknown input; an unsupported region fails construction.
- A token-fetch failure yields `TaxonomyExchangeResult.result_failure` and makes no partner calls.
- A hook exception on one field produces a `FailedExchangedTaxonomyField` while other fields still succeed.
- A successful field carries the platform id through `set_override`.
- If the stored-override block was generated: a field with `platform_integration_segment_id` set returns success without calling the handler.
- If the batch-scoped hook was generated: it is invoked exactly once for a multi-field sync, and a failure inside it marks every field failed.

---

## Step 4 — Final checklist to print

- [ ] Every batch-invariant value is a Thrift field; nothing per-segment leaked into the struct.
- [ ] Nothing batch-invariant left in `segment_body_format` — the body contains only values that genuinely differ per segment.
- [ ] New union tag appended, no tag renumbered or reused.
- [ ] The OAuth seat value is a `required` Thrift field.
- [ ] Every derived value (URL, marketplace, etc.) is a lookup in `dist`, not a Thrift field.
- [ ] Constructor validates every `required` field with a `Preconditions` message naming the field.
- [ ] Token acquired once per `sync`, not once per field.
- [ ] `SegmentPayload` field names match the `segment_body_format` keys.
- [ ] `createOrVerifySegment` is idempotent.
- [ ] Per-field failures are collected, not thrown — one bad segment must not fail the batch.
- [ ] Factory case added; `default:` still last.
- [ ] **Generated code compiles as emitted.** Unimplemented hooks throw `UnsupportedOperationException`; they are never
      left as bare `// TODO` bodies on a non-void method. Verify with `./gradlew :taxonomy_service:compileJava` from `java/`.
- [ ] Every referenced symbol is imported, including `LoggingHelper`, `ImmutableSet`, `OAuthServiceClient` and
      `{{Connector}}ApiServiceHandler` used only by `main()` or the constructor.
- [ ] `{{Connector}}ApiServiceHandler` and the `ApiServiceFactory.{{connectorCamel}}(...)` factory method exist. If the
      partner client is not written yet, generate a minimal handler class with stubbed methods so the deliverer compiles.
- [ ] Thrift regenerated before compiling `dist` — `{{Connector}}TaxonomyConfig` and the new union tag must exist, and the
      `main()` constructor call must match the struct's actual required-field order.
- [ ] No blank-final assigned inside a `try` block; parse into a local, then assign.
- [ ] Every property in the Shared properties table is written to global context, including the two booleans, so the
      `taxonomy-partner-flow` skill resolves the same names.

## Relationship to `taxonomy-partner-flow`

> **Dependency: `taxonomy-partner-flow` depends on `taxonomy-connector-scaffold`. This skill has no dependency on it.**
> `taxonomy-partner-flow` must not run before this skill has produced the Thrift struct, the deliverer skeleton and the factory
> wiring, and must not be invoked to "fix up" or restructure that output.

The partner-specific resource chain (Amazon DM's dataroom → dataset → sharing rules, Google's audience list, LinkedIn's
DMP segment) belongs in `taxonomy-partner-flow`, one invocation per partner or one parameterized by partner API docs.
`taxonomy-connector-scaffold` owns the contract; `taxonomy-partner-flow` fills in the two hooks.

**Contract `taxonomy-partner-flow` must honor** — fixed here, not negotiable downstream:

- Implement `ensureAccountScopedResources()` (if this skill generated it) and
  `createOrVerifySegment(bearerToken, payload, fieldContext)`.
- Return the partner's platform segment id from `createOrVerifySegment`; the caller persists it via `set_override`.
- Keep both hooks idempotent. Both run on every sync, including no-op syncs.
- Throw on failure. Do not catch and return null — the generated loop converts the exception into a per-field failure
  with the right message and context.
- Do not restructure `sync()`, move the token fetch into the loop, change the hook signatures, or swallow exceptions.
- Read shared identifiers from global context (see the Shared properties section), never re-derive them.
- Additions that are allowed: private helpers, request/response model classes, and new methods on
  `{{Connector}}ApiServiceHandler`.
- The same compile requirement applies to `taxonomy-partner-flow`'s output.

If the partner needs a value the hooks do not receive, that is a signal to re-run Step 1 — the value is almost certainly
batch-invariant and belongs in the Thrift config, reachable as a field. `taxonomy-partner-flow` should surface that rather than
threading an extra parameter through the hooks.

## Smells to flag if seen

- A Thrift field whose value the developer says "depends on the segment" → belongs in the segment body.
- A Thrift field holding a full URL → should be a region field plus a lookup.
- A Thrift field holding a client id or secret that OAuth already returns → read it from OAuth metadata.
- A `map<string,string>` or JSON-encoded blob in the Thrift config.
- More than one field that identifies the tenant, with no rule for which one wins.
- A token fetch inside the per-field loop.
- An endpoint-level constant rendered into every segment body (the Amazon DM `advertiserAccountIds` mistake) → Thrift field.
- A comma-separated string in the segment body standing in for a list → `list<string>` Thrift field.
- The batch-scoped hook called from inside the per-field loop.
