---
metadata:
  id: "tech.02_api_contracts.define_api_endpoints"
  slug: "define-api-endpoints"
  title: "Define API Endpoints"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "API Contracts & Interfaces"
  type: "instruction"
  folder: "02_api_contracts_interfaces"
  tags: ["mvp_feature"]
  purpose: "Create comprehensive API endpoint specifications"
  context: "Use after data models and user flows are defined"
  tier: 1
dependencies:
  requires: ["data_models","user_flow"]
  produces: ["api_contracts"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "api_contracts"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_api_endpoints"
---
Based on our User Flow Document and Data Models, help me define the API endpoints needed for this application.

For each endpoint:
1. Specify the HTTP method and route path
2. Define request parameters, headers, and body schema
3. Detail response format and status codes
4. Identify authentication and authorization requirements
5. Note rate limiting or caching considerations
6. Describe error handling approach
7. Explain how this endpoint supports specific user flows

The goal is to create a comprehensive API contract that can be implemented by the development team with high specificity and minimal ambiguity.
