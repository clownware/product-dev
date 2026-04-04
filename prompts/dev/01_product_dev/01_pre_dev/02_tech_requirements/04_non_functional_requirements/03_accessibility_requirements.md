---
metadata:
  id: "tech.04_nfr.accessibility_requirements"
  slug: "accessibility-requirements"
  title: "Accessibility Requirements"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Non-Functional Requirements"
  type: "instruction"
  folder: "04_non_functional_requirements"
  tags: ["nfr"]
  purpose: "Define accessibility standards and requirements"
  context: "Use to ensure the product meets WCAG and inclusive design standards"
  tier: 2
dependencies:
  requires: ["user_flow","screen_inventory"]
  produces: ["accessibility_requirements"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "accessibility_requirements"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "accessibility_requirements"
---
Help me define accessibility requirements for our application:

1. Specify compliance standards (WCAG level)
2. Identify key accessibility features required
3. Define keyboard navigation requirements
4. Specify screen reader compatibility needs
5. Establish color contrast and typography guidelines
6. Define testing procedures for accessibility

These requirements should ensure our application is usable by people with various disabilities.
