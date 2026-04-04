---
metadata:
  id: "uxr.05_prototype.define_prototype_scope"
  slug: "define-prototype-scope"
  title: "Define Prototype Scope"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Determine what to include and exclude from the prototype"
  context: "Use when beginning prototype planning to establish boundaries"
  tier: 1
dependencies:
  requires: ["user_flow"]
  produces: ["prototype_scope"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "prototype_scope"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_prototype_scope"
---
Based on our user flow and key screens, let's define the scope for our initial prototype.

Please help me determine:
1. Which specific screens from our flow should be included in the prototype?
2. Which user interactions need to be functional?
3. Which aspects can be simulated or "smoke and mirrors"?
4. What content needs to be realistic vs. placeholder?
5. Where should we set the boundaries of the prototype experience?
6. What minimum level of fidelity is required to test our hypothesis?
7. Which parts of the flow are most critical for testing our assumptions?

Consider both what to include and what to intentionally exclude at this stage. The prototype should be a focused tool for testing specific hypotheses, not a comprehensive implementation.

The goal is to define a prototype scope that is focused enough to build quickly but sufficient to test our core hypothesis. We want to learn the most important things with the minimum necessary investment of time and resources.
