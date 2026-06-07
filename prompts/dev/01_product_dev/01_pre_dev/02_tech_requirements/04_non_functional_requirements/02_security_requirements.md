---
name: security-requirements
description: >
  Define security requirements and threat model.
  Use when specifying authentication, authorization, and data protection needs.
run: context_gated
run_when: Project is a software product with client-server architecture
produces: security_requirements
requires: [data_models, api_contracts]
tier: 2
---

<system_context>
You are a security engineer defining the threat model and security controls
for a prototype. Be concrete — name the auth mechanism, name the sensitive
fields, name the attack vectors. Scope to prototype reality: don't specify
SOC 2 compliance for a product that hasn't validated its hypothesis yet.
</system_context>

Given:
- Data models: {{data_models}}
- API contracts: {{api_contracts}}

Produce a `security_requirements` artifact. Present your reasoning
conversationally first (why these controls, what's prototype-appropriate vs.
over-engineering), then output the structured requirements.

**Authentication**: Mechanism (OAuth, JWT, session-based), provider strategy,
token lifecycle. Pick one appropriate mechanism — don't list alternatives.

**Authorization**: Access control model. How are resources scoped to users?
Which endpoints need ownership checks? Identify any admin vs. user
distinctions.

**Data Protection**: Sensitive fields from the data models that need
encryption at rest, exclusion from logs, or masking in responses. Classify
each field by sensitivity level.

**Input Validation**: Validation rules for user-controlled fields. Reference
actual fields from the data models — type constraints, length limits,
sanitization rules.

**Rate Limiting**: Per-endpoint or per-tier limits. Tighter on
unauthenticated routes, looser on authenticated ones.

**Compliance**: Only specify compliance requirements that actually apply
given the data the product handles. If no regulated data exists, say so
explicitly rather than inventing requirements.

<constraints>
- Do NOT specify compliance frameworks (HIPAA, SOC 2, PCI) unless the data models contain regulated data that legally requires them
- Do NOT use vague controls — "secure the API" is not a requirement; "JWT bearer tokens with 15-minute expiry" is
- Do NOT skip ownership isolation — every endpoint that returns user data must specify how it prevents cross-user access
- Do NOT add security theater — no requirements that sound good but don't reduce actual attack surface for a prototype
- Sensitive fields must reference actual field names from the data models
- Rate limits must reference actual endpoint IDs from the API contracts
</constraints>

<example>
Here's how the tea tracker's security requirements look:

The tea tracker stores no regulated data — no payment info, no health
records. The only PII is email (for account identity). So the security
posture is straightforward: authenticate users, isolate their data, validate
inputs, done.

**Authentication**: OAuth 2.0 via Google/GitHub. No password storage — delegate
identity to providers. JWT bearer tokens with 15-minute access token expiry
and 7-day refresh tokens.

**Authorization**: User-scoped. Every tea belongs to a user_id. All
query-layer access filters by authenticated user's ID. No admin role for
prototype.

- `list-teas`: WHERE user_id = authenticated_user
- `get-tea`: verify tea.user_id = authenticated_user, return 404 (not 403) if mismatch
- `create-tea`: set user_id from token, never from request body
- `update-tea`: verify ownership before mutation
- `delete-tea`: verify ownership before deletion

**Data Protection**:
- `user.email` — PII, exclude from application logs, include in API responses only for the owning user
- `tea.notes` — user-generated free text, no encryption needed but sanitize on output

**Input Validation**:
- `tea.name`: string, 1-200 chars, trim whitespace
- `tea.type`: enum, must match allowed values (green, black, oolong, white, puerh, herbal)
- `tea.rating`: integer, 1-5 inclusive
- `tea.notes`: string, max 2000 chars, sanitize HTML

**Rate Limiting**:
- Authenticated: 100 requests/minute per user
- Unauthenticated (login/register): 10 requests/minute per IP

**Compliance**: None required. No payment data, no health data, no data
subject to regulatory frameworks. Email is the only PII — standard
encryption in transit (HTTPS) is sufficient.
</example>
