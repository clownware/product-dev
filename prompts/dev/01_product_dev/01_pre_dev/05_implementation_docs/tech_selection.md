---
metadata:
  id: "impl.tech_selection"
  slug: "tech-selection-rationale"
  title: "Technology Selection Rationale"
  version: "0.1.0"
  status: "active"
  phase: "dev"
  category: "Implementation"
  type: "instruction"
  folder: "05_implementation_docs"
  tags: ["implementation"]
  purpose: "Document technology selection decisions with rationale"
  context: "Use when finalizing technology choices for implementation"
  tier: 2
dependencies:
  requires: ["tech_stack_evaluation","solution_concept"]
  produces: ["tech_selection_rationale"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "tech_selection_rationale"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "tech_selection_rationale"
---
Based on our solution requirements and user needs, let's evaluate and select the optimal technology stack.

Please help me:

1. Evaluate frontend technology options:
   - Framework requirements based on UI/UX needs
   - State management considerations
   - Performance requirements
   - Developer experience and team capabilities
   - Future maintainability and scalability

2. Evaluate backend technology options:
   - API requirements and patterns
   - Data storage needs
   - Performance and scaling considerations
   - Integration requirements
   - Operational characteristics

3. Consider infrastructure and deployment:
   - Hosting requirements
   - CI/CD approach
   - Monitoring and observability
   - Security requirements
   - Cost considerations

4. For each major technology decision:
   - Present 2-3 viable options
   - Compare pros/cons for our specific needs
   - Make a clear recommendation with rationale

5. Present the recommended full-stack architecture with:
   - Key technology choices
   - How they fit together
   - Specific versions/tools
   - Implementation considerations

The selected technology stack should optimally support our solution requirements while considering both immediate development needs and long-term maintenance.
