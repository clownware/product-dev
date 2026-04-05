# Non-Functional Requirements — Tea Tracker

Source prompt: `performance-requirements`
Generated: 2026-04-04

---

## Scale Basis

All targets are derived from the proto_persona and product constraints:
- Target user: a solo collector with 30–45 teas and 4–6 vendors
- Single-user collection (no shared data, no concurrent writes to the same collection)
- MVP target: 1–1,000 registered users at launch; 10,000 upper bound for initial infrastructure sizing
- Collection size hard ceiling: 500 teas per user (beyond this the product's UX premise breaks — a 500-tea collection needs faceted search, not a grid)

These are not enterprise-scale targets. Over-engineering for scale is explicitly out of scope for MVP.

---

## 1. Response Time Requirements

| Endpoint / Operation | P50 Target | P95 Target | Hard Timeout |
|----------------------|-----------|-----------|--------------|
| `GET /v1/teas` (collection load, <=50 teas) | <200ms | <500ms | 5s |
| `POST /v1/teas` (add tea) | <300ms | <600ms | 5s |
| `PATCH /v1/teas/:id` (brewed / edit) | <200ms | <400ms | 5s |
| `GET /v1/teas/:id` (detail load) | <150ms | <300ms | 5s |
| `GET /v1/vendors` (autocomplete) | <100ms | <200ms | 3s |
| `POST /v1/vendors` | <200ms | <400ms | 5s |
| `POST /v1/auth/login` | <500ms | <1000ms | 10s |
| `POST /v1/auth/register` | <500ms | <1000ms | 10s |

**Rationale for vendor autocomplete being the strictest target:** The user flow identifies the vendor field autocomplete as friction-critical (flow step 2 — "less effort than a spreadsheet"). Autocomplete that lags noticeably breaks the add-tea interaction.

**Rationale for auth endpoints being more relaxed:** bcrypt password hashing is intentionally slow (work factor 12 recommended). Login/register are infrequent and users tolerate a brief wait.

All targets measured at the API server boundary, not including client-side network latency.

---

## 2. Throughput Requirements

| Scenario | Target |
|----------|--------|
| Sustained request rate (MVP launch, 1,000 users) | 10 requests/second |
| Peak burst (e.g. seasonal buying spike, many users adding teas simultaneously) | 50 requests/second for up to 60 seconds |
| Max concurrent authenticated sessions | 500 |

**Basis:** With 1,000 registered users and typical collector behavior (check app 1–2x/day, add 1–5 teas per session), sustained throughput will be well under 10 req/s. The 50 req/s burst target provides 5x headroom for growth without infrastructure changes.

---

## 3. Resource Utilization Targets

| Resource | Target (per server instance) | Alert Threshold |
|----------|------------------------------|-----------------|
| CPU | <40% average under sustained load | >70% for >5 minutes |
| Memory | <512MB for API process | >80% of available |
| Database connections | <20 concurrent per instance | >80% of pool size |
| Disk I/O | Not a primary constraint — read-heavy workload fits in DB cache | >80% saturation |
| Network egress | <1GB/day at 1,000 active users | >5GB/day (investigate) |

**Storage estimate:**
- Average tea record: ~500 bytes (all fields stored)
- 45 teas per user × 500 bytes = ~22KB per user
- 10,000 users × 22KB = ~220MB of tea data
- Vendor and user records add <10% overhead
- Total data volume at 10,000 users: <300MB — fits comfortably in a single database instance with no sharding concern

---

## 4. Availability and Reliability

| Metric | Target |
|--------|--------|
| Uptime | 99.5% monthly (~3.6 hours downtime/month acceptable for MVP) |
| Planned maintenance window | Off-peak (02:00–04:00 local time), with 24h notice |
| Data durability | No data loss for committed writes (standard ACID guarantees required) |
| Backup frequency | Daily automated database backup, retained 30 days |
| Recovery time objective (RTO) | <4 hours from backup |
| Recovery point objective (RPO) | <24 hours (daily backup cadence) |

99.5% uptime is appropriate for a personal productivity tool in MVP. Tea tracking is not life-critical; a few hours of downtime is tolerable. Targeting 99.9% from day one would over-engineer the deployment.

---

## 5. Scalability Expectations

**Vertical scaling first.** The application does not require horizontal scale at MVP. A single well-provisioned server handles the stated throughput targets.

**Horizontal scaling readiness:** The API should be stateless (all session state in JWTs + database). This allows adding more API server instances behind a load balancer without application changes.

**Database:** Single primary instance sufficient through 10,000 users. Add read replica if `GET /v1/teas` query times degrade beyond P95 targets. No sharding anticipated below 1M records.

**Growth trigger for re-evaluation:** If registered users exceed 10,000 or sustained throughput exceeds 40 req/s, revisit infrastructure sizing.

---

## 6. Degradation Behavior Under Load

| Scenario | Behavior |
|----------|----------|
| Database connection pool exhausted | Return `503 Service Unavailable` immediately with `Retry-After: 5` header — do not queue indefinitely |
| Response time >hard timeout | Return `503` with `error.code: "TIMEOUT"` — do not return partial data |
| Rate limit hit by a single client | Return `429 Too Many Requests` with `Retry-After: 60` header |
| Auth service unavailable | Fail all authenticated endpoints with `503` — do not allow unauthenticated access as fallback |

**Rate limit:** 60 requests per client IP per minute on all endpoints. Burst allowance: 20 requests in any 5-second window.

---

## 7. Monitoring and Alerting Thresholds

| Signal | Warning Threshold | Critical Threshold | Action |
|--------|------------------|--------------------|--------|
| API P95 response time | >500ms for 5 min | >2s for 2 min | Investigate query performance |
| Error rate (5xx) | >1% of requests over 5 min | >5% of requests over 1 min | Page on-call |
| Database query time | P95 >100ms for 5 min | P95 >500ms for 2 min | Investigate slow queries / missing indexes |
| CPU utilization | >70% for 5 min | >90% for 2 min | Scale or investigate |
| Failed login rate | >10 failures/minute from single IP | >50 failures/minute | Trigger IP-level rate limiting (brute force protection) |
| Disk usage | >70% of allocated | >90% of allocated | Provision additional storage |

**Minimum observable signals for MVP:**
- Request rate, P50/P95 latency, error rate — per endpoint
- Database query latency — P50/P95
- Active user sessions count
- Failed authentication attempts — for brute force detection

Application-level distributed tracing (e.g. OpenTelemetry) is recommended from day one. It is significantly harder to add tracing retroactively than to instrument at build time.
