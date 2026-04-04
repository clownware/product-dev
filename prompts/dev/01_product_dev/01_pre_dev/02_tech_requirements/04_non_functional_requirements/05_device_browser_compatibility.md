---
metadata:
  id: "tech.04_nfr.device_browser_compatibility"
  slug: "device-browser-compatibility"
  title: "Device & Browser Compatibility"
  version: "0.1.0"
  status: "active"
  phase: "spec"
  category: "Non-Functional Requirements"
  type: "instruction"
  folder: "04_non_functional_requirements"
  tags: ["nfr"]
  purpose: "Define device and browser support requirements"
  context: "Use when specifying cross-platform compatibility targets"
  tier: 3
dependencies:
  requires: ["platform_strategy"]
  produces: ["compatibility_requirements"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "compatibility_requirements"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "device_browser_compatibility"
---
Help me define device and browser compatibility requirements for our application:

1. Specify which desktop browsers must be supported (versions and market share)
2. Identify mobile device requirements (operating systems, screen sizes)
3. Define minimum specifications for acceptable performance
4. Establish progressive enhancement and graceful degradation approaches
5. Specify testing procedures across different environments
6. Define any special device feature requirements (touch, camera, GPS, etc.)

These requirements should ensure our application works well across our target user environments.
