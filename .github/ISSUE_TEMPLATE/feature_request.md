---
name: Feature request
about: Suggest a new prompt, skill, command, validation check, or schema extension
title: 'feat: '
labels: enhancement
assignees: ''
---

## Problem

What can't you do today, or what's painful about the current workflow? Be specific about where in the pipeline this surfaces (which phase, which command, which artifact).

## Proposal

What you'd like to see. If this is a prompt or skill change, sketch the conversational flow. If this is a schema or validation change, sketch the YAML.

## Why this fits the framework

This project is a **spec package compiler** (see ADR 0010). Features land if they make the compiler produce better spec packages, the prompts produce better artifacts, or the framework consumes less builder time. Features that add team-collaboration, project-management, or methodology-instruction surface area are out of scope (see `docs/updates/prd-v3.md` § Scope Boundaries).

Tell us how this fits.

## Alternatives considered

Anything else you tried, or any existing prompt / command / script that gets close.

## Affected components

- [ ] New / changed prompt (specify path)
- [ ] New / changed skill or command
- [ ] Spec package schema (`docs/spec-package-schema.md`)
- [ ] Validation check
- [ ] Compilation step
- [ ] Handoff format
- [ ] MCP server
- [ ] Documentation only

## Would this need a new ADR?

If yes, briefly describe the decision.
