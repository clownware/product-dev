---
metadata:
  id: "uxr.04_user_flow.map_primary_user_flow"
  slug: "map-primary-user-flow"
  title: "Map Primary User Flow"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Define the core happy path from entry to goal completion"
  context: "Use after solution concept to map ideal user journey"
  tier: 1
dependencies:
  requires: ["solution_concept"]
  produces: ["user_flow"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "user_flow"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "map_primary_user_flow"
---
Based on our solution concept and key features, please map the primary user flow from start to goal completion.

Requirements:

1. Start with the user's entry point into the experience
2. Include each significant step the user takes
3. Note the user's goal or intention at each step
4. End with successful completion of the core task
5. Focus only on the "happy path" where everything goes as expected
6. Format as a numbered sequence for clarity
7. Identify the actions, screens, and decisions (using standard flow notation)
8. Keep the flow focused on the specific user goal identified in our problem statement

The flow should map the quickest and easiest path to goal completion, making sure each step logically leads to the next. This establishes the backbone for our prototype design.

Remember that user flows should map the user's perspective and mental model, not your technical or organizational structure. Focus on what the user is trying to accomplish at each stage.
