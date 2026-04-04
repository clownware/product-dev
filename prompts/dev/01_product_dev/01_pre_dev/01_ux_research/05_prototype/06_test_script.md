---
metadata:
  id: "uxr.05_prototype.test_script_outline"
  slug: "test-script-outline"
  title: "Test Script Outline"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Create an outline for the test script"
  context: "Use as a quick alternative to the full test script"
  tier: 3
dependencies:
  requires: ["test_questions"]
  produces: ["test_script_outline"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "test_script_outline"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "test_script_outline"
---
Create a brief test script outline covering:
1. Introduction (2 min) - welcome, context setting
2. Background questions (3 min) - relevant user context
3. Tasks (15 min) - 3-4 specific tasks to attempt
4. Debrief (5 min) - overall impressions, hypothesis-specific questions

Keep it concise - this is a planning outline, not the final script.
