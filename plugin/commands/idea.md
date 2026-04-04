---
name: idea
description: Start exploring a product idea or problem domain
arguments:
  - name: concept
    description: Optional concept or domain to explore
    required: false
---

Start a product ideation session using the `product-ideation` skill.

## Setup

1. Check if `.product-dev/context.json` exists in the working directory.
   - If not, create the project: initialize `.product-dev/context.json` with timestamps, `tier: 1`, empty artifacts and prompts_executed. Ask the user for a project name.
   - If it exists, read it and briefly note existing progress.

2. Determine entry point from user input:
   - If `$ARGUMENTS` contains a specific product idea (e.g., "tea tracking app") → use `capture_idea` prompt
   - If `$ARGUMENTS` describes a domain interest (e.g., "problems in specialty tea") → use `explore_problem` prompt
   - If no arguments provided → ask: "What's on your mind? Tell me about the idea, problem, or space you're interested in."

3. Read the selected prompt from `prompts/dev/01_product_dev/01_pre_dev/01_ux_research/00_fuzzy_front_end/` and execute it.

4. After producing output, write the artifact to `.product-dev/artifacts/initial_concept.md` and update the registry.

5. Continue the `product-ideation` skill flow: advance through the prompt chain conversationally, checking tier escalation signals after each user response.
