---
metadata:
  id: "uxr.01_define_problem.qualify_problem"
  slug: "qualify-problem"
  title: "Qualify Problem"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Problem Definition"
  type: "instruction"
  folder: "01_define_problem"
  tags: ["problem"]
  purpose: "Assess the problem's priority and impact from user perspective"
  context: "Use to validate problem significance before investing in solutions"
dependencies:
  requires: []
  produces: []
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "qualify_problem"
---
For our problem statement: "[insert problem statement]", help me assess its priority from a user perspective.

Please evaluate:
1. Severity: How painful is this problem when users encounter it? (1-5 scale)
2. Frequency: How often do users encounter this problem? (1-5 scale)
3. Reach: What percentage of our target users likely experience this problem?
4. Trend: Is this problem becoming more or less significant over time?
5. Uniqueness: How well is this problem currently addressed by existing solutions?

This assessment will help validate whether this problem is worth solving and how urgently it needs attention.
