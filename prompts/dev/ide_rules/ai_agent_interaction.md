---
title: "AI Agent Interaction Guidelines"
type: rules
scope: global
status: active
---
# Rule Hierarchy & Decision-Making

1. **Project Requirements** trump all other considerations
    
    - The needs of the specific project always come first
    - Technical decisions should be driven by actual requirements, not preferences
2. **Global Developer Principles** guide the decision-making process
    
    - The principles in global-rules.md establish the _approach_ to solving problems
    - They define how to evaluate solutions, not which specific technologies to use
3. **Tech Stack Preferences** provide implementation guidance
    
    - These are defaults and starting points, not rigid requirements
    - They can be overridden when project needs or global principles suggest a better alternative
4. **Project-Specific Rules** (.windsurfrules) apply to a specific codebase
    
    - These maintain consistency within an established project
    - They represent concrete decisions already made for that specific project

When contradictions arise between these levels, generally prefer:

1. Project requirements (highest priority)
2. Project-specific rules for that codebase
3. Global developer principles
4. Tech stack preferences (lowest priority)# AI Agent Interaction Guidelines

_Specific instructions for AI agents working in this development environment_

## Memory Loading Structure

For AI assistants working on projects, follow this memory loading sequence:

1. **Project-specific context**
    
    - `project-context.md` - Contains specific project requirements and decisions
    - `.windsurfrules` - Contains minimal runtime instructions for this project
2. **Global guidance documents**
    
    - `global-rules.md` - Core development principles and philosophy
    - `tech-stack-preferences.md` - Technical stack options and selection criteria
    - `ai-collab-guidelines.md` - How AI assistants should interact and respond

This structure allows AI assistants to understand:

- The specific project they're working on
- The global principles that guide development
- The technical options available and when to use them
- How to communicate effectively with developers

## AI Agent Routing Commands

Use these commands to direct AI assistants to the right information source:

```
> Search tech-stack-preferences.md for "best framework for content-heavy sites"
> Load global-rules.md to evaluate tradeoffs for Bun vs Node
> Reference windsurfrules for code style guidelines
```

## Agent Capabilities & Access

- AI agents have read access to:
    
    - global-rules.md
    - tech-stack-preferences.md
    - .windsurfrules
    - project-context.md (project-specific)
    - Repository code and documentation
- Default behavior expectations:
    
    - Follow global rules for reasoning and recommendations
    - Apply project-specific rules from .windsurfrules
    - Reference tech stack preferences for implementation details
    - Explain rationale for technical decisions

## Preferred Interaction Patterns

### Code Generation

- Generate complete, functional components
- Include TypeScript types and interfaces
- Follow project structure from .windsurfrules
- Add meaningful comments for complex logic
- Ensure error handling for all async operations

### Code Review

- Focus on:
    - TypeScript type safety
    - Performance optimizations
    - Security considerations
    - Adherence to project structure
    - Consistency with existing codebase

### Architecture Discussions

- Start with requirements analysis
- Present multiple approaches with tradeoffs
- Consider performance, maintainability, and DX
- Reference specific sections from tech-stack-preferences.md
- Provide diagrams or visualizations when helpful

## Contextual Memory Management

When working on a project, AI agents should:

1. First load global-rules.md for high-level principles
2. Then load project-specific .windsurfrules
3. Reference tech-stack-preferences.md for implementation details
4. Maintain context of the current task and project state

## Project-Specific Adjustments

Specific projects may override certain defaults. When they do:

1. Project-specific rules (.windsurfrules) take precedence
2. Global rules (global-rules.md) apply where not overridden
3. When conflicts exist, prefer the more specific/local rule