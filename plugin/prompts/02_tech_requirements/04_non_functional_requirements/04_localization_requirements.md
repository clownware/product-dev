---
name: localization-requirements
description: >
  Define internationalization and localization architecture.
  Use when the product will serve multiple locales or needs i18n-ready structure.
run: always
produces: localization_requirements
requires: [solution_concept]
tier: 3
---

<system_context>
You are a localization engineer defining the i18n architecture for a
prototype. Be practical — most prototypes ship in one language, but the
architecture should not make localization painful later. Focus on structural
decisions (string externalization, formatting APIs) not translation workflow.
</system_context>

Given:
- Solution concept: {{solution_concept}}
- Screen inventory (if available — may not exist for non-UI products): reference if the product-flow skill produced a screen_inventory artifact

Produce a `localization_requirements` artifact. Present your reasoning
conversationally first (which languages matter for prototype vs. future,
what structural decisions prevent localization debt), then output the
structured requirements.

**Prototype Scope**: Which language(s) the prototype ships in. Be explicit
that this is a scoping decision, not a permanent constraint.

**String Architecture**: How UI text is managed — hardcoded (acceptable for
prototype?), externalized to resource files, or key-based with a library.
Recommend the minimum viable approach that doesn't create migration pain.

**Formatting**: Date, time, number, and currency formatting approach. Name
the API or library (Intl, date-fns, etc.) and the default locale.

**Layout Direction**: Whether the CSS/layout supports RTL. For prototype,
state whether RTL is deferred but specify what structural choices prevent
blocking it later (logical properties vs. physical, flexbox vs. float).

**Content Strategy**: Identify content types that need localization beyond
UI strings — error messages, email templates, user-generated content display
rules (text direction detection).

**Text Expansion**: Identify UI elements with tight space constraints where
translated text (typically 30-50% longer than English) would break layout.
Reference specific screens if screen inventory exists.

<constraints>
- Do NOT specify a full translation pipeline for a prototype — focus on architecture, not workflow
- Do NOT recommend hardcoding strings if the product concept implies multi-locale ambitions
- Do NOT ignore date/number formatting even for single-language prototypes — locale-aware formatting is cheap to add and expensive to retrofit
- Do NOT treat RTL as an afterthought — state the structural CSS approach even if RTL is deferred
- Do NOT recommend a localization library without stating its bundle size impact
</constraints>

<example>
Here's how the tea tracker's localization requirements look:

The tea tracker is a personal tool — prototype ships English-only. But tea
is global, and the concept could attract users in CJK markets where tea
culture is strong. So the architecture should externalize strings and use
locale-aware formatting from day one, even though translation is deferred.

**Prototype Scope**: English (en-US) only. No translation files, no
language switcher, no locale detection.

**String Architecture**: Externalize all UI strings to a single JSON
resource file (e.g., `messages/en.json`). Key format: `screen.component.label`
(e.g., `collection.empty.title`). This adds ~30 minutes to initial setup
and prevents a painful migration when localization becomes real.

**Formatting**:
- Dates: Use `Intl.DateTimeFormat` with explicit locale parameter. Tea
  purchase dates, freshness calculations display in user's locale format.
- Numbers: Use `Intl.NumberFormat` for any numeric display (rating counts,
  collection size).
- No currency in tea tracker — not applicable.

**Layout Direction**: Defer RTL support. Structural preparation:
- Use CSS logical properties (`margin-inline-start` not `margin-left`)
- Use flexbox for layout (inherently direction-aware)
- Avoid absolute positioning of text elements

**Content Strategy**:
- UI strings: externalized (see above)
- Error messages: externalize alongside UI strings, same key structure
- User-generated content (tea names, notes): display as-is, no translation.
  Add `dir="auto"` attribute to user text containers for automatic
  direction detection.

**Text Expansion**: Tight areas to watch:
- Freshness status badges ("Fresh", "Drink Soon", "Past Peak") — German
  equivalents are 40-60% longer. Use flexible badge width, not fixed.
- Navigation labels — keep under 2 words or use icons with text.
</example>
