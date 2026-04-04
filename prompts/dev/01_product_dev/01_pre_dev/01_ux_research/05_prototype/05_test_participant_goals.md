---
metadata:
  id: "uxr.05_prototype.test_participant_goals"
  slug: "test-participant-goals"
  title: "Test Participant Goals"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Define what each test participant should try to accomplish"
  context: "Use when designing specific tasks for test participants"
  tier: 3
dependencies:
  requires: ["test_questions"]
  produces: ["participant_goals"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "participant_goals"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "test_participant_goals"
---
For our prototype test, let's define specific goals for test participants.

For each test task:
1. What should the participant try to accomplish?
2. What context should we provide without biasing them?
3. What does successful completion look like?
4. What should we observe during this task?
5. What follow-up questions should we ask?

Design 3-4 tasks that map directly to our test questions and hypothesis.
