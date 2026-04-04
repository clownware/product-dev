---
metadata:
  id: "bridge.api_first_planning"
  slug: "api-first-planning"
  title: "API-First Planning"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Bridge to Architecture"
  type: "instruction"
  folder: "04_bridge_to_architecture"
  tags: ["architecture"]
  purpose: "Plan API-first development approach"
  context: "Use when designing the system as API-first"
  tier: 2
dependencies:
  requires: ["api_contracts","data_models"]
  produces: ["api_first_plan"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "api_first_plan"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "api_first_planning"
---
Based on our solution concept: "[insert solution concept]" and user flows, let's define the API contract that will support our application.

Please help me:

1. Identify all necessary API endpoints based on user interactions
2. For each endpoint:
   - Define the HTTP method (GET, POST, PUT, DELETE, etc.)
   - Specify the route/URL pattern
   - Detail request parameters and body schema
   - Define response structure and status codes
   - Document authentication requirements
   - Note rate limiting or other constraints

3. Define standard data structures that will be used across endpoints

4. Provide example request/response pairs for key endpoints

5. Consider:
   - Error handling approach
   - Versioning strategy
   - Content negotiation
   - Caching directives
   - Pagination for list endpoints

This API contract will serve as the foundation for both frontend and backend development, enabling parallel work streams and clear interface boundaries.
