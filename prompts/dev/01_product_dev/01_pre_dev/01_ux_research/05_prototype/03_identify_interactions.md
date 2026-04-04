---
metadata:
  id: "uxr.05_prototype.identify_key_interactions"
  slug: "identify-key-interactions"
  title: "Identify Key Interactions"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Prototype Planning & Testing"
  type: "instruction"
  folder: "05_prototype"
  tags: ["mvp_feature"]
  purpose: "Define which interactions need to be functional in prototype"
  context: "Use to prioritize interaction development"
  tier: 2
dependencies:
  requires: ["prototype_scope"]
  produces: ["key_interactions"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "key_interactions"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "identify_key_interactions"
---
For our prototype, please identify the specific interactions that need to be functional.

For each key interaction:
1. Describe the user action (e.g., "tap button", "swipe list")
2. Note the expected system response
3. Explain why this interaction is critical to test
4. Suggest how complex it might be to implement
5. Note any specific details needed for the interaction to feel realistic

Focus on interactions that are essential to testing our hypothesis rather than trying to make everything functional.
