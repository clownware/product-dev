---
name: create-flow-diagram
description: >
  Generate a structured flow diagram from the user flow.
  Use to create a visual representation of the flow.
run: always
produces: flow_diagram
requires: [user_flow, decision_points]
tier: 3
---
Based on our complete user flow including decision points and error paths, please create a structured flow diagram.

Use this notation:
- [Rectangle] for screens/states
- <Diamond> for decision points
- (Rounded) for start/end
- --> for flow direction
- [!] for error states

Include the happy path, key decision branches, and error recovery paths. Format as a text-based diagram that can be translated to a visual tool.
