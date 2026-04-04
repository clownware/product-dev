---
metadata:
  id: "uxr.01_define_problem.problem_priority"
  slug: "problem-priority"
  title: "Problem Priority Assessment"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Problem Definition"
  type: "instruction"
  folder: "01_define_problem"
  tags: ["problem"]
  purpose: "Assess problem priority and urgency for resource allocation"
  context: "Use after qualifying the problem to determine investment level"
  tier: 3
dependencies:
  requires: ["problem_qualification"]
  produces: ["priority_assessment"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "priority_assessment"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "problem_priority"
---
Based on our problem qualification results, help me create a priority assessment.

Please evaluate:
1. Where does this problem fall on a severity x frequency matrix?
2. What is the estimated market size or user reach?
3. How does this compare to alternative problems we could solve?
4. What is the urgency - is this problem getting worse over time?
5. What is the strategic fit with our capabilities and goals?

Recommend a priority level (Critical / High / Medium / Low) with clear rationale.
