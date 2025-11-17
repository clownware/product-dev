---
title: "Prompt: {{title}}"
type: prompt
status: complete
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}
category: [design|development|project_management|research|creative]
subcategory: [ux|ui|vscode|role|llm_eval|writing]
target_model: ["GPT-4o"]
use_case: ""
source: [original|adapted|collaborative]
effectiveness_score: # optional: 1-10
ai_analyzed: yes
ai_version: "Claude 3.7"
ai_feedback:
  strengths: []
  blind_spots: []
  next_questions: []
related_sources: []
tags: []
ai_tags: []
---
### 1 — Concrete apps that fit this stack

|Example app|Why the stack is a sweet spot|
|---|---|
|**Freelancer-CRM / Client portal** – contacts, invoices, simple ticketing|CRUD-heavy, low user-count. HTMX tables & inline-edit forms feel “SPA-like” without shipping React. Go + sqlc keeps logic type-safe; single-region Fly VM + SQLite is plenty.|
|**Conference schedule & call-for-papers site**|Mostly read traffic with a few admin screens. HTMX handles live-filtering of sessions, Alpine drives modal “submit talk” form. Background emails (goroutine or Fly cron) confirm submissions.|
|**Internal Ops dashboard for an e-commerce store**|Needs fast filters/exports on orders. sqlc-generated queries hit Postgres; HTMX swaps table body on filter change. Role-based auth (admin, support) fits Phase 6.|
|**Tiny SaaS (URL shortener + analytics)**|2 tables, 3 endpoints. HTMX makes real-time click stats feel live; Go’s raw performance serves redirect traffic easily.|
|**Newsletter + content CMS**|Staff log in, write posts in markdown. HTMX provides instant preview panes; background goroutine batches email sends. LiteFS-replicated SQLite keeps latency low at the edge.|
|**One-off public data explorer** (open-data CSV → searchable site)|Upload CSV to R2, import into SQLite, serve faceted search via HTMX without writing JS bundles.|

---

### 2 — Reusable “base” application template

Think **“Batteries-included, Opinionated, but Trim”**. Start a repo called `go-htmx-starter` with:

csharp

CopyEdit

`. ├── cmd/ │   └── web/            # main.go ─ bootstrap & router ├── internal/ │   ├── domain/         # Go structs (business logic) │   ├── db/             # sqlc-generated code + migrations │   ├── handler/        # HTTP handlers, grouped per feature │   └── middleware/ ├── web/                # Tailwind, HTMX, Alpine, templates │   ├── layouts/ │   ├── partials/ │   └── static/ ├── scripts/            # Taskfile tasks & Fly deploy script ├── migrations/ ├── testdata/ └── go.mod`

**Features baked-in**

- **Auth scaffold** – email + password, bcrypt, session cookies, CSRF tokens.
    
- **Tailwind pipeline** – `npm dlx tailwindcss -i ./web/input.css -o ./web/static/app.css --watch`.
    
- **HTMX helpers** – Go funcs for `HX-Redirect`, `HX-Trigger`, `HX-Retarget`.
    
- **Flash messages** – via Alpine + HTMX trigger.
    
- **Generic CRUD module** – example `Product` model with list/create/edit/delete endpoints and table partial (replace to suit).
    
- **Taskfile targets**
    
    - `task dev`: air + Tailwind in watch mode
        
    - `task db:up`: spin up SQLite or connect to Supabase/Postgres
        
    - `task fly:deploy`: build & release.
        
- **Make-it-yours checklist** in README: change module path, rename entity, choose DB driver.
    

Fork once, replace the sample entity, keep the plumbing.

---

### 3 — Using **Supabase Postgres** and **Firebase Auth** with this stack

|Question|Short answer|
|---|---|
|_Can I point sqlc-generated code at Supabase Postgres?_|**Yes.** Supabase is just Postgres + extras. Grab the connection string (`postgresql://user:pass@db.supabase.co:5432/postgres`), set as `DATABASE_URL`, and sqlc-generated repos work unchanged. Latency will be a bit higher than co-locating Postgres on Fly, but fine for dashboards.|
|_Can the Go server delegate auth to Firebase?_|**Yes, but plan the flow.** You’ll: 1) run Firebase Auth in the browser, 2) send the ID token in an `Authorization` header or cookie, 3) verify it in Go with `firebase.google.com/go/v4/auth`, then 4) create a local session/cookie if you still want HTMX to work with server-side redirects.|
|_Are Supabase + Firebase “rational” choices?_|_Pros_: zero infra to manage, SOC2/GDPR off your plate, built-in email/password + social login (Firebase) and row-level policies (Supabase).  <br>_Cons_: two vendors instead of one; extra network hops; Supabase Auth tokens ≠ Firebase tokens, so you’d be mixing systems. If you already like Firebase UX, consider letting **Supabase handle both Postgres **and** Auth** to keep a single identity provider.|

**When it shines**

- Hack-day prototypes: spin up Supabase in one click, skip migrations for day 1.
    
- Mobile companion apps: reuse the same Firebase Auth token in your Go backend.
    
- Teams without DBA/SRE: let Supabase scale the DB.
    

**Watch-outs**

- Out-of-region DB adds ~50-100 ms RTT to every query if your Fly app and Supabase aren’t in the same region.
    
- Firebase Auth verification adds an HTTP call the first time per key-set rotation (cache keys).
    
- RLS/Policies in Supabase are bypassed if you connect with service keys from Go; enforce rules in code or switch to the PostgREST path.
    

---

### 4 — What the template can flex into (non-enterprise)

|Extension idea|Extra you’d add|
|---|---|
|**Multi-tenant SaaS**|Add `account_id` column to every table via sqlc templates; mount Alpine-powered settings page; use Fly’s Postgres + row-level ACL.|
|**Public-facing marketing site + admin**|Keep same code-base: `/` routes hit cached HTML; `/admin` is HTMX-driven CRUD secured by cookie auth.|
|**Real-time dashboard**|Use Server-Sent Events (`hx-sse`) instead of WebSockets; goroutine pumps updates every N seconds.|
|**File-sharing micro-service**|Plug Cloudflare R2 adapter into the storage layer, keep metadata in SQLite.|
|**Email drip tool**|Add Asynq + Redis when cron goroutines aren’t enough; worker runs `SendCampaign` jobs pulled from `campaigns` table.|

---

### 5 — Decision grid: built-in auth vs Supabase vs Firebase

|Feature need|Built-in sessions|Supabase Auth|Firebase Auth|
|---|---|---|---|
|Zero external calls|✅|❌|❌|
|Social login OOTB|➖ (add separately)|✅|✅|
|Row-level DB security|❌ (code it)|✅ (RLS)|❌|
|Works well with HTMX redirects|✅|✅* (if you swap session after token)|✅*|
|Price at hobby scale|free|free tier|free tier|
|Local dev offline|✅|✅ (`supabase start`)|❌ (needs emulator)|

*You’ll usually exchange the ID token for a normal server-side session cookie so HTMX can keep using cookies transparently.

---

#### TL;DR

- **Template to fork:** `go-htmx-starter` with Chi/Echo, Tailwind, HTMX patterns, session auth, sqlc, Taskfile, Fly deploy.
    
- **Great fits:** internal dashboards, small SaaS, content CMS, ops tools.
    
- **Supabase Postgres** works out of the box with sqlc; just mind region latency.
    
- **Firebase Auth** is fine if you value its UI and MFA, but adds a token-verification step; Supabase Auth gives you DB + auth in one place.
    
- Pick the mix that minimizes _your_ operational burden—this stack is thin enough to stay happy with any of the above.