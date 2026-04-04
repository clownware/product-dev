---
metadata:
  id: "setup.03_collab.version_control"
  slug: "strategize-version-control"
  title: "Strategize Version Control"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Team Collaboration"
  type: "instruction"
  folder: "03_team_collaboration_setup"
  tags: ["setup"]
  purpose: "Define branching strategy and version control practices"
  context: "Use when setting up Git workflow for the team"
  tier: 2
dependencies:
  requires: ["team_workflow"]
  produces: ["version_control_strategy"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "version_control_strategy"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "strategize_version_control"
---
Help me define a version control strategy that supports our AI-powered development workflow.

Please address:

1. Branch Strategy:
   - Branch naming conventions
   - Branch types (feature, bug, release, etc.)
   - Protection rules for key branches
   - Integration with CI/CD

2. Commit Standards:
   - Commit message format
   - Conventional commits implementation
   - Code authorship attribution for AI-generated code
   - Linking commits to issues/tasks

3. Pull Request Process:
   - PR template structure
   - Review requirements
   - Automated checks for PRs
   - AI-assisted code review integration

4. Release Management:
   - Versioning scheme
   - Release branch strategy
   - Changelogs and release notes
   - Hotfix procedures

5. Git Workflow:
   - Rebase vs. merge strategy
   - Conflict resolution approach
   - Large file handling
   - History management

This strategy should facilitate collaboration, ensure code quality, and provide clear traceability while adapting to the unique aspects of AI-assisted development.
