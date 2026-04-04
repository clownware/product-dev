---
metadata:
  id: "setup.01_assess.project_tools"
  slug: "assess-project-tools"
  title: "Assess Project Tools"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Tool Selection & Setup"
  type: "instruction"
  folder: "01_assess_project_environment"
  tags: ["setup"]
  purpose: "Evaluate current and needed development tools"
  context: "Use when setting up a new project environment"
  tier: 2
dependencies:
  requires: ["solution_concept"]
  produces: ["tool_assessment"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "tool_assessment"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "assess_project_tools"
---
Based on our project requirements and specifications from the UX phase, help me assess the optimal toolset for this project.

For each category, suggest the most appropriate tool and configuration:

1. IDE & Development Environment:
   - Assess if Windsurf IDE is appropriate for this project's needs
   - Recommend specific extensions or configurations for our use case
   - Suggest development container specifications if applicable

2. AI Assistance Integration:
   - Evaluate how to best configure Cline extension for this project
   - Define patterns for AI-assisted development that match our workflow
   - Suggest prompt templates specific to our project domain

3. Component Generation Strategy:
   - Assess if V0 is the right fit for our UI component needs
   - Recommend configuration options based on our design system requirements
   - Suggest integration patterns with our broader development workflow

4. API Development Tools:
   - Evaluate if Apidog meets our specific API documentation needs
   - Recommend configuration settings based on our API design patterns
   - Suggest integration points with our development and testing workflows

5. Version Control & CI/CD:
   - Recommend branch strategy and commit conventions
   - Suggest automated testing and deployment pipeline configurations
   - Define code review processes and standards

6. Environment Configuration:
   - Suggest local development environment setup
   - Recommend staging and production environment configurations
   - Define environment variable management approach

Provide reasoning for each recommendation based on our specific project requirements, team skills, and development philosophy.
