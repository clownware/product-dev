---
metadata:
  id: "uxr.04_user_flow.plan_error_handling"
  slug: "plan-error-handling"
  title: "Plan Error Handling"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Define how to handle critical errors in flow"
  context: "Use to ensure smooth error recovery"
  tier: 2
dependencies:
  requires: ["user_flow"]
  produces: ["error_handling_plan"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "error_handling_plan"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "plan_error_handling"
---
For our user flow, let's identify potential critical errors and how to handle them.

Please consider:
1. What are 2-3 critical errors that might occur during the primary user flow?
2. For each error, at what point in the flow might it occur?
3. How should we communicate this error to the user?
4. What recovery path should we provide?
5. How can we help prevent this error in the first place?

Focus only on critical errors that would prevent the user from completing their task, not minor edge cases.
