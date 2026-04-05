---
name: define-business-rules
description: >
  Document key business logic rules for implementation.
  Use after solution design to specify business logic.
run: always
produces: business_rules
requires: [solution_concept, user_flow]
tier: 1
---
Based on our Solution Hypothesis and Data Models, help me document the key business logic rules that should be implemented.

For each business rule:
1. Provide a clear name and description
2. Explain when this rule should be applied
3. Detail the exact logic/algorithm to be implemented
4. Identify dependencies on other rules or data
5. Note any exceptions or special cases
6. Specify how rule violations should be handled
7. Explain how this rule supports our core business objectives

The goal is to create a medium-specificity guide that clarifies business logic without over-constraining implementation details.
