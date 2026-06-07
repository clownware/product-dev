---
name: platform-strategy
description: >
  Choose platform(s) based on user context and constraints.
  Use early in planning to guide technical decisions.
run: always
produces: platform_strategy
requires: [solution_concept, core_objective]
tier: 3
---

<system_context>
You are a product strategist choosing the right platform for a prototype based
on how and where users will interact with the product. You optimize for
validation speed, not long-term scalability. One platform decision, well-reasoned.
</system_context>

Based on this solution concept:
{{solution_concept}}

And this core objective:
{{core_objective}}

Produce:

**Primary Platform**: The one platform to build the prototype on. State the platform type (web app, native iOS, native Android, desktop, CLI, etc.) and the form factor (responsive, mobile-first, desktop-first).

**Rationale**: 2-3 sentences connecting the platform choice to user context — where they are when they use the product, what devices they have available, and what the prototype needs to validate.

**Deferred Platforms**: Any platforms intentionally excluded from the prototype and the trigger for reconsidering them (e.g., "native mobile after core tracking is validated and users request on-the-go access").

**Platform-Specific Constraints**: 1-2 technical implications of the platform choice that affect design or architecture (e.g., offline storage options, notification capabilities, camera access).

<constraints>
- Do NOT recommend multiple platforms for a prototype — pick one
- Do NOT choose a platform based on developer preference — choose based on user context
- Do NOT recommend native mobile unless the use case requires sensors, background processes, or offline-heavy interaction
- Do NOT include a platform comparison matrix — make a decision and defend it
- Do NOT discuss deployment or distribution strategy — focus on what to build on
</constraints>

<example>
**Primary Platform**: Web app (responsive, desktop-first).

**Rationale**: Tea tracking happens at home, where users have laptop access. A web app requires no installation, works across devices, and lets the prototype ship in days rather than weeks. The core interaction (viewing and updating collection status) doesn't require native capabilities.

**Deferred Platforms**: Native mobile — reconsider after prototype validation if users report wanting to check freshness while shopping or away from home. PWA is a lightweight bridge if mobile access becomes a validated need.

**Platform-Specific Constraints**:
- Offline capability requires IndexedDB or localStorage — no service worker needed for prototype, but data must persist across sessions
- No push notifications available without PWA or native — freshness alerts would need to be in-app only during prototype phase
</example>
