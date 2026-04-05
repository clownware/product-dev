---
name: define-data-models
description: >
  Design core data models from solution concept and user flow.
  First step in the tech requirements sequence.
run: always
produces: data_models
requires: [solution_concept, user_flow]
tier: 1
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
