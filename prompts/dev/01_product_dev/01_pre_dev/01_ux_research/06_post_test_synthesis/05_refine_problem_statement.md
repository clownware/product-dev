---
name: post-test-refine-problem
description: >
  Refine problem statement based on test learnings.
  Use when test results suggest the problem needs reframing.
run: always
produces: updated_problem_statement
requires: [hypothesis_evaluation, problem_statement]
tier: 3
---
Based on our test results and hypothesis evaluation, let's revisit our problem statement: {{problem_statement}}

Consider:
1. Did testing reveal aspects of the problem we didn't anticipate?
2. Should we narrow or broaden the problem scope?
3. Did users describe the problem differently than we framed it?
4. Are there adjacent problems that emerged as more important?

Provide an updated problem statement with clear rationale for changes.
