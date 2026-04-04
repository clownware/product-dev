---
metadata:
  id: "uxr.06_post_test_synthesis.refine_problem_statement"
  slug: "post-test-refine-problem"
  title: "Refine Problem Statement Post-Test"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Post-Test Analysis"
  type: "instruction"
  folder: "06_post_test_synthesis"
  tags: ["mvp_feature"]
  purpose: "Refine problem statement based on test learnings"
  context: "Use when test results suggest the problem needs reframing"
  tier: 3
dependencies:
  requires: ["hypothesis_evaluation","problem_statement"]
  produces: ["updated_problem_statement"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "updated_problem_statement"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "post_test_refine_problem"
---
Based on our test results and hypothesis evaluation, let's revisit our problem statement: "[insert problem statement]"

Consider:
1. Did testing reveal aspects of the problem we didn't anticipate?
2. Should we narrow or broaden the problem scope?
3. Did users describe the problem differently than we framed it?
4. Are there adjacent problems that emerged as more important?

Provide an updated problem statement with clear rationale for changes.
