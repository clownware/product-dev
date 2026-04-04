---
metadata:
  id: "tech.01_data_models.validate_data_model"
  slug: "validate-data-model"
  title: "Validate Data Model"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Data Models"
  type: "instruction"
  folder: "01_data_models"
  tags: ["mvp_feature"]
  purpose: "Review data models for completeness and potential issues"
  context: "Use after initial data model design for quality check"
  tier: 2
dependencies:
  requires: ["data_models"]
  produces: ["data_model_validation"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "data_model_validation"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "validate_data_model"
---
For our defined data models, help me identify potential issues or improvements:

1. Are there any missing attributes that would be required for the identified user flows?
2. Do the relationships between models accurately reflect real-world connections?
3. Are there any potential data integrity concerns?
4. How well do these models support our core success metrics?
5. What edge cases should we consider in our data modeling?
6. Are there any performance implications we should address?

This validation will help ensure our data models are robust and well-aligned with our business needs.
