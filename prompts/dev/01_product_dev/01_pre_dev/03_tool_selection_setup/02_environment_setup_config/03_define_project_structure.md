---
metadata:
  id: "setup.02_env.project_structure"
  slug: "define-project-structure"
  title: "Define Project Structure"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Environment Setup"
  type: "instruction"
  folder: "02_environment_setup_config"
  tags: ["setup"]
  purpose: "Define directory structure and file organization"
  context: "Use when scaffolding a new project"
  tier: 2
dependencies:
  requires: ["tech_stack_evaluation"]
  produces: ["project_structure"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "project_structure"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_project_structure"
---
Help me define an optimal project structure based on our selected tools and architectural approach.

Create a detailed directory structure and file organization that:

1. Aligns with our chosen meta-framework (Next.js with App Router)
2. Facilitates effective use of our AI tooling (Windsurf, Cline, V0)
3. Supports clean separation of concerns in our architecture
4. Enables efficient team collaboration
5. Follows established patterns for our technology stack
6. Accommodates our testing and documentation requirements

For each major directory or organizational unit:
- Explain its purpose and responsibility
- Define naming conventions
- Describe file organization patterns
- Suggest template files where appropriate
- Note how it integrates with our toolchain

Include recommendations for:
- Feature organization
- API route structuring
- Component hierarchy
- State management approach
- Utility and helper organization
- Test organization
- Documentation placement

This structure should be optimized for our specific project needs while maintaining adherence to established best practices for our technology stack.
