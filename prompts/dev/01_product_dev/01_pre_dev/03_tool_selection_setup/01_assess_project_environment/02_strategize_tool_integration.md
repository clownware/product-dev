---
metadata:
  id: "setup.01_assess.tool_integration"
  slug: "strategize-tool-integration"
  title: "Strategize Tool Integration"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Tool Selection & Setup"
  type: "instruction"
  folder: "01_assess_project_environment"
  tags: ["setup"]
  purpose: "Plan how tools will work together"
  context: "Use after assessing tools to plan integration approach"
  tier: 2
dependencies:
  requires: ["tool_assessment"]
  produces: ["integration_strategy"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "integration_strategy"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "strategize_tool_integration"
---
Help me develop a cohesive strategy for integrating our selected tools into a seamless workflow.

Please address:

1. Tool Interoperability:
   - How Windsurf IDE, Cline, V0, and Apidog should share data and context
   - Integration points between design tools and development tools
   - How to maintain consistency across tool boundaries

2. Workflow Sequences:
   - Define optimal tool sequences for different development tasks
   - Identify handoff points between tools and team members
   - Suggest automation opportunities between tools

3. Context Preservation:
   - How to maintain context and knowledge across different tools
   - Strategies for documentation that spans tool boundaries
   - Methods for tracing requirements through different tools

4. AI Tool Optimization:
   - How to configure AI tools for our specific domain
   - Strategies for building effective context for AI tools
   - Methods for evaluating and improving AI tool outputs

5. Quality Assurance Across Tools:
   - How to implement consistent validation across tool boundaries
   - Testing strategies that span multiple tools
   - Quality metrics that can be applied consistently

The goal is to create a cohesive ecosystem where our tools complement each other rather than creating silos or friction points.
