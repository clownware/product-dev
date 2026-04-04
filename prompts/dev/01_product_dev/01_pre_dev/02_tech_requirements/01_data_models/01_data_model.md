---
metadata:
  id: "tech.01_data_models.define_data_models"
  slug: "define-data-models"
  title: "Define Core Data Models"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Data Models"
  type: "instruction"
  folder: "01_data_models"
  tags: ["mvp_feature"]
  purpose: "Design essential data models based on solution requirements"
  context: "Use after user flow and solution hypothesis are established"
  tier: 2
dependencies:
  requires: []
  produces: []
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "define_data_models"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "define_data_models"
---
Based on our Solution Hypothesis Document, help me define the core data models needed for this project.

For each data model:
1. Provide a clear name and description of what this entity represents
2. List all required attributes/fields with their types and constraints
3. Define relationships between this model and other models
4. Identify any unique constraints or validation rules
5. Mark attributes as required vs optional
6. Note any specific indexing needs for performance
7. Identify any special data handling requirements (encryption, etc.)

Focus on creating a clean domain model that accurately represents the essential data structures without over-engineering. The goal is high specificity that will guide development.
