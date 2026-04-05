---
name: analyze-problem
description: >
  Deep dive into the underlying factors of the identified problem.
  Use to understand root causes and context of the problem.
run: always
produces: problem_analysis
requires: [problem_statement]
tier: 2
---
For our problem statement: {{problem_statement}}, please help me understand the underlying factors.

Analyze this problem by identifying:
1. What are 3-5 root causes of this problem?
2. When and where does this problem typically occur for users?
3. What makes this problem particularly challenging to solve?
4. What workarounds might users currently employ?
5. What secondary problems might emerge from these workarounds?

This analysis will help us ensure we're addressing the fundamental need rather than just surface symptoms.
