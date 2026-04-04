---
metadata:
  id: "uxr.00_fuzzy_front_end.explore_user_segments"
  slug: "explore-user-segments"
  title: "Explore User Segments"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Early Ideation & Exploration"
  type: "instruction"
  folder: "00_fuzzy_front_end"
  tags: ["problem"]
  purpose: "Identify and analyze potential user segments for the problem space"
  context: "Use when determining which user segment to target initially"
  tier: 2
dependencies:
  requires: []
  produces: ["user_segment_analysis"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "user_segment_analysis"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "explore_user_segments"
---
For the problem area we're exploring in [specific domain], help me identify and compare potential user segments who might benefit from a solution.

Please help me:

1. Identify 4-6 distinct user segments who might experience this problem
2. For each segment:
   - Describe their key characteristics and context
   - Outline their primary goals and pain points related to our problem area
   - Note their likely frequency and severity of experiencing the problem
   - Consider their willingness to adopt new solutions
3. Compare these segments across:
   - Size and accessibility (how easy to reach)
   - Specificity of needs (how unique are their requirements)
   - Potential impact of solving their problem
   - Resource requirements to serve them well
4. Recommend 1-2 most promising segments to focus on initially with clear rationale

This exploration will help us prioritize which user segment to focus on first, ensuring we design for a specific group with well-understood needs rather than trying to solve for everyone.
