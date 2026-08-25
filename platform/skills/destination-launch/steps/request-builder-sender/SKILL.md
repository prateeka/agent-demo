---
name: destination-launch-request-builder-sender
description: Request builder and request sender for streaming delivery in dist (s2s_data_syncer).
---

# Step: request-builder-sender

Implement the **request builder** (assemble a partner payload from a `DistributionRecord`) and the
**request sender** (HTTP send path + response/error handling) for a streaming destination in the
`dist` `s2s_data_syncer` module.

This step turns the partner API client (from `partner-api-client`) into a working send path. It does
**not** own the transposer, `Format`→properties mapping, or record-handler config wiring — those are
finished in `transposer-record-handler`. See **Boundary with transposer-record-handler** below.

## Repos

`dist`, `dist_types` — see `platform/config/repos.yaml`. All new code lives in the `dist`
`s2s_data_syncer` module under
`java/s2s_data_syncer/src/main/java/com/liveramp/streaming_deliverer/handler/integration/{destination}/`.

## Detect prior work

If `## Details` on the step task is filled, diff the repo against the recorded file paths before
re-implementing. Also grep for the destination package
(`handler/integration/{destination}/`) and for a `{DEST}_FORMAT` / `StreamingAlgorithm.{DEST}` entry
in `RecordHandlerFactory` — a partial launch may already have scaffolding.

## Read first — exact global keys

From `launches/{slug}/epic.md` → `## Global context`:

- `release.ticket_id` — PR titles use `[{release.ticket_id}] ...`
- `destination.api_family`, `thrift.streaming_format`, `thrift.streaming_endpoint_config`
- `streaming.api_base_urls`
- `oauth.type`

Also read this step's task file (path supplied by the orchestrator) for local detail.

## Ask the user

### 1. Handler type — ask this FIRST (it decides the interface you implement)

How does the partner API map records to HTTP requests? The answer picks the builder interface,
factory, and record-handler package:

| User answer | Handler type | Builder interface (`handler/type/...`) | Builder method |
|---|---|---|---|
| One record → one request (AmazonDM default) | **one-to-one** | `one_to_one/OneToOneRequestBuilder<PRequest>` | `PRequest buildPartnerRequest(DistributionRecord)` |
| Batch many records into one request | **many-to-one** | `many_to_one/ManyToOneRequestBuilder<PRequest>` | `PRequest buildPartnerRequest(Collection<DistributionRecord>)` (+ `buildPartnerRequests(...)` for multi-send) |
| One record → several requests | **one-to-many** | `one_to_many/OneToManyRequestBuilder<PRequest>` | `List<PRequest> buildPartnerRequests(DistributionRecord)` |

If **many-to-one**, also ask: max batch size, and whether partial-batch failures must be reported
per-record (affects response mapping / `BulkPartnerResponse`).

### 2. Payload / auth / semantics

- Audience ingestion **mandatory headers** (auth, client id, account id, api version)?
- Request **payload shape** and **operation types** (e.g. ADD→CREATE, DELETE→DELETE), plus consent
  or TTL fields the partner requires?
- **Identifier type(s)** to support (LiveRamp ID, MAID, hashed PII, …) and how each maps into the
  payload?
- Which HTTP status codes are **success**, which are **retryable**, and which are **terminal**
  (quarantine / skip)?

## Reference implementation — Amazon DM (s2s_data_syncer)

Mirror these classes; keep the same package/file layout under `handler/integration/{destination}/`.

| Concern | Amazon DM class (relative to `dist`) |
|---|---|
| Request builder | `java/s2s_data_syncer/.../handler/integration/amazon_dm/AmazonDMRequestBuilder.java` |
| Partner request (immutable POJO) | `.../amazon_dm/AmazonDMPartnerRequest.java` |
| Request sender | `.../amazon_dm/AmazonDMRequestSender.java` |
| Invalid-dataset cache (optional) | `.../amazon_dm/AmazonDMInvalidDataSetCache.java` |
| Builder factory hook | `.../handler/config/factory/OneToOneRequestBuilderFactory.java` → `AmazonDMRequestBuilderFactory` |
| Sender factory hook | `.../handler/config/factory/RequestSenderFactory.java` → `AmazonDMSenderFactory` |
| Response type | `.../handler/sender/http/StreamingPartnerResponse.java` |
| Interfaces | `.../handler/type/one_to_one/OneToOneRequestBuilder.java`, `.../handler/sender/RequestSender.java` |
| Retry wrapper | `.../handler/sender/SenderRetryDecorator.java` |
| Tests | `java/s2s_data_syncer/src/test/.../integration/amazon_dm/TestAmazonDMRequestBuilder.java`, `TestAmazonDMRequestSender.java` |

## Internal sub-steps (skill-owned)

### 1. Partner request POJO — `{Dest}PartnerRequest implements PartnerRequest`

- Immutable; one field per value the sender needs (ids, account/client ids, `accessToken`, payload).
- Mark secrets (`accessToken`) `transient`; `toString()` returns `new Gson().toJson(this)` for logging.

### 2. Request builder — `{Dest}RequestBuilder implements {HandlerType}RequestBuilder<{Dest}PartnerRequest>`

Implement the interface for the handler type chosen in **Ask the user #1** (`OneToOne` shown below;
for many-to-one, iterate the `Collection<DistributionRecord>`; for one-to-many, return a
`List<PRequest>`). Core logic (`buildPartnerRequest`):

- Constructor args match the AmazonDM shape:
  `DistributionFieldFormatter`, `Properties`, `IdentifierTransformer`,
  `Map<String, DistributionIdentifierTransformation>`, `OAuthService.Iface`.
- Read config from `properties.getProperty({Dest}Constants.X_PROPERTY)` (property keys come from the
  `partner-api-client` constants).
- Map operation type: `OperationType.valueOf(properties.getProperty(OPERATION_TYPE_PROPERTY))` →
  partner action; throw `IllegalArgumentException` on unsupported values.
- OAuth: `OAuthHandler oauthHandler = new OAuthHandler(oAuthClient, oauthIntegrationId);` then
  `oauthHandler.getAccessToken()` and `oauthHandler.getMetadataProperty(CLIENT_ID_PROPERTY)`; throw
  `RuntimeException` if required metadata is missing.
- Resolve the id label(s):
  `distributionFieldFormatter.getIdLabels(record.get_dist_fields())`.
- For each `DistributionEntity entity : record.get_entities()`, transform the identifier via
  `identifierTransformer.doTransformation(DistributionEntityUtils.getExternalIdentifier(entity),
  identifierTransformationsByName.get(EXTERNAL_IDENTIFIER_NAME))`, then append to the payload.
- Optional overrides: `filterRecord(record)` to drop records; `buildDestinationStatsRequest(...)` for
  stats-only destinations.

### 3. Request sender — `{Dest}RequestSender implements RequestSender<{Dest}PartnerRequest, StreamingPartnerResponse>`

Implement `sendRequest(request) throws IOException`:

- Build the Retrofit client from the partner API service:
  `new ApiServiceFactory.Builder<>({Dest}ApiService.class, {Dest}Constants.BASE_URL).build()`
  (provide a `@VisibleForTesting` constructor that injects a mock `ApiService`).
- Call the partner endpoint; time it with `DogClient.get().recordExecutionTime(...)`.
- **Response mapping** into `StreamingPartnerResponse`:
  - success → `setSuccessful(true)`, `setStatusMessage(...)`, metric `response:success`.
  - partial/logical errors in body → `setSuccessful(false)`, `addErrorToMap(...)`, metric
    `response:quarantined`.
  - `null` response → throw `IOException` (metric `response:failure`).
- **Error/retry contract (critical — the retry decorator depends on it):**
  - **Throw `IOException`** for transient/retryable failures (5xx, timeouts, 429 when retry enabled).
    `SenderRetryDecorator` retries on thrown `IOException` or when
    `response.getRetryInfo().shouldRetry()` is true.
  - **Return an unsuccessful response (do not throw)** for terminal, non-retryable cases you want to
    skip/quarantine (e.g. 404 not-found, cached-invalid dataset).
  - Inspect `RetrofitError`: `status = re.getResponse().getStatus()`; special-case 404 (skip / cache
    invalid) and 429 (rate-limit metric) as the reference does.
- Metrics: destination tag `destination:{dest}`, counter `streaming_jobs_count` with
  `response:success|failure|quarantined`, plus any destination-specific counters.

### 4. Wire the factory hooks (in this step)

- Builder factory — add an inner class to the factory that matches the handler type:
  for **one-to-one**, `{Dest}RequestBuilderFactory implements OneToOneRequestBuilderFactory` (see
  `AmazonDMRequestBuilderFactory`) whose `build(...)` returns
  `new {Dest}RequestBuilder(distributionFieldFormatter, properties, identifierTransformer,
  identifierTransformationsByName, oauthServiceClient)`. For **many-to-one / one-to-many**, use the
  corresponding batch/config factory in `handler/config/factory/` instead.
- `RequestSenderFactory` — add inner class
  `{Dest}SenderFactory implements RequestSenderFactory` whose `build(...)` returns
  `new {Dest}RequestSender()`.

### 5. Unit tests

Add `Test{Dest}RequestBuilder` and `Test{Dest}RequestSender` alongside the classes; see the test
matrix below.

## Boundary with transposer-record-handler

Finish here vs. defer to `transposer-record-handler`:

| Wiring | Owner |
|---|---|
| `{Dest}PartnerRequest`, `{Dest}RequestBuilder`, `{Dest}RequestSender` | **this step** |
| `{Dest}RequestBuilderFactory` / `{Dest}SenderFactory` inner classes | **this step** |
| `RecordHandlerFactory.ALGORITHM_BY_FORMAT` (`Format._Fields.{DEST}_FORMAT → StreamingAlgorithm.{DEST}`) | transposer-record-handler |
| `RecordHandlerFactory.getProperties(...)` case (thrift `Format` → `Properties`) | transposer-record-handler |
| `getFieldFormatsAndFieldId(...)` case, record-handler config factory, metrics registration | transposer-record-handler |

If the record-handler wiring is already present (partial launch), just confirm the factory hooks
reference your new builder/sender.

**Handoff artifact:** `transposer-record-handler` defines the `{Dest}Format` thrift struct and its
`RecordHandlerFactory.getProperties(...)` case using the *exact* `{Dest}Constants.X_PROPERTY` names
and types your builder reads via `properties.getProperty(...)`. These must match by name and type —
hand off the property-key table below (see **Write to step task**) rather than loose prose, so the
two steps can't silently drift out of sync.

## Test matrix (mirror the AmazonDM tests)

**Builder** (`Test{Dest}RequestBuilder`, Mockito): build with `new DefaultProperties(map)`; mock
`DistributionFieldFormatter`, `IdentifierTransformer`, the transformations map, `OAuthService.Iface`,
and `DistributionRecord`.

- Each supported identifier type maps to the correct payload field.
- Operation type → partner action (ADD→CREATE, DELETE→DELETE, …).
- Multiple entities produce members in order.
- Request carries correct metadata (account/client ids, access token, dataset id).
- Missing required OAuth metadata → `RuntimeException`.
- Unsupported identifier type → `IllegalArgumentException`.

**Sender** (`Test{Dest}RequestSender`, Mockito): inject mock `ApiService` via the test constructor.

- Success (no errors) → `isSuccessful()` true; API called once.
- Partial failure (errors in body) → not successful; error map populated.
- Retryable statuses (429/401/403/500, null response) → `IOException` thrown.
- Terminal 404 → not successful, dataset cached invalid; second call skips the HTTP call.
- Pre-cached-invalid dataset → skips the HTTP call entirely.

## Write to step task (local)

Record on `launches/{slug}/tasks/request-builder-sender.md`:

- **Property-key table (required handoff to `transposer-record-handler`)** — one row per config
  value read via `properties.getProperty({Dest}Constants.X_PROPERTY)`:

  | Constant (`{Dest}Constants.X_PROPERTY`) | Source `{Dest}Format` field | Type | Required? |
  |---|---|---|---|
  | e.g. `OPERATION_TYPE_PROPERTY` | e.g. `operation_type` | `String` (enum name) | yes |

  Include every property the builder reads — headers, identifier type(s), operation-type mapping,
  account/client ids, OAuth integration id, etc. This table is what `transposer-record-handler`
  copies 1:1 into the new `{Dest}Format` struct and its `getProperties()` case — don't summarize as
  prose.
- Success / retry / terminal status codes and whether an invalid-dataset cache was added.
- File paths for builder, sender, partner request, factories, tests.
- Test output summary and PR link (`[{release.ticket_id}] ...`).

## Return global keys (orchestrator merges)

- `streaming.operation_types` (list)
- `streaming.identifier_types` (list)

Return only these unless the user explicitly asks to add more to global context.

## Definition of done

- `{Dest}RequestBuilder` and `{Dest}RequestSender` compile and their unit tests pass.
- Send path is wired to the partner API client from `partner-api-client`.
- Builder/sender factory hooks reference the new classes.
- Error/retry contract honored (throw `IOException` for retryable; return unsuccessful for terminal).

## Verification

Run the builder and sender unit tests per repo conventions (see `dist/AGENTS.md` for the module test
command). Confirm the factory hooks resolve and the retry decorator behavior matches the status-code
contract above.
