---
name: platform-strategy
description: >
  Develop platform strategy and release approach.
  Use early in planning to guide technical decisions.
run: always
produces: platform_strategy
requires: [problem_statement]
tier: 3
---

For our solution addressing: {{problem_statement}}, let's develop a clear platform strategy.

Please help me determine:

1. Which platforms should we prioritize initially? (Web, iOS, Android, desktop, etc.)
2. For each relevant platform:
   - What unique constraints or considerations apply?
   - What specific user expectations exist on this platform?
   - What technical capabilities or limitations should we account for?
3. Which functionality should be:
   - Core (identical across all platforms)
   - Adapted (same intent but platform-specific implementation)
   - Platform-specific (unique to certain platforms)
4. What is our approach to:
   - Authentication across platforms
   - Data synchronization
   - Offline capabilities
   - Platform-specific features vs. consistency
5. How should we sequence our platform releases?

This platform strategy will guide technical decisions and ensure we deliver a consistent yet platform-appropriate experience.