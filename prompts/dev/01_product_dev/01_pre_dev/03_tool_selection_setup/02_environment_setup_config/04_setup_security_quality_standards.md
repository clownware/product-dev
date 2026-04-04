---
metadata:
  id: "setup.02_env.security_quality"
  slug: "setup-security-quality"
  title: "Setup Security & Quality Standards"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Environment Setup"
  type: "instruction"
  folder: "02_environment_setup_config"
  tags: ["setup"]
  purpose: "Configure security and quality tooling"
  context: "Use when setting up linting, SAST, and quality gates"
  tier: 3
dependencies:
  requires: ["security_requirements"]
  produces: ["security_quality_setup"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "security_quality_setup"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "setup_security_quality"
---
Help me set up security and code quality standards for our project.

Please recommend:
1. Static analysis tools appropriate for our tech stack
2. Security scanning configuration (SAST, dependency auditing)
3. Code quality rules and linting configuration
4. Pre-commit hooks for automated checks
5. CI/CD quality gates

Focus on practical, automatable standards that catch issues early.
