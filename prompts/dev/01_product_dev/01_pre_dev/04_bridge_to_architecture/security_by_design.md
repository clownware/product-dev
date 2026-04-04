---
metadata:
  id: "bridge.security_by_design"
  slug: "security-by-design"
  title: "Security by Design"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Bridge to Architecture"
  type: "instruction"
  folder: "04_bridge_to_architecture"
  tags: ["architecture"]
  purpose: "Embed security into the architecture from the start"
  context: "Use when designing system architecture with security as a first-class concern"
  tier: 2
dependencies:
  requires: ["security_requirements","data_models"]
  produces: ["security_design"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "security_design"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "security_by_design"
---
For our solution concept: "[insert solution concept]", let's establish a comprehensive security approach.

Please help me:

1. Identify security requirements across these dimensions:
   - Authentication & Identity
   - Authorization & Access Control
   - Data Protection & Privacy
   - Input Validation & Output Encoding
   - Session Management
   - API Security
   - Infrastructure Security

2. Assess potential threat vectors:
   - What are the most likely attack scenarios?
   - What data assets are most valuable/sensitive?
   - What user actions present the highest risk?

3. Define our security strategy:
   - Authentication approach (methods, MFA requirements, etc.)
   - Authorization model (roles, permissions, contexts)
   - Data protection measures (encryption at rest/in transit)
   - Input validation principles
   - Session handling approach
   - API security measures
   - Other security controls

4. Outline security implementation guidance:
   - Key security libraries or frameworks to leverage
   - Security testing approach
   - Security review checkpoints

This security-by-design approach ensures we address security proactively rather than as an afterthought.
