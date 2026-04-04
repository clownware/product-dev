---
metadata:
  id: "uxr.01_define_problem.create_proto_persona"
  slug: "create-proto-persona"
  title: "Create Proto-Persona"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Problem Definition"
  type: "instruction"
  folder: "01_define_problem"
  tags: ["problem"]
  purpose: "Develop a lightweight persona to represent the target user"
  context: "Use after problem statement to create a concrete user representation"
  tier: 1
dependencies:
  requires: ["problem_statement"]
  produces: ["proto_persona"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "proto_persona"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "create_proto_persona"
---
Based on our problem statement: "[insert problem statement]", please create a lightweight proto-persona that represents our target user.

Focus only on characteristics directly relevant to the identified problem:
1. Key demographics (only those relevant to the problem, not comprehensive)
2. Goals and motivations related to the problem space
3. Pain points and specific frustrations
4. Behaviors and habits that contextualize the need
5. Relevant skills, knowledge, or experience levels
6. A brief quote that captures their perspective on this problem
7. Context of use (when/where they would use similar products)

Remember that effective personas focus on behaviors over demographics unless demographic information is directly relevant to product use. Keep it concise but include specific details that make the persona memorable and distinct.

This is an initial hypothesis of our user, not a comprehensive persona. We'll refine this as we learn more through testing and validation.
