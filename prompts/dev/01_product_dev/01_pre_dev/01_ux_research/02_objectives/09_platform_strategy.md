---
metadata:
  id: "uxr.02_objectives.platform_strategy"
  slug: "platform-strategy"
  title: "Platform Strategy"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Objectives & Success Metrics"
  type: "instruction"
  folder: "02_objectives"
  tags: ["value_prop"]
  purpose: "Develop platform strategy and release approach"
  context: "Use early in planning to guide technical decisions"
  tier: 3
dependencies:
  requires: ["problem_statement"]
  produces: ["platform_strategy"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "platform_strategy"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "platform_strategy"
---

For our solution addressing: "[insert problem statement]", let's develop a clear platform strategy.

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