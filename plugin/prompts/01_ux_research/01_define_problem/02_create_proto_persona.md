---
name: create-proto-persona
description: >
  Build a lightweight persona representing the target user.
  Behavior-focused, not demographic-heavy.
run: always
produces: proto_persona
requires: [problem_statement]
tier: 1
---

<system_context>
You are a UX researcher creating a proto-persona — a hypothesis about who
the user is, grounded in the problem statement. Prioritize behaviors and
motivations over demographics. This persona should make the team feel like
they know someone specific, not a market segment.
</system_context>

Based on this problem statement:
{{problem_statement}}

Create a proto-persona with these sections:

**Name & Sketch**: A first name and one-sentence behavioral description (not a job title).

**Relevant Context**: 3-4 bullet points — only demographics, skills, or circumstances that directly affect how they experience this problem. Skip anything generic.

**Goals**: 2-3 things they're trying to accomplish related to the problem space. Frame as motivations, not features.

**Frustrations**: 2-3 specific pain points. Include what they do today and why it falls short.

**Behaviors**: 2-3 observable habits or patterns that contextualize the problem. Things you could see if you watched them.

**Quote**: One sentence in their voice that captures their relationship to this problem.

<constraints>
- Do NOT pad with irrelevant demographics (age, location, income) unless directly relevant
- Do NOT describe an idealized user — include realistic limitations and workarounds
- Do NOT list desired features as goals — goals are outcomes, not tools
- Do NOT exceed 250 words
</constraints>

<example>
**Name & Sketch**: Maya — a tea enthusiast whose collection has grown past the point of casual tracking.

**Relevant Context**:
- Buys from 4-5 online vendors, typically monthly
- Stores tea in a dedicated cabinet with ~35 varieties
- Self-taught through forums and YouTube, not formal training

**Goals**:
- Know what she has before placing another order
- Use her teas while they're still at peak quality
- Spend her tea budget on variety, not accidental duplicates

**Frustrations**:
- Started a spreadsheet twice, abandoned it both times because updating felt like homework
- Discovered a 6-month-old opened gyokuro that had gone flat — felt like wasted money
- Can't remember which vendor's second flush Darjeeling she preferred last year

**Behaviors**:
- Opens the cabinet and scans visually before deciding what to brew
- Takes photos of new teas when they arrive but doesn't organize them
- Reads r/tea daily but rarely posts

**Quote**: "I love trying new teas, but I hate the feeling that I'm neglecting the ones I already have."
</example>
