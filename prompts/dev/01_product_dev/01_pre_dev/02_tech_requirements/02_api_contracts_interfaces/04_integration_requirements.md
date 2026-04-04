---
metadata:
  id: "tech.02_api_contracts.define_integration_requirements"
  slug: "define-integration-requirements"
  title: "Define Integration Requirements"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "API Contracts & Interfaces"
  type: "instruction"
  folder: "02_api_contracts_interfaces"
  tags: ["mvp_feature"]
  purpose: "Specify requirements for external system integrations"
  context: "Use when planning third-party integrations"
  tier: 2
dependencies:
  requires: []
  produces: []
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "define_integration_requirements"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_integration_requirements"
---
For any external systems or third-party services our application needs to integrate with, help me define the integration requirements:

1. Identify each external system we need to connect with
2. Define the purpose and scope of each integration
3. Specify the APIs or interfaces we'll use
4. Document authentication and security requirements
5. Define data transformation needs
6. Establish error handling and retry strategies
7. Identify rate limits or quotas to be aware of
8. Note any compliance or regulatory considerations

This specification will ensure we properly plan for all external dependencies and integration points.
