---
metadata:
  id: "tech.04_nfr.performance_requirements"
  slug: "performance-requirements"
  title: "Performance Requirements"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Non-Functional Requirements"
  type: "instruction"
  folder: "04_non_functional_requirements"
  tags: ["nfr"]
  purpose: "Define performance targets and constraints"
  context: "Use when specifying how fast and responsive the system must be"
  tier: 2
dependencies:
  requires: ["solution_concept","user_flow"]
  produces: ["performance_requirements"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "performance_requirements"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "performance_requirements"
---
Help me define clear performance requirements for our application:

1. Specify expected response times for key operations
2. Define throughput requirements (transactions/users per time period)
3. Set targets for resource utilization (CPU, memory, network, storage)
4. Establish scalability expectations
5. Define acceptable degradation parameters under load
6. Specify monitoring and alerting thresholds

These requirements should be specific, measurable, and aligned with user expectations.
