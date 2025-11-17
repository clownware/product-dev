---
title: "Prompt: {{title}}"
type: prompt
status: complete
created: {{date:YYYY-MM-DD}}
modified: {{date:YYYY-MM-DD}}
category: [design|development|project_management|research|creative]
subcategory: [ux|ui|vscode|role|llm_eval|writing]
target_model: ["GPT-4o"]
use_case: ""
source: [original|adapted|collaborative]
effectiveness_score: # optional: 1-10
ai_analyzed: yes
ai_version: "Claude 3.7"
ai_feedback:
  strengths: []
  blind_spots: []
  next_questions: []
related_sources: []
tags: []
ai_tags: []
---
# [Project Name]

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#project-name)

Every time you choose to apply a rule(s), explicitly state the rule(s) in the output. You can abbreviate the rule description to a single word or phrase.

## Project Context

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#project-context)

[Brief description ]

- [more description]
- [more description]
- [more description]

## Code Style and Structure

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#code-style-and-structure)

- Write concise, technical TypeScript code with accurate examples
- Use functional and declarative programming patterns; avoid classes
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Structure repository files as follows:

```
server/
├── src/
    ├── components/     # Shared React components
    ├── hooks/          # Custom React hooks
    ├── utils/          # Helper functions
    ├── types/          # TypeScript types
    └── lib/            # Shared libraries
extension/
├── src/
    ├── background/     # Service worker scripts
    ├── content/        # Content scripts
    ├── popup/          # Extension popup UI
    ├── options/        # Extension options page
    ├── components/     # Shared React components
    ├── hooks/          # Custom React hooks
    ├── utils/          # Helper functions
    ├── lib/            # Shared libraries
    ├── types/          # TypeScript types
    └── storage/        # Chrome storage utilities
shared/
├── src/
    ├── types/          # TypeScript types, only used for shared types between server and extension
    └── utils/          # Helper functions, only used for shared functions between server and extension
```

## Tech Stack

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#tech-stack)

- React
- TypeScript
- Tailwind CSS
- Shadcn UI
- Chrome Extension
- Express.js

## Naming Conventions

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#naming-conventions)

- Use lowercase with dashes for directories (e.g., components/form-wizard)
- Favor named exports for components and utilities
- Use PascalCase for component files (e.g., VisaForm.tsx)
- Use camelCase for utility files (e.g., formValidator.ts)

## TypeScript Usage

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#typescript-usage)

- Use TypeScript for all code; prefer interfaces over types
- Avoid enums; use const objects with 'as const' assertion
- Use functional components with TypeScript interfaces
- Define strict types for message passing between different parts of the extension
- Use absolute imports for all files @/...
- Avoid try/catch blocks unless there's good reason to translate or handle error in that abstraction
- Use explicit return types for all functions

## Chrome Extension Specific

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#chrome-extension-specific)

- Use Manifest V3 standards
- Implement proper message passing between components:
    
    ```ts
    interface MessagePayload {
      type: string;
      data: unknown;
    }
    ```
    
- Handle permissions properly in manifest.json
- Use chrome.storage.local for persistent data
- Implement proper error boundaries and fallbacks
- Use lib/storage for storage related logic
- For the async injected scripts in content/,
    - they must not close over variables from the outer scope
    - they must not use imported functions from the outer scope
    - they must have wrapped error handling so the error message is returned to the caller

## State Management

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#state-management)

- Use React Context for global state when needed
- Implement proper state persistence using chrome.storage (for extension)
- Implement proper cleanup in useEffect hooks

## Syntax and Formatting

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#syntax-and-formatting)

- Use "function" keyword for pure functions
- Avoid unnecessary curly braces in conditionals
- Use declarative JSX
- Implement proper TypeScript discriminated unions for message types

## UI and Styling

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#ui-and-styling)

- Use Shadcn UI and Radix for components
- use `npx shadcn@latest add <component-name>` to add new shadcn components
- Implement Tailwind CSS for styling
- Consider extension-specific constraints (popup dimensions, permissions)
- Follow Material Design guidelines for Chrome extensions
- When adding new shadcn component, document the installation command

## Error Handling

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#error-handling)

- Implement proper error boundaries
- Log errors appropriately for debugging
- Provide user-friendly error messages
- Handle network failures gracefully

## Testing

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#testing)

- Write unit tests for utilities and components
- Implement E2E tests for critical flows
- Test across different Chrome versions
- Test memory usage and performance

## Security

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#security)

- Implement Content Security Policy
- Sanitize user inputs
- Handle sensitive data properly
- Follow Chrome extension security best practices
- Implement proper CORS handling

## Git Usage

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#git-usage)

Commit Message Prefixes:

- "fix:" for bug fixes
- "feat:" for new features
- "perf:" for performance improvements
- "docs:" for documentation changes
- "style:" for formatting changes
- "refactor:" for code refactoring
- "test:" for adding missing tests
- "chore:" for maintenance tasks

Rules:

- Use lowercase for commit messages
- Keep the summary line concise
- Include description for non-obvious changes
- Reference issue numbers when applicable

## Documentation

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#documentation)

- Maintain clear README with setup instructions
- Document API interactions and data flows
- Keep manifest.json well-documented
- Don't include comments unless it's for complex logic
- Document permission requirements

## Development Workflow

[](https://gist.github.com/yifanzz/3cfb8f9065769ffbf94348255f85597d#development-workflow)

- Use proper version control
- Implement proper code review process
- Test in multiple environments
- Follow semantic versioning for releases
- Maintain changelog