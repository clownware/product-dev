---
metadata:
  id: "uxr.03_solution_hypothesis.risk_assessment"
  slug: "risk-assessment"
  title: "Risk Assessment"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Identify and assess key risks to the solution hypothesis"
  context: "Use after defining solution concept to evaluate risks and mitigation strategies"
  tier: 2
dependencies:
  requires: ["solution_concept"]
  produces: ["risk_assessment"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "risk_assessment"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "risk_assessment"
---

For our solution hypothesis: "[insert hypothesis]", please help me identify and assess the key risks.

Please identify:
1. What are the top 3 risks that might cause our solution to fail?
2. For each risk, how likely is it to occur? (High/Medium/Low)
3. For each risk, how severe would the impact be? (High/Medium/Low)
4. What early indicators might suggest these risks are manifesting?
5. What mitigation strategies could we employ for each risk?

This assessment will help us focus our testing on the most critical assumptions and prepare contingency plans.