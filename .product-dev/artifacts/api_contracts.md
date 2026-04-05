# API Contracts — Tea Tracker

Source prompt: `define-api-endpoints`
Generated: 2026-04-04

Context gate: "Software product with client-server architecture" — PASSES. This is a mobile/web app with a REST API backend.

---

## Auth Model

**Mechanism:** JSON Web Tokens (JWT), Bearer scheme.

**Token lifecycle:**
- Access token: 24-hour TTL, signed HS256, issued on login
- Refresh token: 30-day TTL, stored server-side (allows revocation), rotated on use
- Tokens carry `sub` (user.id, UUID v4) and `iat`/`exp` claims

**Public endpoints** (no token required): `POST /v1/auth/register`, `POST /v1/auth/login`

**Authenticated endpoints** (Bearer token required in `Authorization` header): all others

**Token revocation:** Refresh token invalidated on logout and on password change. Access tokens are short-lived and not individually revocable — 24-hour TTL is the revocation window.

---

## Error Contract

All error responses share this shape:

```json
{
  "error": {
    "code": "string — machine-readable slug, e.g. VALIDATION_FAILED",
    "message": "string — human-readable description",
    "details": [
      {
        "field": "string — dot-path to the offending field, e.g. 'name'",
        "issue": "string — what's wrong, e.g. 'required', 'max_length_exceeded'"
      }
    ]
  }
}
```

`details` is present only on `400` validation errors. It is an empty array (not omitted) for all other error codes.

**Standard error codes used across endpoints:**

| HTTP Status | `error.code` | When |
|-------------|--------------|------|
| 400 | `VALIDATION_FAILED` | Request body fails field-level validation |
| 401 | `UNAUTHORIZED` | Missing, malformed, or expired access token |
| 403 | `FORBIDDEN` | Token valid but resource belongs to another user |
| 404 | `NOT_FOUND` | Resource ID does not exist or is not visible to caller |
| 409 | `CONFLICT` | Uniqueness constraint violation (e.g. duplicate vendor name) |
| 422 | `UNPROCESSABLE` | Request is valid but violates a business rule |
| 429 | `RATE_LIMITED` | Too many requests from this client |
| 500 | `INTERNAL_ERROR` | Unexpected server fault |

---

## Endpoint Inventory

| Method | Route | Purpose | Flow Step | Auth |
|--------|-------|---------|-----------|------|
| POST | `/v1/auth/register` | Create user account | Pre-flow / onboarding | No |
| POST | `/v1/auth/login` | Exchange credentials for tokens | Pre-flow / onboarding | No |
| POST | `/v1/auth/refresh` | Rotate access token using refresh token | Session maintenance | No (uses refresh token) |
| POST | `/v1/auth/logout` | Revoke refresh token | Session end | Yes |
| GET | `/v1/teas` | Load collection overview | Flow step 1 — overview screen load | Yes |
| POST | `/v1/teas` | Add a new tea | Flow step 2–3 — Save in Add Tea form | Yes |
| GET | `/v1/teas/:id` | Load tea detail | Flow step 5 — Tea Detail screen | Yes |
| PATCH | `/v1/teas/:id` | Update tea fields | Flow step 5 — Edit, or "Brewed" decrement | Yes |
| DELETE | `/v1/teas/:id` | Remove tea from collection | Tea Detail — mark as finished / delete | Yes |
| GET | `/v1/vendors` | List user's vendors for autocomplete | Flow step 2 — vendor field autocomplete | Yes |
| POST | `/v1/vendors` | Create a new vendor | Flow step 2 — new vendor entered and saved | Yes |

---

## Endpoint Specifications

---

### POST /v1/auth/register

**Purpose:** Create a new user account.

**Request headers:** `Content-Type: application/json`

**Request body:**
```json
{
  "email": "string, required — RFC 5321, max 254 chars, lowercased before storage",
  "password": "string, required — min 8 chars, max 72 chars (bcrypt limit)"
}
```

**Response 201:**
```json
{
  "user": {
    "id": "uuid v4",
    "email": "lena@example.com",
    "created_at": "2026-04-04T14:00:00Z"
  },
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "access_token_expires_at": "2026-04-05T14:00:00Z"
  }
}
```

**Errors:**
- `400 VALIDATION_FAILED` — email malformed, password too short or too long
- `409 CONFLICT` — email already registered

**Notes:** Email is lowercased before uniqueness check and storage. Password is never echoed in any response.

---

### POST /v1/auth/login

**Purpose:** Authenticate a user and issue tokens.

**Request headers:** `Content-Type: application/json`

**Request body:**
```json
{
  "email": "string, required",
  "password": "string, required"
}
```

**Response 200:**
```json
{
  "user": {
    "id": "uuid v4",
    "email": "lena@example.com"
  },
  "tokens": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "access_token_expires_at": "2026-04-05T14:00:00Z"
  }
}
```

**Errors:**
- `400 VALIDATION_FAILED` — missing fields
- `401 UNAUTHORIZED` — credentials do not match any account (do not distinguish email-not-found from wrong-password in the response message — prevents user enumeration)

---

### POST /v1/auth/refresh

**Purpose:** Exchange a valid refresh token for a new access token. Rotates the refresh token (old token invalidated on use).

**Request headers:** `Content-Type: application/json`

**Request body:**
```json
{
  "refresh_token": "string, required"
}
```

**Response 200:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "access_token_expires_at": "2026-04-06T14:00:00Z"
}
```

**Errors:**
- `401 UNAUTHORIZED` — refresh token missing, malformed, expired, or already revoked

---

### POST /v1/auth/logout

**Purpose:** Revoke the current refresh token, ending the session.

**Request headers:** `Authorization: Bearer <access_token>`, `Content-Type: application/json`

**Request body:**
```json
{
  "refresh_token": "string, required"
}
```

**Response 204:** No body.

**Errors:**
- `401 UNAUTHORIZED` — access token invalid

---

### GET /v1/teas

**Purpose:** Load the user's collection overview. Returns all teas for the authenticated user, sorted by attention priority (freshness urgency desc, then `created_at` desc). Includes computed fields needed to render the overview grid.

**Request headers:** `Authorization: Bearer <access_token>`

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | enum: `sealed\|opened\|finished` | none (all) | Filter by `tea.status` |
| `limit` | integer, 1–100 | 50 | Page size |
| `cursor` | string, opaque | none | Cursor for next page (cursor-based pagination) |

**Response 200:**
```json
{
  "teas": [
    {
      "id": "uuid v4",
      "name": "Gyokuro Imperial",
      "type": "green",
      "status": "opened",
      "quantity_g": 40,
      "vendor_id": "uuid v4 or null",
      "vendor_name": "Yunnan Sourcing",
      "opened_at": "2026-03-10",
      "days_since_opened": 25,
      "freshness_status": "warning",
      "effective_freshness_window_days": 30,
      "created_at": "2026-03-09T18:00:00Z",
      "updated_at": "2026-04-01T09:00:00Z"
    }
  ],
  "pagination": {
    "next_cursor": "string or null",
    "has_more": true
  }
}
```

**Computed fields in response** (not stored — calculated server-side):
- `days_since_opened`: `CURRENT_DATE - opened_at` when `status = opened`; `null` when `status = sealed`
- `freshness_status`: `fresh | warning | stale` — see Business Rules for derivation
- `effective_freshness_window_days`: `tea.freshness_window_days` if non-null, else type default
- `vendor_name`: denormalized from `vendor.name` for read performance; null when `vendor_id` is null

**Errors:**
- `401 UNAUTHORIZED`

**Notes:** The sort order is defined in Business Rules (BR-001). `finished` teas are excluded from the default response unless `status=finished` is passed — users don't need finished teas cluttering the overview.

**Assumption:** "finished" teas are retained in storage for historical reference but hidden from the default overview. The design artifacts don't explicitly state this but it's implied by "mark as finished" as a discrete action from delete.

---

### POST /v1/teas

**Purpose:** Add a new tea to the user's collection. Corresponds to the Save action in the Add Tea form (flow steps 2–3).

**Request headers:** `Authorization: Bearer <access_token>`, `Content-Type: application/json`

**Request body:**
```json
{
  "name": "string, required — 1–200 chars, trimmed",
  "type": "enum, required — green|black|oolong|white|puerh|herbal|other",
  "vendor_id": "uuid v4, optional — must belong to authenticated user if provided",
  "status": "enum, optional — sealed|opened — default: sealed",
  "quantity_g": "integer, optional — min 0",
  "opened_at": "string YYYY-MM-DD, conditional — required when status=opened",
  "purchased_at": "string YYYY-MM-DD, optional",
  "freshness_window_days": "integer, optional — min 1, overrides type default"
}
```

**Response 201:**
```json
{
  "tea": {
    "id": "uuid v4",
    "name": "Gyokuro Imperial",
    "type": "green",
    "status": "sealed",
    "quantity_g": 100,
    "vendor_id": "uuid v4 or null",
    "vendor_name": "Yunnan Sourcing",
    "opened_at": null,
    "purchased_at": "2026-04-04",
    "freshness_window_days": null,
    "effective_freshness_window_days": 30,
    "days_since_opened": null,
    "freshness_status": null,
    "created_at": "2026-04-04T14:00:00Z",
    "updated_at": "2026-04-04T14:00:00Z"
  }
}
```

**Errors:**
- `400 VALIDATION_FAILED` — name empty or over 200 chars, invalid type enum, opened_at missing when status=opened, quantity_g negative, opened_at is a future date
- `401 UNAUTHORIZED`
- `403 FORBIDDEN` — vendor_id belongs to a different user
- `404 NOT_FOUND` — vendor_id does not exist

**Notes:** `user_id` is set server-side from the JWT `sub` claim — never accepted from the client. `opened_at` defaults to today's date server-side when `status=opened` and `opened_at` is omitted (matching the form behavior described in user flow step 3).

---

### GET /v1/teas/:id

**Purpose:** Load full detail for a single tea. Corresponds to Tea Detail screen (flow step 5).

**Request headers:** `Authorization: Bearer <access_token>`

**Path parameters:** `id` — UUID v4

**Response 200:**
```json
{
  "tea": {
    "id": "uuid v4",
    "name": "Gyokuro Imperial",
    "type": "green",
    "status": "opened",
    "quantity_g": 40,
    "vendor_id": "uuid v4 or null",
    "vendor_name": "Yunnan Sourcing",
    "opened_at": "2026-03-10",
    "purchased_at": "2026-03-09",
    "freshness_window_days": null,
    "effective_freshness_window_days": 30,
    "days_since_opened": 25,
    "freshness_status": "warning",
    "notes": null,
    "created_at": "2026-03-09T18:00:00Z",
    "updated_at": "2026-04-01T09:00:00Z"
  }
}
```

**Errors:**
- `401 UNAUTHORIZED`
- `403 FORBIDDEN` — tea belongs to a different user
- `404 NOT_FOUND`

---

### PATCH /v1/teas/:id

**Purpose:** Update one or more fields on an existing tea. Used for two distinct flow actions: (1) general editing from Tea Detail, and (2) the "Brewed" action which decrements `quantity_g`.

**Request headers:** `Authorization: Bearer <access_token>`, `Content-Type: application/json`

**Path parameters:** `id` — UUID v4

**Request body** (all fields optional; only provided fields are updated — partial update semantics):
```json
{
  "name": "string, 1–200 chars, trimmed",
  "type": "enum — green|black|oolong|white|puerh|herbal|other",
  "vendor_id": "uuid v4 or null — null explicitly removes vendor association",
  "status": "enum — sealed|opened|finished",
  "quantity_g": "integer, min 0",
  "opened_at": "string YYYY-MM-DD",
  "purchased_at": "string YYYY-MM-DD",
  "freshness_window_days": "integer min 1, or null to revert to type default",
  "notes": "string max 1000 chars or null"
}
```

**Response 200:** Full tea object (same shape as `GET /v1/teas/:id` response).

**Errors:**
- `400 VALIDATION_FAILED` — field constraint violations (same rules as POST)
- `401 UNAUTHORIZED`
- `403 FORBIDDEN` — tea or vendor_id belongs to a different user
- `404 NOT_FOUND` — tea or vendor_id does not exist
- `422 UNPROCESSABLE` — business rule violation (e.g. setting status=sealed while opened_at is set; see BR-004)

**Notes:** The "Brewed" button in the user flow (step 5) is implemented as `PATCH /v1/teas/:id` with `{ "quantity_g": <current - serving_size> }`. The serving decrement logic lives on the client — the server accepts the absolute new value, not a delta. This avoids concurrent-write conflicts for a single-user app.

---

### DELETE /v1/teas/:id

**Purpose:** Permanently remove a tea from the collection. Distinct from marking `status=finished` — delete removes the record entirely.

**Request headers:** `Authorization: Bearer <access_token>`

**Path parameters:** `id` — UUID v4

**Response 204:** No body.

**Errors:**
- `401 UNAUTHORIZED`
- `403 FORBIDDEN`
- `404 NOT_FOUND`

---

### GET /v1/vendors

**Purpose:** List all vendors for the authenticated user. Used to populate the vendor autocomplete in the Add Tea form (flow step 2).

**Request headers:** `Authorization: Bearer <access_token>`

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string, max 200 chars | none | Prefix-match filter on `vendor.name` for autocomplete |
| `limit` | integer, 1–50 | 50 | Page size (50 is the hard max — a user with >50 vendors is an edge case, not a design target per persona) |

**Response 200:**
```json
{
  "vendors": [
    {
      "id": "uuid v4",
      "name": "Yunnan Sourcing",
      "created_at": "2026-01-10T12:00:00Z"
    }
  ]
}
```

**Errors:**
- `401 UNAUTHORIZED`

**Notes:** No pagination cursor — vendor lists are small (persona has 4–6 vendors; hard max 50 enforced server-side). Sorted alphabetically by `name`. The `q` filter is case-insensitive prefix match, not full-text search.

---

### POST /v1/vendors

**Purpose:** Create a new vendor for the authenticated user. Triggered when the user types a vendor name not in the autocomplete list and saves a tea (flow step 2–3).

**Request headers:** `Authorization: Bearer <access_token>`, `Content-Type: application/json`

**Request body:**
```json
{
  "name": "string, required — 1–200 chars, trimmed"
}
```

**Response 201:**
```json
{
  "vendor": {
    "id": "uuid v4",
    "name": "Yunnan Sourcing",
    "created_at": "2026-04-04T14:00:00Z"
  }
}
```

**Errors:**
- `400 VALIDATION_FAILED` — name empty or over 200 chars
- `401 UNAUTHORIZED`
- `409 CONFLICT` — vendor with this name already exists for this user (case-insensitive match)

**Notes:** Vendor creation is a separate action from tea creation. The client should: (1) POST /v1/vendors to create vendor, (2) use the returned `vendor.id` in the subsequent POST /v1/teas body. If the user selects an existing vendor from autocomplete, step 1 is skipped.

---

## Excluded Endpoints

The following were considered and explicitly excluded because they have no corresponding step in the user flow:

- `PUT /v1/vendors/:id` (rename vendor) — not in MVP flow
- `DELETE /v1/vendors/:id` — not in MVP flow
- `GET /v1/users/me` — not needed for MVP screens; user identity is carried in the token
- `PATCH /v1/users/me` (profile edit) — not in scope
- Any bulk or batch endpoints — collection size does not warrant them
