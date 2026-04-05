---
name: problem-priority
description: >
  Assess problem priority and urgency for resource allocation.
  Use after qualifying the problem to determine investment level.
run: always
produces: priority_assessment
requires: [problem_qualification]
tier: 3
---
Based on our problem qualification results, help me create a priority assessment.

Please evaluate:
1. Where does this problem fall on a severity x frequency matrix?
2. What is the estimated market size or user reach?
3. How does this compare to alternative problems we could solve?
4. What is the urgency - is this problem getting worse over time?
5. What is the strategic fit with our capabilities and goals?

Recommend a priority level (Critical / High / Medium / Low) with clear rationale.
