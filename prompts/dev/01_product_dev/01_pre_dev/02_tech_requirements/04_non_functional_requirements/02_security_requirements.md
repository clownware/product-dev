---
metadata:
  id: "tech.04_nfr.security_requirements"
  slug: "security-requirements"
  title: "Security Requirements"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Non-Functional Requirements"
  type: "instruction"
  folder: "04_non_functional_requirements"
  tags: ["nfr"]
  purpose: "Define security requirements and threat model"
  context: "Use when specifying authentication, authorization, and data protection needs"
  tier: 2
dependencies:
  requires: ["data_models","api_contracts"]
  produces: ["security_requirements"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "security_requirements"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "security_requirements"
---
Help me define comprehensive security requirements for our application:

1. Identify authentication and authorization needs
2. Specify data protection requirements (in transit and at rest)
3. Define input validation and sanitization requirements
4. Establish audit logging requirements
5. Specify compliance requirements (GDPR, HIPAA, etc. if applicable)
6. Define secure deployment practices
7. Establish penetration testing and security review processes

These requirements should address both technical and process aspects of security.
