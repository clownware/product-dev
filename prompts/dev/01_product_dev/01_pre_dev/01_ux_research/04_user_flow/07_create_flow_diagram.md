---
metadata:
  id: "uxr.04_user_flow.create_flow_diagram"
  slug: "create-flow-diagram"
  title: "Create Flow Diagram"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "User Flow & Interaction"
  type: "instruction"
  folder: "04_user_flow"
  tags: ["user_flow"]
  purpose: "Generate a structured flow diagram from the user flow"
  context: "Use to create a visual representation of the flow"
  tier: 3
dependencies:
  requires: ["user_flow","decision_points"]
  produces: ["flow_diagram"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "flow_diagram"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "create_flow_diagram"
---
Based on our complete user flow including decision points and error paths, please create a structured flow diagram.

Use this notation:
- [Rectangle] for screens/states
- <Diamond> for decision points
- (Rounded) for start/end
- --> for flow direction
- [!] for error states

Include the happy path, key decision branches, and error recovery paths. Format as a text-based diagram that can be translated to a visual tool.
