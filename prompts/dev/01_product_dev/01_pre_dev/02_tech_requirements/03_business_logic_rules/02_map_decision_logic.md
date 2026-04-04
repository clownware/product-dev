---
metadata:
  id: "tech.03_business_logic.map_decision_logic"
  slug: "map-decision-logic"
  title: "Map Decision Logic"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Business Logic & Rules"
  type: "instruction"
  folder: "03_business_logic_rules"
  tags: ["mvp_feature"]
  purpose: "Create detailed decision flow documentation"
  context: "Use for complex decision-making processes"
  tier: 2
dependencies:
  requires: ["business_rules"]
  produces: ["decision_logic"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "decision_logic"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "map_decision_logic"
---
For our key user flows that involve complex decisions, help me map the decision logic:

1. Identify decision points in our user flows
2. Define the inputs needed for each decision
3. Create decision trees or flowcharts for complex decision logic
4. Document the expected outcomes for different input combinations
5. Note edge cases and how they should be handled
6. Explain how this decision logic aligns with user expectations

This mapping will help ensure consistent implementation of business rules across the application.
