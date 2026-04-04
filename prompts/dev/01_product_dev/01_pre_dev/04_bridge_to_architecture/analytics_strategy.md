---
metadata:
  id: "bridge.analytics_strategy"
  slug: "analytics-strategy"
  title: "Analytics Strategy"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Bridge to Architecture"
  type: "instruction"
  folder: "04_bridge_to_architecture"
  tags: ["architecture"]
  purpose: "Define analytics implementation strategy"
  context: "Use when planning how to measure product usage and success"
  tier: 2
dependencies:
  requires: ["success_metrics","user_flow"]
  produces: ["analytics_strategy"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "analytics_strategy"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "analytics_strategy"
---
For our solution: "[insert solution concept]" with core metrics: "[insert metrics]", let's develop a comprehensive analytics strategy.

Please help me define:

1. Key events to track:
   - User actions and interactions
   - System events and state changes
   - Error conditions
   - Performance metrics
   - Business metrics

2. For each critical event:
   - Specific definition and trigger conditions
   - Properties/parameters to capture
   - Connection to product goals and hypotheses
   - Implementation considerations

3. User property/dimension strategy:
   - What user characteristics should we capture?
   - What segmentation dimensions are important?
   - What session/context data is relevant?

4. Implementation approach:
   - Recommended analytics tool/platform
   - Integration strategy (client vs. server-side)
   - Data layer requirements
   - Privacy and consent considerations

5. Reporting framework:
   - Key dashboards needed
   - Critical metrics for ongoing monitoring
   - Alert thresholds

This analytics strategy will ensure we collect the right data to measure success and inform future iterations.
