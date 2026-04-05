---
name: validate-data-model
description: >
  Review data models for completeness and potential issues.
  Use after initial data model design for quality check.
run: always
produces: data_model_validation
requires: [data_models]
tier: 2
---
For our defined data models, help me identify potential issues or improvements:

1. Are there any missing attributes that would be required for the identified user flows?
2. Do the relationships between models accurately reflect real-world connections?
3. Are there any potential data integrity concerns?
4. How well do these models support our core success metrics?
5. What edge cases should we consider in our data modeling?
6. Are there any performance implications we should address?

This validation will help ensure our data models are robust and well-aligned with our business needs.
