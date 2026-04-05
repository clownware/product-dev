---
name: identify-data-access-patterns
description: >
  Determine how data will be accessed and queried.
  Use before database optimization and API design.
run: always
produces: identify_data_access_patterns
requires: []
tier: 2
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
