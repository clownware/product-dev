---
name: scope-problem
description: >
  Define boundaries and constraints for the problem to address.
  Use to establish clear scope before moving to solution design.
run: always
produces: problem_scope
requires: [problem_statement]
tier: 2
---
Let's establish clear boundaries for our problem scope based on our statement: {{problem_statement}}

Help me define:
1. What specific aspects of this problem we WILL address
2. What related aspects we will explicitly NOT address (at least initially)
3. How we might narrow the focus to ensure we can adequately address it in a prototype
4. What constraints might affect our ability to solve this problem completely

The goal is to define a problem scope that is narrow enough to be addressable in our prototype but significant enough to provide real user value.
