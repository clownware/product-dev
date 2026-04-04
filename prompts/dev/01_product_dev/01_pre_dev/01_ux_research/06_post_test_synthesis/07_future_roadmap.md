---
metadata:
  id: "uxr.06_post_test_synthesis.future_roadmap"
  slug: "future-roadmap"
  title: "Future Roadmap"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Post-Test Analysis"
  type: "instruction"
  folder: "06_post_test_synthesis"
  tags: ["mvp_feature"]
  purpose: "Define a forward-looking roadmap based on validated learnings"
  context: "Use after completing a test cycle to plan ahead"
  tier: 3
dependencies:
  requires: ["iteration_plan"]
  produces: ["future_roadmap"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "future_roadmap"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "future_roadmap"
---
Based on everything we've learned, help me outline a forward-looking roadmap.

Please define:
1. Immediate next steps (next 1-2 weeks)
2. Short-term goals (next 1-3 months)
3. Medium-term vision (3-6 months)
4. Key milestones and decision points
5. Assumptions that need continued validation
6. Resources or capabilities we'll need

This roadmap should be grounded in what we've validated, not speculation.
