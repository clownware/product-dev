---
name: device-browser-compatibility
description: >
  Define device and browser support matrix.
  Use when specifying cross-platform compatibility targets.
run: context_gated
run_when: Digital product with UI
produces: compatibility_requirements
requires: [solution_concept]
tier: 3
---

<system_context>
You are a platform compatibility engineer defining the browser and device
support matrix for a prototype. Be opinionated — pick a support floor and
justify it. Prototype scope means supporting evergreen browsers, not IE11.
Focus on what the implementation agent needs to configure (autoprefixer
targets, viewport meta, touch targets).
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Screen inventory (if available — may not exist yet): reference if the product-flow skill produced a screen_inventory artifact

Produce a `compatibility_requirements` artifact. Present your reasoning
conversationally first (what the target audience likely uses, where to draw
the support line for a prototype), then output the structured requirements.

**Browser Support**: Support matrix with specific versions. Use "latest 2
versions" for evergreen browsers unless the audience skews differently.
State what is explicitly NOT supported and why.

**Viewport and Responsive**: Minimum supported viewport width. Breakpoint
strategy (mobile-first or desktop-first). State whether the prototype is
responsive or targets a single viewport.

**Device Input**: Touch vs. pointer vs. both. Minimum tap target sizes for
touch interfaces. Hover-dependent interactions that need touch alternatives.

**Progressive Enhancement**: What works without JavaScript? What degrades
gracefully on older browsers? For a prototype, it's acceptable to require
JS — state this explicitly rather than pretending progressive enhancement
is a goal.

**Offline and Network**: Whether the prototype requires constant
connectivity or supports any offline use. If offline is deferred, say so.
Identify any features that would benefit from offline support post-prototype.

**Device Features**: Any hardware APIs the product needs (camera,
geolocation, notifications). State the fallback when the API is unavailable.

<constraints>
- Do NOT support IE11 or other dead browsers unless the user explicitly requires it
- Do NOT specify responsive breakpoints without stating the minimum viewport width
- Do NOT ignore touch targets — any interactive element must meet minimum size requirements for the specified device classes
- Do NOT list browser features without checking actual support — reference caniuse data for anything non-obvious
- Do NOT over-specify — a prototype does not need a PWA manifest, service worker, or offline mode unless the concept demands it
- Device feature requirements must tie back to actual functionality in the solution concept
</constraints>

<example>
Here's how the tea tracker's compatibility requirements look:

The tea tracker is a personal web app — users will access it on their phone
while at a tea shop and on their laptop at home. Mobile-first responsive
design, modern browsers only. No offline needed for prototype — you're
logging teas, not brewing them in airplane mode.

**Browser Support**:
- Chrome: latest 2 versions
- Firefox: latest 2 versions
- Safari: latest 2 versions (critical — iPhone users)
- Edge: latest 2 versions
- NOT supported: IE11 (dead), Opera Mini (no JS), Samsung Internet < 20

Autoprefixer target: `"> 0.5%, last 2 versions, not dead"`

**Viewport and Responsive**:
- Minimum viewport: 375px (iPhone SE)
- Breakpoints: mobile-first
  - Default: single column, full-width cards
  - 768px+: two-column collection grid
  - 1024px+: sidebar navigation, three-column grid
- No horizontal scrolling at any breakpoint

**Device Input**:
- Touch and pointer both supported
- Minimum tap target: 44x44px (WCAG 2.5.5)
- No hover-only interactions — all hover states have tap equivalents
- Swipe gestures: none for prototype (avoid gesture discovery problems)

**Progressive Enhancement**:
- JavaScript required — the app is a SPA, no server-rendered fallback
- `<noscript>` message: "This app requires JavaScript to run"
- CSS custom properties: supported in all target browsers, no fallback needed

**Offline and Network**:
- Constant connectivity required for prototype
- Deferred: service worker for offline tea collection viewing (post-validation)
- No localStorage caching of collection data in prototype

**Device Features**:
- Camera: not needed (no image upload in prototype scope)
- Geolocation: not needed
- Notifications: not needed (freshness reminders deferred)
- No hardware API dependencies for prototype
</example>
