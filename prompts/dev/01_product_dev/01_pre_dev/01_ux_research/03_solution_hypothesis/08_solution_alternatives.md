---
metadata:
  id: "uxr.03_solution_hypothesis.solution_alternatives"
  slug: "solution-alternatives"
  title: "Solution Alternatives"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Solution Hypothesis"
  type: "instruction"
  folder: "03_solution_hypothesis"
  tags: ["value_prop"]
  purpose: "Explore multiple distinct solution approaches before committing to one"
  context: "Use after defining problem and objective to ensure broad solution exploration"
  tier: 3
dependencies:
  requires: ["problem_statement", "core_objective"]
  produces: ["alternative_solutions"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "alternative_solutions"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "solution_alternatives"
---

Based on our problem statement: "[insert problem statement]" and core objective: "[insert objective]", let's explore multiple potential solution approaches.

Please generate 3 distinct solution alternatives that:
1. Take meaningfully different approaches to solving the core problem
2. Represent different trade-offs or priorities
3. Each have potential to meet our success metrics

For each alternative:
1. Provide a concise description of the core concept (1-2 sentences)
2. Outline the key attributes or features (3-4 bullet points)
3. Explain the primary user benefit
4. Identify key strengths and potential advantages
5. Note key weaknesses or limitations
6. Assess feasibility for prototype development (high/medium/low)

After presenting the alternatives, compare them across:
1. Alignment with user needs
2. Potential impact on our success metrics
3. Implementation complexity
4. Risk profile
5. Uniqueness in the market

Conclude with a recommendation for which approach to pursue with clear rationale.

This exploration will ensure we've considered multiple pathways before committing to a specific direction.