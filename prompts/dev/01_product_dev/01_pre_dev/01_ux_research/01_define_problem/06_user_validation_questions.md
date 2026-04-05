---
name: user-validation-questions
description: >
  Generate questions to validate problem with real users.
  Use when preparing for user interviews or validation sessions.
run: always
produces: validation_questions
requires: [problem_statement, proto_persona]
tier: 3
---
Based on our problem statement and proto-persona, help me create a set of questions to validate our assumptions with real users.

Please generate:
1. 5-7 open-ended questions that test our core problem assumptions
2. 2-3 questions that explore the user's current workarounds
3. 2-3 questions that gauge severity and frequency of the problem
4. 1-2 questions about willingness to adopt a new solution

Ensure questions are neutral and don't lead the user toward confirming our assumptions.
