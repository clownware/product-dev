---
metadata:
  id: "uxr.03_solution_hypothesis.generate_features"
  slug: "generate-features"
  title: "Generate Features"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Identify essential features needed to test the hypothesis"
  context: "Use after formulating hypothesis to define minimum feature set for testing"
  tier: 2
dependencies:
  requires: ["hypothesis_statement"]
  produces: ["feature_list"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "feature_list"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "generate_features"
---

For our solution concept and hypothesis: "[insert hypothesis]", please identify the 2-3 essential features needed to test this hypothesis.

For each feature:
1. Provide a brief description of functionality
2. Explain how it directly contributes to testing our hypothesis
3. Note why it's considered essential (vs. nice-to-have)
4. Describe the key user interaction(s) involved
5. Indicate any particular challenges in implementing it

Focus only on the minimum features needed to test our core hypothesis. We can expand later if the initial concept proves successful.