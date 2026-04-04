---
metadata:
  id: "uxr.05_prototype.prototype_tool_selection"
  slug: "prototype-tool-selection"
  title: "Prototype Tool Selection"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Select appropriate prototyping tools"
  context: "Use when deciding how to build the prototype"
  tier: 3
dependencies:
  requires: ["prototype_scope","fidelity_decision"]
  produces: ["prototype_tool_choice"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "prototype_tool_choice"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "prototype_tool_selection"
---
Based on our prototype scope and fidelity decisions, help me select the right prototyping tool.

Consider:
1. Required fidelity level (low/mid/high for visual, interaction, content)
2. Key interactions that need to be functional
3. Team skills and tool familiarity
4. Time available for prototype development
5. Testing requirements (remote vs. in-person, recording needs)

Recommend 1-2 tools with rationale and note any trade-offs.
