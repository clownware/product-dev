---
metadata:
  id: "uxr.05_prototype.define_test_questions"
  slug: "define-test-questions"
  title: "Define Test Questions"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Formulate specific questions the prototype test should answer"
  context: "Use to ensure test focuses on hypothesis validation"
  tier: 1
dependencies:
  requires: ["hypothesis_statement"]
  produces: ["test_questions"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "test_questions"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_test_questions"
---
Based on our hypothesis statement: "[insert hypothesis]", please help me formulate specific questions our prototype test should answer.

Requirements:
1. Each question should connect directly to an aspect of our hypothesis
2. Questions should be specific and answerable through observation or user feedback
3. Include 2-3 primary questions focused on validating/invalidating our core hypothesis
4. Include 1-2 secondary questions about usability or implementation details
5. Frame questions neutrally to avoid biasing our testing

These questions will guide our test plan and help us evaluate whether our prototype successfully addresses our core hypothesis.
