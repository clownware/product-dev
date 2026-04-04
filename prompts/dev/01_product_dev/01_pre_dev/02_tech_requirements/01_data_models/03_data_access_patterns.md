---
metadata:
  id: "tech.01_data_models.identify_data_access_patterns"
  slug: "identify-data-access-patterns"
  title: "Identify Data Access Patterns"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Data Models"
  type: "instruction"
  folder: "01_data_models"
  tags: ["mvp_feature"]
  purpose: "Determine how data will be accessed and queried"
  context: "Use before database optimization and API design"
  tier: 2
dependencies:
  requires: []
  produces: []
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "identify_data_access_patterns"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "identify_data_access_patterns"
---
Based on our user flows and data models, help me identify the key data access patterns for this application:

1. What are the most frequent data retrieval operations?
2. Which queries will need to be optimized for performance?
3. What aggregations or complex queries will be required?
4. Are there any time-series or analytical queries needed?
5. Which data operations might benefit from caching?
6. Are there any patterns that suggest denormalization might be beneficial?

For each pattern, suggest:
- The optimal query structure
- Any indexing recommendations
- Performance considerations
- Potential optimizations

Understanding these patterns will inform our database design decisions and API implementation strategy.
