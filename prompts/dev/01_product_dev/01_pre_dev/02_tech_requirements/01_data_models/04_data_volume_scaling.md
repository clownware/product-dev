---
metadata:
  id: "tech.01_data_models.assess_data_volume_scaling"
  slug: "assess-data-volume-scaling"
  title: "Assess Data Volume & Scaling"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Data Models"
  type: "instruction"
  folder: "01_data_models"
  tags: ["mvp_feature"]
  purpose: "Project data growth and scaling requirements"
  context: "Use for capacity planning and architecture decisions"
  tier: 2
dependencies:
  requires: []
  produces: []
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "assess_data_volume_scaling"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "assess_data_volume_scaling"
---
Help me assess the expected data volume and scaling needs for our application:

1. Estimate the growth rate of each core data model
2. Identify which models will have the highest volume
3. Project storage requirements over time (1 month, 6 months, 1 year)
4. Determine which queries might become problematic at scale
5. Suggest appropriate data partitioning or sharding strategies if needed
6. Identify potential bottlenecks in our data architecture

This assessment will help us make informed decisions about storage solutions and scaling strategies.
