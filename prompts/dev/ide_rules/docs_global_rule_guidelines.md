---
title: "AI-Native Developer System: Core Documents"
type: rules
scope: global
status: active
---
# AI-Native Developer System: Core Documents

## Document Architecture

|File|Purpose|Primary Audience|
|---|---|---|
|`global-rules.md`|Your developer OS: mindset, principles, architecture|LLMs|
|`ai-collab-guidelines.md`|Specific to how LLMs should behave inside tools|LLMs|
|`tech-stack-preferences.md`|Full toolchain, framework guidance|LLMs|
|`.windsurfrules`|Runtime agent context (minimal, project-local)|LLMs|

## Key Characteristics

- **Machine-First Design**: All documents are optimized for LLM consumption as rulesets
- **Minimal Context Loading**: Only load what's needed for the current task
- **Hierarchical Structure**: Project-specific overrides global defaults
- **Function-Oriented**: Each document has a specific, non-overlapping purpose

## System Operation

1. **Project Initialization**:
    
    - Create minimal `.windsurfrules` for the specific project
    - Optionally create project-specific context if needed
2. **LLM Runtime**:
    
    - `.windsurfrules` provides immediate project context
    - Global documents are referenced as needed:
        - `global-rules.md` for development philosophy
        - `tech-stack-preferences.md` for technical decisions
        - `ai-collab-guidelines.md` for response formatting
3. **Document Update Strategy**:
    
    - Update global documents when your overall approach changes
    - Keep `.windsurfrules` focused only on project-specific variations# AI-Native Developer System Structure

```
/windsurf-memory/
├── global-rules.md             # Behavioral guidance + system-wide dev philosophy
├── tech-stack-preferences.md   # Full dev stack & tooling strategy
├── ai-design-notes.md          # AI-specific interaction logic
├── project-context.md          # Template for local project intent + user stories
│
/projects/
├── project-name/
│   ├── .windsurfrules          # Minimal instructions for Cascade runtime
│   ├── project-context.md      # Project-specific implementation of template
│   └── [project files]
```

## System Components

1. **Global Rules (`global-rules.md`)**
    
    - Universal principles for AI agents and dev mindset
    - High-level behavioral approach and selection philosophy
    - Architecture principles and AI assistant guidelines
    - Core development tools
2. **Windsurf Rules (`.windsurfrules`)**
    
    - Project-level instructions for AI agents
    - Specific tech stack context for the current project
    - Code style and application structure guidelines
    - References to global rules and tech preferences
3. **Tech Stack Preferences (`tech-stack-preferences.md`)**
    
    - Comprehensive guide to technology options and tradeoffs
    - Framework selection guidelines based on project needs
    - Detailed breakdown of language, frontend, and backend preferences
    - Includes experimental tools and technologies to avoid
4. **AI Design Notes (`ai-design-notes.md`)**
    
    - AI agent routing commands and interaction patterns
    - Capabilities and access permissions for AI assistants
    - Contextual memory management guidelines
    - Project-specific adjustment mechanisms
5. **Project Context (`project-context.md`)**
    
    - Template for capturing project requirements and technical decisions
    - User stories and technical constraints
    - Project structure and development priorities
    - Special notes for AI assistants working on the project

## Usage

1. **For New Projects**
    
    - Copy `project-context.md` template into new project folder
    - Create project-specific `.windsurfrules` file
    - Fill in project details and technical decisions
2. **For AI Interactions**
    
    - Use routing commands to direct AI to specific information
    - Reference global rules for system-wide principles
    - Reference tech stack preferences for implementation details
    - Reference project-specific rules for local context
3. **For Human Developers**
    
    - Use as documentation of team standards and preferences
    - Reference for onboarding new team members
    - Living documentation that evolves with team experience