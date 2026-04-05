---
name: setup-security-quality
description: >
  Configure security and quality tooling.
  Use when setting up linting, SAST, and quality gates.
run: always
produces: security_quality_setup
requires: [security_requirements]
tier: 3
---
Help me set up security and code quality standards for our project.

Please recommend:
1. Static analysis tools appropriate for our tech stack
2. Security scanning configuration (SAST, dependency auditing)
3. Code quality rules and linting configuration
4. Pre-commit hooks for automated checks
5. CI/CD quality gates

Focus on practical, automatable standards that catch issues early.
