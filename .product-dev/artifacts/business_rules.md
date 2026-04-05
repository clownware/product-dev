# Business Rules — Tea Tracker

Source prompt: `define-business-rules`
Generated: 2026-04-04

---

## BR-001 — Collection Sort Order (Attention Priority)

**Name:** Attention Priority Sort

**Trigger:** Every call to `GET /v1/teas` (collection overview load).

**Logic:**
Sort all non-finished teas in the following priority order (ascending priority number = top of list):

1. `freshness_status = stale` AND `status = opened` — most urgent, tea is past window
2. `freshness_status = warning` AND `status = opened` — attention needed soon
3. `freshness_status = fresh` AND `status = opened` — opened but not urgent
4. `status = sealed` — not yet opened, no freshness clock running; sorted by `created_at DESC` within this group

Within each priority group, secondary sort is `opened_at ASC` (longest-opened first) for groups 1–3, and `created_at DESC` for group 4.

**Dependencies:** BR-002 (freshness_status derivation must be computed before sort).

**Exceptions:** Teas with `status = finished` are excluded from this sort entirely — they are filtered out of the default collection response.

**Edge cases:**
- Tea with `status = opened` and `opened_at = null`: treat as `freshness_status = null`, sort at the bottom of the opened group. Assumption: `opened_at` should always be set when status is opened (enforced at write), so this is a data integrity fallback only.
- Tea with `quantity_g = 0` and `status = opened`: still subject to freshness sort — quantity reaching zero does not auto-close the tea.

**Violation handling:** N/A — this is a read-time computation, not a writable constraint.

**Business objective:** Surfaces the "what needs attention" read immediately on app open (core objective: confident inventory decisions without memory overhead).

---

## BR-002 — Freshness Status Derivation

**Name:** Freshness Status Calculation

**Trigger:** Computed at read time on any Tea with `status = opened`. Applied during `GET /v1/teas` and `GET /v1/teas/:id`.

**Logic:**

```
effective_window = tea.freshness_window_days ?? TYPE_DEFAULTS[tea.type]
days_open = CURRENT_DATE - tea.opened_at

if days_open <= (effective_window * 0.67):
    freshness_status = "fresh"
elif days_open <= effective_window:
    freshness_status = "warning"
else:
    freshness_status = "stale"
```

Warning threshold: 67% of the freshness window elapsed. Rationale: gives the user approximately one-third of the window as a "brew soon" nudge, which aligns with the user flow description ("opened 3 weeks ago, brew soon" for a 30-day green tea = 21 days = 70% — close enough to justify this threshold).

**Type defaults:**

| Type | Default window (days) |
|------|-----------------------|
| `green` | 30 |
| `white` | 60 |
| `oolong` | 45 |
| `black` | 180 |
| `puerh` | 730 |
| `herbal` | 90 |
| `other` | 90 |

**Dependencies:** Requires `tea.opened_at` and `tea.type` to be set.

**Exceptions:**
- `status = sealed`: `freshness_status = null`, `days_since_opened = null` — freshness clock has not started
- `status = finished`: `freshness_status = null` — tea is done, no urgency signal needed
- `opened_at = null` with `status = opened`: `freshness_status = null` — treat as data gap, do not crash or guess

**Violation handling:** N/A — read-only derivation.

**Business objective:** Drives the urgency nudges that are the product's core value proposition ("what's going stale"). The 67% warning threshold is the key tunable — if user testing shows it fires too early or too late, this is the first value to adjust.

---

## BR-003 — Opened Date Requirement

**Name:** Status-to-Date Consistency

**Trigger:** Any write to a Tea (`POST /v1/teas`, `PATCH /v1/teas/:id`) where `status = opened`.

**Logic:**
- If `status` is being set to `opened` and `opened_at` is not provided: default `opened_at` to `CURRENT_DATE` (server-side). This matches the user flow step 3 behavior ("defaults to sealed, today's date").
- If `opened_at` is explicitly provided: validate it is not a future date (must be `<= CURRENT_DATE`).
- If `status` is being set back to `sealed` from `opened`: `opened_at` must be cleared to null on the same write. The server should enforce this — not silently leave a stale `opened_at` value.

**Dependencies:** None.

**Exceptions:** When updating a tea from `opened` → `finished`, `opened_at` is retained (preserves history).

**Violation handling:**
- Future `opened_at` date: `400 VALIDATION_FAILED` with `field: "opened_at"`, `issue: "cannot_be_future_date"`
- Setting `status=sealed` while `opened_at` is already set without clearing it: `422 UNPROCESSABLE`

**Business objective:** Ensures the freshness clock (BR-002) has accurate start data. An `opened_at` date in the future would produce a negative `days_since_opened` and break the entire freshness model.

---

## BR-004 — Quantity Floor

**Name:** Quantity Cannot Go Negative

**Trigger:** Any write that sets `tea.quantity_g`.

**Logic:**
- `quantity_g` must be `>= 0` at all times.
- The client sends the absolute target value (not a delta). The server validates the value is non-negative.
- There is no enforcement that `quantity_g > 0` when `status = opened` — a tea can have zero grams remaining while still open (user may want to mark it finished separately, or may track it without quantity).

**Dependencies:** None.

**Exceptions:** `quantity_g = null` is explicitly valid — means the user has chosen not to track quantity for this tea. This is not the same as 0.

**Violation handling:** `400 VALIDATION_FAILED` with `field: "quantity_g"`, `issue: "min_value_0"`

**Business objective:** Protects data integrity. Negative gram counts are meaningless and would surface confusing UI states.

---

## BR-005 — Vendor Uniqueness Per User

**Name:** No Duplicate Vendor Names Per User

**Trigger:** `POST /v1/vendors` (vendor creation).

**Logic:**
- Before creating a vendor, check for an existing vendor with the same name under the same `user_id`.
- Comparison is case-insensitive: "Yunnan Sourcing" and "yunnan sourcing" are treated as the same vendor.
- If a match is found, return `409 CONFLICT` rather than creating a duplicate.

**Dependencies:** None.

**Exceptions:** None — this rule has no exceptions. Duplicate vendor names would break autocomplete UX and make vendor-tea traceability ambiguous.

**Violation handling:** `409 CONFLICT` with `error.code: "CONFLICT"`, `error.message: "A vendor with this name already exists"`. The client should surface this as an autocomplete suggestion: "Did you mean [existing vendor name]?" rather than a raw error.

**Business objective:** Preserves the vendor-tea connection thread (core objective). If duplicate vendors accumulate, the traceability feature becomes unreliable.

---

## BR-006 — Resource Ownership Scoping

**Name:** User Data Isolation

**Trigger:** Every authenticated API request that reads or writes a Tea or Vendor.

**Logic:**
- All read queries must include `WHERE user_id = [JWT sub claim]`.
- All writes must set `user_id = [JWT sub claim]` (server-side, never from request body).
- Any request for a resource whose `user_id` does not match the JWT `sub` returns `403 FORBIDDEN` (not `404`) to avoid leaking the existence of other users' data.

**Exception:** If the resource ID does not exist at all (no row in database), return `404 NOT_FOUND`. Only return `403` when the row exists but belongs to another user.

**Dependencies:** Auth model (JWT with `sub` claim).

**Violation handling:** `403 FORBIDDEN` on ownership mismatch; `404 NOT_FOUND` on non-existent resource.

**Business objective:** Single-user collection privacy. The product is explicitly not a social platform — one user must never be able to access another's collection.

---

## BR-007 — Tea Status Transition Rules

**Name:** Valid Status Transitions

**Trigger:** Any `PATCH /v1/teas/:id` that includes a `status` field change.

**Logic — allowed transitions:**

| From | To | Allowed |
|------|----|---------|
| `sealed` | `opened` | Yes — user opens the tea |
| `sealed` | `finished` | Yes — tea discarded without opening |
| `opened` | `finished` | Yes — tea consumed or discarded |
| `opened` | `sealed` | Yes — user corrects a mistake (cleared `opened_at` required) |
| `finished` | `opened` | No — finished is a terminal state |
| `finished` | `sealed` | No — finished is a terminal state |

**Dependencies:** BR-003 (opened_at handling on transition to/from `opened`).

**Exceptions:** No exceptions to the terminal-state rule. If a user accidentally marks something finished, they should delete it and re-add rather than revive it — this keeps state history clean.

**Violation handling:** `422 UNPROCESSABLE` with `error.message: "Cannot transition from finished to [target status]"`

**Business objective:** Prevents ghost teas from re-entering the active collection and polluting the freshness overview with stale data.
