---
metadata:
  id: "uxr.05_prototype.choose_fidelity_level"
  slug: "choose-fidelity-level"
  title: "Choose Fidelity Level"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Determine appropriate fidelity for different prototype aspects"
  context: "Use to balance effort vs. test validity"
  tier: 2
dependencies:
  requires: ["prototype_scope"]
  produces: ["fidelity_decision"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "fidelity_decision"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "choose_fidelity_level"
---
Help me determine the appropriate fidelity level for our prototype based on our testing goals.

Please consider:
1. What level of visual fidelity is necessary to test our hypothesis?
2. What level of interaction fidelity is necessary?
3. What level of content fidelity is necessary?
4. How might different fidelity choices affect our test results?
5. What's the minimum fidelity needed to get valid feedback?
6. Which aspects would benefit from higher fidelity and which can remain lower?
7. How does our fidelity choice align with our specific testing questions?

For each decision, consider the trade-off between investment (time/resources) and learning value. Higher fidelity isn't always better - it depends entirely on what you're trying to learn.

Recommend a specific fidelity approach (low/mid/high) for each aspect (visual, interaction, content) with justification based on our specific testing needs. Consider a hybrid approach where critical components have higher fidelity while less important elements remain simpler.
