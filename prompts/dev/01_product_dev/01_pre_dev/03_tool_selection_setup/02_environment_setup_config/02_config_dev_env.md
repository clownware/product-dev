---
metadata:
  id: "setup.02_env.config_dev_env"
  slug: "configure-dev-environment"
  title: "Configure Development Environment"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Environment Setup"
  type: "instruction"
  folder: "02_environment_setup_config"
  tags: ["setup"]
  purpose: "Set up the development environment"
  context: "Use when configuring IDE, linting, testing, and CI"
  tier: 2
dependencies:
  requires: ["tech_stack_evaluation"]
  produces: ["dev_env_config"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "dev_env_config"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "configure_dev_environment"
---
Based on our selected toolset, help me create configuration files and documentation for our development environment.

Generate the following:

1. Project README template with:
   - Project overview
   - Setup instructions
   - Development workflow guidelines
   - Tool usage instructions
   - Documentation references

2. Configuration file templates for:
   - VSCode/Windsurf settings.json
   - Extension recommendations (extensions.json)
   - Git configuration (.gitignore, .gitattributes)
   - Linting and formatting (.eslintrc, .prettierrc)
   - Build and package configuration

3. Docker/containerization setup if applicable:
   - Dockerfile
   - docker-compose.yml
   - Container startup scripts

4. CI/CD pipeline configuration:
   - GitHub Actions workflow definitions
   - Build and test scripts
   - Deployment configurations

5. Local environment setup script:
   - Dependencies installation
   - Environment variable configuration
   - Local service startup

Each configuration should align with our project requirements and chosen tools while following industry best practices. Include comments explaining key configuration choices and their rationale.
