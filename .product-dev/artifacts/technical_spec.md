# Technical Specification — Tea Tracker

Source prompt: `technical-spec-consolidated`
Generated: 2026-04-04

---

## Product Summary

Tea Tracker is a personal tea collection management app ("Tea Cabinet Snapshot"). The core user interaction is opening the app and immediately seeing which teas need attention — with freshness status and vendor context attached — without relying on memory or manual tracking.

The system is a client-server product: a mobile/web client backed by a REST API with a relational database. Single-user collections; no sharing or social features.

---

## Part 1 — Data Models

Full specification: `.product-dev/artifacts/data_models.md`

### Entities

**User** — Authenticated account, owns a collection.

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUID v4 | PK, immutable |
| `email` | string, max 254 | Unique, RFC 5321, lowercase |
| `password_hash` | string, max 255 | bcrypt, write-only |
| `created_at` | timestamp UTC | Immutable |
| `updated_at` | timestamp UTC | Auto-updated |

**Tea** — Core entity. One entry per distinct product in the collection.

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUID v4 | PK, immutable |
| `user_id` | UUID v4 | FK → User, non-null |
| `vendor_id` | UUID v4 | FK → Vendor, nullable |
| `name` | string, max 200 | Required, trimmed |
| `type` | enum | `green\|black\|oolong\|white\|puerh\|herbal\|other` |
| `status` | enum | `sealed\|opened\|finished`, default `sealed` |
| `quantity_g` | integer | Min 0, nullable |
| `opened_at` | date YYYY-MM-DD | Nullable; required when status=opened |
| `purchased_at` | date YYYY-MM-DD | Nullable |
| `freshness_window_days` | integer | Min 1, nullable (overrides type default) |
| `notes` | string, max 1000 | Nullable |
| `created_at` / `updated_at` | timestamp UTC | Standard audit fields |

**Computed at read time (not stored):**
- `days_since_opened` — `CURRENT_DATE - opened_at` when status=opened
- `freshness_status` — `fresh | warning | stale` (see BR-002)
- `effective_freshness_window_days` — per-tea override or type default
- `vendor_name` — denormalized from Vendor for read performance

**Vendor** — Tea supplier, scoped per user.

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | UUID v4 | PK, immutable |
| `user_id` | UUID v4 | FK → User, non-null |
| `name` | string, max 200 | Required, trimmed, unique per user (case-insensitive) |
| `created_at` / `updated_at` | timestamp UTC | Standard audit fields |

**Required indexes:**
- `User.email` (unique)
- `Tea.(user_id)`, `Tea.(user_id, status)`, `Tea.(user_id, opened_at)`
- `Vendor.(user_id)`, `Vendor.(user_id, name)` (unique)

**Type freshness defaults:**

| Type | Window (days) |
|------|--------------|
| green | 30 |
| white | 60 |
| oolong | 45 |
| black | 180 |
| puerh | 730 |
| herbal | 90 |
| other | 90 |

---

## Part 2 — API Contracts

Full specification: `.product-dev/artifacts/api_contracts.md`

### Auth Model

JWT Bearer tokens. Access token TTL: 24 hours. Refresh token TTL: 30 days, server-side stored, rotated on use. Public endpoints: register and login only.

### Endpoint Inventory

| Method | Route | Purpose | Auth |
|--------|-------|---------|------|
| POST | `/v1/auth/register` | Create account | No |
| POST | `/v1/auth/login` | Issue tokens | No |
| POST | `/v1/auth/refresh` | Rotate access token | No (uses refresh token) |
| POST | `/v1/auth/logout` | Revoke refresh token | Yes |
| GET | `/v1/teas` | Collection overview | Yes |
| POST | `/v1/teas` | Add tea | Yes |
| GET | `/v1/teas/:id` | Tea detail | Yes |
| PATCH | `/v1/teas/:id` | Update tea / decrement quantity | Yes |
| DELETE | `/v1/teas/:id` | Remove tea | Yes |
| GET | `/v1/vendors` | Vendor list / autocomplete | Yes |
| POST | `/v1/vendors` | Create vendor | Yes |

### Standard Error Shape

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "human-readable description",
    "details": [{ "field": "name", "issue": "required" }]
  }
}
```

`details` is present on 400 only; empty array on all other error codes.

### Key Endpoint Notes

- `GET /v1/teas` sort order follows BR-001 (stale opened → warning opened → fresh opened → sealed). Excludes `finished` teas by default. Cursor-based pagination, default page size 50.
- `POST /v1/teas` — `user_id` set server-side from JWT `sub`. `opened_at` defaults to today when `status=opened` and omitted.
- `PATCH /v1/teas/:id` — partial update semantics. "Brewed" action sends absolute `quantity_g` value (client computes decrement). `vendor_id: null` explicitly removes vendor association.
- `GET /v1/vendors?q=` — case-insensitive prefix match, no cursor pagination (max 50 results), sorted alphabetically.
- Vendor creation is always a separate call before tea creation when a new vendor is entered.

---

## Part 3 — Business Rules

Full specification: `.product-dev/artifacts/business_rules.md`

### Rule Summary

| ID | Name | Trigger | Key Constraint |
|----|------|---------|----------------|
| BR-001 | Attention Priority Sort | `GET /v1/teas` | Stale opened → warning opened → fresh opened → sealed |
| BR-002 | Freshness Status Derivation | Read-time on opened teas | Warning fires at 67% of effective window elapsed |
| BR-003 | Opened Date Requirement | Write when status=opened | Default to today if omitted; reject future dates; clear on revert to sealed |
| BR-004 | Quantity Floor | Any quantity_g write | Min 0; null is valid (untracked); 0 is not the same as null |
| BR-005 | Vendor Uniqueness | POST /v1/vendors | Case-insensitive unique per user; 409 on duplicate |
| BR-006 | Resource Ownership Scoping | Every authenticated request | All queries WHERE user_id = JWT sub; 403 on mismatch |
| BR-007 | Status Transition Rules | PATCH with status change | `finished` is terminal; cannot transition out of it |

### BR-002 Algorithm (authoritative)

```
effective_window = tea.freshness_window_days ?? TYPE_DEFAULTS[tea.type]
days_open = CURRENT_DATE - tea.opened_at

freshness_status =
  days_open <= effective_window * 0.67  → "fresh"
  days_open <= effective_window          → "warning"
  else                                   → "stale"
```

### BR-007 Valid Transitions

```
sealed  → opened    (allowed)
sealed  → finished  (allowed)
opened  → finished  (allowed)
opened  → sealed    (allowed — requires cleared opened_at)
finished → *        (BLOCKED — terminal state)
```

---

## Part 4 — Non-Functional Requirements

Full specification: `.product-dev/artifacts/nfr.md`

### Scale Basis

- MVP target: 1,000 registered users at launch; 10,000 upper bound for initial infra
- Collection ceiling: 500 teas per user
- Sustained throughput: 10 req/s; peak burst: 50 req/s for 60s
- Storage at 10,000 users: <300MB total — single database instance, no sharding

### Response Time Targets

| Operation | P50 | P95 | Hard Timeout |
|-----------|-----|-----|--------------|
| Collection load (`GET /v1/teas`) | <200ms | <500ms | 5s |
| Add tea (`POST /v1/teas`) | <300ms | <600ms | 5s |
| Tea detail (`GET /v1/teas/:id`) | <150ms | <300ms | 5s |
| Vendor autocomplete (`GET /v1/vendors`) | <100ms | <200ms | 3s |
| Auth (login/register) | <500ms | <1000ms | 10s |

### Availability

- Uptime target: 99.5% monthly
- Data durability: ACID guarantees on all writes
- Backup: daily, 30-day retention, RTO <4h, RPO <24h

### Degradation

- Pool exhaustion → `503` with `Retry-After: 5`, never queue indefinitely
- Rate limit: 60 req/IP/min, burst 20 in 5s → `429` with `Retry-After: 60`
- Auth unavailable → `503` on all authenticated endpoints, no fallback to unauthenticated access

### Monitoring Minimums

- Per-endpoint: request rate, P50/P95 latency, 5xx error rate
- Database: P50/P95 query latency
- Auth: failed login rate per IP (brute force detection at >50 failures/minute)
- Alerting: >5% error rate over 1 minute = critical page

---

## Cross-Reference Summary

### Consistency Checks

1. **Data model fields trace to API specs.** All request/response fields in the API contracts are traceable to `Tea`, `Vendor`, or `User` fields, or are explicitly marked as computed.

2. **Business rules map to API error codes.** BR-003 maps to `400 VALIDATION_FAILED` (future date), `422 UNPROCESSABLE` (sealed with stale opened_at). BR-005 maps to `409 CONFLICT`. BR-007 maps to `422 UNPROCESSABLE`. All are consistent.

3. **NFR targets reference specific endpoints.** Vendor autocomplete response time (`<100ms P50`) references `GET /v1/vendors`, which is explicitly in the endpoint inventory.

4. **Sort order in BR-001 matches `GET /v1/teas` spec.** Both exclude `finished` by default and describe the same priority ordering.

### Assumptions Made (design artifacts were silent on these)

1. **Finished tea retention.** The design artifacts describe "mark as finished" as a discrete action separate from delete. Assumption: finished teas are retained in storage and hidden from the default overview (not permanently deleted). A user may want to query finished teas for historical reference. This assumption drives the `status=finished` filter param on `GET /v1/teas`.

2. **Serving size / brew decrement amount.** The user flow says "taps Brewed to decrement quantity" but does not specify by how much. Assumption: the client sends the absolute new `quantity_g` value (client computes the decrement). This avoids the need for a delta semantics API and sidesteps concurrent write concerns. A fixed serving size (e.g. 3g) is a client-side UX decision not specified here.

3. **No vendor management screens.** The screen inventory explicitly notes "no dedicated vendor management screen." This is consistent with the API design (no PATCH/DELETE vendor endpoints). If a user wants to rename a vendor, that path is not in scope.

4. **Freshness window defaults.** The type defaults (30 days for green, 730 for puerh, etc.) are not stated in the design artifacts. These are derived from common tea storage conventions. They are the primary tunable for the prototype test — if users find the warning fires too early or too late, the 67% threshold and/or the per-type defaults are the adjustment points.

5. **Single-user only.** No design artifact addresses multi-user or family accounts. The data model and API are strictly single-user. If this changes, `vendor.user_id` scoping and the JWT ownership model would need revisiting.

6. **Authentication is in scope.** The design artifacts focus on the collection UX and do not detail auth. Auth is assumed necessary for any persistent server-side storage. The register/login/refresh/logout endpoint set is the minimum required. No OAuth/social login is included.

7. **No offline mode.** The design artifacts do not mention offline capability. The spec assumes an always-connected client. If offline-first behavior is required, the data model and sync strategy would need significant additions.

### Inconsistencies Found

1. **"Notes" field ambiguity.** The `notes` field is reserved in the Tea data model but absent from all three screens in the screen inventory and not present in the user flow. It is not exposed in the MVP Add Tea form spec. This is intentional (future capability) but creates a gap: the field exists in the data model and API but is invisible to the user. Decision: retain it in the schema for forward compatibility, do not expose in MVP UI.

2. **"Edit details" mentioned in Tea Detail but not specced as a screen.** The screen inventory's Tea Detail section lists "edit details" as a secondary action. The screen inventory has no dedicated Edit screen — edits presumably happen inline on the Detail screen. The API supports this via `PATCH /v1/teas/:id`. No inconsistency in the API, but the client UI implementation will need to decide between in-place editing and a separate edit form. This is a client-side decision outside the scope of this spec.

3. **Brewed action decrement amount.** The user flow says "taps Brewed to decrement quantity" but does not define the decrement amount or whether it's a fixed serving or user-entered. The API spec resolves this conservatively (client sends absolute quantity), but the UX for selecting or defaulting a serving size is unspecified and will need a decision before implementation.
