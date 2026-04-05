---
name: api-first-planning
description: >
  Plan API-first development approach.
  Use when designing the system as API-first.
run: always
produces: api_first_plan
requires: [api_contracts, data_models]
tier: 2
---
Based on our solution concept: {{solution_concept}} and user flows, let's define the API contract that will support our application.

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
