---
metadata:
  id: "uxr.01_define_problem.user_validation_questions"
  slug: "user-validation-questions"
  title: "User Validation Questions"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Problem Definition"
  type: "instruction"
  folder: "01_define_problem"
  tags: ["problem"]
  purpose: "Generate questions to validate problem with real users"
  context: "Use when preparing for user interviews or validation sessions"
  tier: 3
dependencies:
  requires: ["problem_statement","proto_persona"]
  produces: ["validation_questions"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "validation_questions"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "user_validation_questions"
---
Based on our problem statement and proto-persona, help me create a set of questions to validate our assumptions with real users.

Please generate:
1. 5-7 open-ended questions that test our core problem assumptions
2. 2-3 questions that explore the user's current workarounds
3. 2-3 questions that gauge severity and frequency of the problem
4. 1-2 questions about willingness to adopt a new solution

Ensure questions are neutral and don't lead the user toward confirming our assumptions.
