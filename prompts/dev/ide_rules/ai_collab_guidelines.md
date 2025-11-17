---
title: "AI Collaboration Guidelines"
type: rules
scope: global
status: active
---
# AI Collaboration Guidelines

_How AI assistants should interact with developers in this environment_

## Communication Principles

- Be concise but thorough in responses
- Include rationale for technical recommendations
- Default to TypeScript when showing code examples
- Provide context about why certain approaches are recommended
- Compare alternatives when appropriate
- Format code examples with proper markdown and syntax highlighting
- Use descriptive variable and function names in examples
- For complex solutions, break down explanations step by step

## Response Format

- Start with a direct answer to the question when possible
- Use markdown for formatting and code blocks
- Structure complex responses with clear headings
- Include links to documentation when referencing external resources
- Label examples clearly
- Use tables for comparing multiple options

## Code Generation

- Generate complete, functional components
- Include TypeScript types and interfaces
- Follow project structure from .windsurfrules
- Add meaningful comments for complex logic
- Ensure error handling for all async operations

## Code Review

- Focus on:
    - TypeScript type safety
    - Performance optimizations
    - Security considerations
    - Adherence to project structure
    - Consistency with existing codebase

## Architecture Discussions

- Start with requirements analysis
- Present multiple approaches with tradeoffs
- Consider performance, maintainability, and DX
- Reference specific sections from tech-stack-preferences.md
- Provide diagrams or visualizations when helpful

## AI Routing Commands

Use these commands to direct AI assistants to the right information source:

```
> Search tech-stack-preferences.md for "best framework for content-heavy sites"
> Load global-rules.md to evaluate tradeoffs for Bun vs Node
> Reference windsurfrules for code style guidelines
```