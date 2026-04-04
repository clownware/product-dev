---
metadata:
  id: "tech.03_business_logic.define_business_rules"
  slug: "define-business-rules"
  title: "Define Business Rules"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Business Logic & Rules"
  type: "instruction"
  folder: "03_business_logic_rules"
  tags: ["mvp_feature"]
  purpose: "Document key business logic rules for implementation"
  context: "Use after solution design to specify business logic"
  tier: 1
dependencies:
  requires: ["solution_concept","user_flow"]
  produces: ["business_rules"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "business_rules"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_business_rules"
---
Based on our Solution Hypothesis and Data Models, help me document the key business logic rules that should be implemented.

For each business rule:
1. Provide a clear name and description
2. Explain when this rule should be applied
3. Detail the exact logic/algorithm to be implemented
4. Identify dependencies on other rules or data
5. Note any exceptions or special cases
6. Specify how rule violations should be handled
7. Explain how this rule supports our core business objectives

The goal is to create a medium-specificity guide that clarifies business logic without over-constraining implementation details.
