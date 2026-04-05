---
name: validate-flow
description: >
  Validate the user flow against objectives and constraints.
  Use as a quality check before prototyping.
run: always
produces: flow_validation
requires: [user_flow, screen_inventory]
tier: 3
---
Let's validate our user flow against our objectives and constraints.

Please check:
1. Does every step contribute to the user achieving their goal?
2. Are there any unnecessary steps that could be removed?
3. Does the flow account for our identified constraints?
4. Is the cognitive load reasonable at each step?
5. Are there accessibility concerns with any step?
6. Does this flow align with our core objective?

Identify any issues and suggest improvements.
