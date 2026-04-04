---
metadata:
  id: "uxr.06_post_test_synthesis.evaluate_hypothesis"
  slug: "evaluate-hypothesis"
  title: "Evaluate Hypothesis"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Post-Test Analysis"
  type: "instruction"
  folder: "06_post_test_synthesis"
  tags: ["mvp_feature"]
  purpose: "Assess whether testing validated or invalidated hypothesis"
  context: "Use after synthesizing test results"
  tier: 1
dependencies:
  requires: ["hypothesis_statement"]
  produces: ["hypothesis_evaluation"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "hypothesis_evaluation"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "evaluate_hypothesis"
---
Based on our test results, let's evaluate our hypothesis: "[insert hypothesis]"

Please assess:
1. Was our hypothesis validated, invalidated, or are the results inconclusive?
2. What specific evidence supports this assessment?
3. Were there any unexpected findings that challenge our assumptions?
4. How did we perform against our success metrics?
5. What level of confidence should we have in these conclusions?
6. What variables or conditions might have influenced our results?
7. What limitations should we acknowledge in our testing approach?
8. How do these results connect back to our original problem statement?

Be careful not to overinterpret limited data. Recognize the difference between statistical significance and practical significance in your assessment.

This evaluation will help us determine our next steps - whether to proceed with the current direction, pivot, or gather more data. It's important to be honest about what we've learned and what remains uncertain.
