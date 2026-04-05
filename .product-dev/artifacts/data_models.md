# Data Models — Tea Tracker

Source prompt: `define-data-models`
Generated: 2026-04-04

---

## Entity Overview

| Entity | Description |
|--------|-------------|
| `User` | An authenticated account that owns a tea collection |
| `Tea` | A single tea entry in the user's collection |
| `Vendor` | A tea supplier associated with one or more teas |

Three entities are sufficient for the MVP. The user flow does not require brewing sessions, purchase orders, or any social construct. A `Vendor` is a first-class entity (not an inline string) because the user flow requires autocomplete from previously entered vendors, and the core objective requires tracing any tea back to its vendor.

---

## 1. User

Represents an authenticated account. The product is single-user-per-collection; no sharing or collaboration is in scope.

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `id` | UUID v4 | Yes | Primary key, immutable | Server-generated |
| `email` | string, max 254 chars | Yes | Unique, lowercase, RFC 5321 format | Used for auth identity |
| `password_hash` | string, max 255 chars | Yes | bcrypt hash, never returned in API responses | Store hash only |
| `created_at` | timestamp, ISO 8601 UTC | Yes | Immutable, server-set on creation | |
| `updated_at` | timestamp, ISO 8601 UTC | Yes | Server-set on every write | |

**Relationships:**
- One User has many Teas (`tea.user_id → user.id`)
- One User has many Vendors (`vendor.user_id → user.id`)

**Unique constraints:** `email` globally unique.

**Indexes:** `email` (unique index, used on login lookup).

**Special handling:** `password_hash` must never appear in any API response body. Treat as write-only at the application layer.

---

## 2. Tea

The core entity. Represents one distinct tea in the user's collection. "Distinct" means one entry per product — not per serving. Quantity tracks remaining amount in grams.

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `id` | UUID v4 | Yes | Primary key, immutable | Server-generated |
| `user_id` | UUID v4 | Yes | Foreign key → `user.id`, non-null | Scopes to collection owner |
| `vendor_id` | UUID v4 | No | Foreign key → `vendor.id`, nullable | Null when vendor not specified |
| `name` | string, max 200 chars | Yes | Non-empty, trimmed | e.g. "Gyokuro Imperial" |
| `type` | enum | Yes | One of: `green`, `black`, `oolong`, `white`, `puerh`, `herbal`, `other` | Matches Add Tea Form selector |
| `status` | enum | Yes | One of: `sealed`, `opened`, `finished` | Defaults to `sealed` on creation |
| `quantity_g` | integer | No | Min 0, nullable | Null means quantity not tracked; 0 means empty |
| `opened_at` | date (YYYY-MM-DD) | No | Nullable; required when `status = opened` | Date the seal was broken |
| `purchased_at` | date (YYYY-MM-DD) | No | Nullable | Date of purchase or arrival |
| `freshness_window_days` | integer | No | Min 1, nullable | Per-tea override of the type default freshness window |
| `notes` | string, max 1000 chars | No | Nullable, trimmed | Free-text field not in MVP flow but reserved |
| `created_at` | timestamp, ISO 8601 UTC | Yes | Immutable, server-set | |
| `updated_at` | timestamp, ISO 8601 UTC | Yes | Server-set on every write | |

**Relationships:**
- Many Teas belong to one User
- Many Teas optionally belong to one Vendor (nullable)

**Unique constraints:** None at the database level — the solution concept explicitly allows duplicate tea names (same tea from different vendors or different vintages).

**Indexes:**
- `(user_id)` — all collection queries are scoped by user
- `(user_id, status)` — overview filtering by status (sealed/opened/finished)
- `(user_id, opened_at)` — freshness sort on the overview grid
- `(vendor_id)` — vendor detail lookup (future)

**Computed / derived attributes** (not stored, calculated at read time):
- `days_since_opened`: integer — `CURRENT_DATE - opened_at` when `status = opened`
- `freshness_status`: enum (`fresh`, `warning`, `stale`) — derived from `days_since_opened` vs `freshness_window_days` (or type default). See Business Rules.
- `effective_freshness_window_days`: integer — `freshness_window_days` if set, otherwise the type default from Business Rules.

---

## 3. Vendor

A tea supplier. Scoped to the user — vendors are not shared across accounts. This enables per-user autocomplete without a global vendor directory.

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| `id` | UUID v4 | Yes | Primary key, immutable | Server-generated |
| `user_id` | UUID v4 | Yes | Foreign key → `user.id`, non-null | Scoped to collection owner |
| `name` | string, max 200 chars | Yes | Non-empty, trimmed, unique per user | e.g. "Yunnan Sourcing" |
| `created_at` | timestamp, ISO 8601 UTC | Yes | Immutable, server-set | |
| `updated_at` | timestamp, ISO 8601 UTC | Yes | Server-set on every write | |

**Relationships:**
- One Vendor belongs to one User
- One Vendor has many Teas (via `tea.vendor_id`)

**Unique constraints:** `(user_id, name)` — a user cannot have two vendors with the same name (case-insensitive comparison enforced at application layer before write).

**Indexes:**
- `(user_id)` — autocomplete queries list all vendors for a user
- `(user_id, name)` — uniqueness enforcement lookup

---

## Relationship Diagram (text)

```
User ──< Tea >── Vendor
         (user_id)    (vendor_id, nullable)
         (vendor_id)
```

One User owns many Teas. One Vendor (scoped to a User) is associated with zero or many Teas. A Tea may exist without a Vendor.

---

## Type Defaults for Freshness Windows

These are constants used in business logic, not stored per-row, but documented here as they directly derive from the Tea `type` enum:

| Tea Type | Default Freshness Window |
|----------|--------------------------|
| `green` | 30 days after opening |
| `white` | 60 days after opening |
| `oolong` | 45 days after opening |
| `black` | 180 days after opening |
| `puerh` | 730 days after opening (aging tea — long window) |
| `herbal` | 90 days after opening |
| `other` | 90 days after opening |

Assumption: freshness windows are reasonable defaults derived from tea preservation conventions. The `freshness_window_days` field on Tea allows per-entry overrides if users want finer control. This override field is not exposed in the MVP Add Tea form but is available via the edit flow.
