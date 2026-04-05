---
name: refine-problem
description: >
  Refine the problem statement based on deeper analysis.
  Use after problem analysis to sharpen the statement.
run: always
produces: refined_problem_statement
requires: [problem_statement, problem_analysis]
tier: 3
---
Based on our problem analysis, let's refine our original problem statement: {{problem_statement}}

Consider:
1. Does the analysis suggest we should narrow or broaden our focus?
2. Are there root causes we should address instead of symptoms?
3. Should the user type be more specific based on what we've learned?
4. Does the insight still capture the core motivation?

Provide a refined problem statement and explain what changed and why.
