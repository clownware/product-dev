---
title: "Global Development Rules"
type: rules
scope: global
status: active
---
# 🔧 Global Development Rules

_Universal principles for AI agents and development mindset_

# Global Developer Principles

## 🧠 Mindset

"Take a stroll around the block to get some fresh air, then crack your knuckles, chug a Diet Coke, and LOCK IN."

_Note: This personal mantra represents an individual developer approach to getting into a focused state. For team settings, adapt tone as appropriate._

## 🧭 Strategic Thinking

- Understand the full problem before acting
- Start from a clear PRD or create one
- Consider tradeoffs, debt, and scaling early

## 🎨 Creative Problem-Solving

- Propose multiple paths forward
- Prefer elegance and simplification
- Improve patterns, don't just follow them

## 🔐 Security-First Development

- Never hardcode secrets
- Validate and sanitize all input
- Enforce least privilege; keep dependencies current

## 🧱 Technical Excellence

- Prioritize readability and testability
- Think through edge cases
- Document non-obvious decisions

## 🤝 Collaborative Development

- Write code as if the next developer will need to understand your reasoning
- Make self-contained PRs
- Communicate reasoning clearly

_Note: The original guideline used colorful language ("as if the next dev is an assassin") to emphasize the importance of writing clear, maintainable code. The principle is about anticipating future developers' needs._

## 🔁 Iterative Improvement

- Break things down
- Prototype novel approaches
- Use each iteration to learn and refine

## 🧼 Project Hygiene

- Isolate config from code
- Commit in small, atomic units
- Remove deprecated code
- Keep logs and temp files out of Git

## 📚 Learning Mindset

- Teach as you go
- Document discoveries
- Improve your understanding over time

## ✅ Best Practices

- Use semantic versioning
- Follow idiomatic patterns
- Build accessible, performant, documented systems

## 🎯 Behavioral Approach

- Start by understanding project requirements before suggesting technologies
- Present trade-offs and comparisons between relevant options
- Consider "right-sizing" the stack to the project needs
- When in doubt, favor simplicity and performance over feature richness
- Always explain the reasoning behind recommendations
- Be willing to challenge assumptions when a different approach might be more suitable

## 💡 Selection Philosophy

- **Project-specific requirements** first and foremost
    
    - Consider performance needs, target audience, and content type
    - Evaluate complexity vs. simplicity trade-offs for each project
    - Assess development speed and maintenance requirements
- Technical considerations:
    
    - Modern, performant, and scalable with strong developer experience
    - Well-maintained and actively developed
    - Appropriate bundle size and runtime performance
    - Server vs. client rendering balance for the specific use case
- Team considerations:
    
    - Align with team skills when practical
    - Consider onboarding and training requirements
    - Prefer technologies that promote code quality and maintainability

## 📐 Architecture Principles

- Prefer composable, modular systems over monolithic approaches
- Build with clear separation of concerns
- Optimize for maintainability and readability first
- Design for performance but not at the expense of developer experience
- Balance technical debt against delivery timelines
- Implement the simplest solution that meets requirements
- Default to established patterns unless there's clear benefit to innovation

# Developer Environment Context

_The following tools represent the current development environment. This provides context for AI assistants but may evolve over time._

- Primary IDE: VSCode (with modern extensions)
- Code Assistant: AI-powered coding assistants integrated with IDE
- Version Control: Git
- Containers: Docker
- Design & UI Collaboration: Figma
- Team Suite: Google Workspace
- Knowledge Base: Obsidian
- Reference Management: Zotero
- External AI Assistants: Claude, ChatGPT, Perplexity, Gemini