---
name: prototype-tool-selection
description: >
  Select appropriate prototyping tools.
  Use when deciding how to build the prototype.
run: always
produces: prototype_tool_choice
requires: [prototype_scope, fidelity_decision]
tier: 3
---
Based on our prototype scope and fidelity decisions, help me select the right prototyping tool.

Consider:
1. Required fidelity level (low/mid/high for visual, interaction, content)
2. Key interactions that need to be functional
3. Team skills and tool familiarity
4. Time available for prototype development
5. Testing requirements (remote vs. in-person, recording needs)

Recommend 1-2 tools with rationale and note any trade-offs.
