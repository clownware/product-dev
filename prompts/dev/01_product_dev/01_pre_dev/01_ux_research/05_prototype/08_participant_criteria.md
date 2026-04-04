---
metadata:
  id: "uxr.05_prototype.define_participant_criteria"
  slug: "define-participant-criteria"
  title: "Define Participant Criteria"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Establish criteria for selecting test participants"
  context: "Use for participant recruitment and screening"
  tier: 3
dependencies:
  requires: ["test_questions"]
  produces: ["participant_criteria"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "participant_criteria"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_participant_criteria"
---
For testing our prototype of: "[insert solution concept]", let's define ideal test participant criteria.

Please help me establish:

1. Essential criteria participants must meet:
   - Key demographic parameters (only if directly relevant)
   - Experience level with the problem space
   - Specific behaviors or needs they must have
   - Technical proficiency requirements
   - Any other must-have characteristics

2. Diversity factors to consider:
   - How might we ensure appropriate representation?
   - What range of experience levels should we include?
   - What variety of contexts or use cases should we cover?

3. Exclusion criteria:
   - Who should we specifically NOT include in testing?
   - What biases might we need to control for?

4. Recruitment approach:
   - Where might we find these participants?
   - What screening questions would identify appropriate candidates?
   - How many participants do we need for valid insights?

5. Test grouping (if applicable):
   - Should we segment participants into different test groups?
   - What comparison points might be valuable?

These criteria will ensure our testing provides relevant insights from participants who represent our target users.
