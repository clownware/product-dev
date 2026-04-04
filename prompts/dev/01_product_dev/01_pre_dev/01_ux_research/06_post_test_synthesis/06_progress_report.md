---
metadata:
  id: "uxr.06_post_test_synthesis.progress_report"
  slug: "progress-report"
  title: "Progress Report"
  version: "0.1.0"
  status: "active"
  phase: "discovery"
  category: "Post-Test Analysis"
  type: "instruction"
  folder: "06_post_test_synthesis"
  tags: ["mvp_feature"]
  purpose: "Generate a structured progress report for stakeholders"
  context: "Use to communicate findings to team or stakeholders"
  tier: 3
dependencies:
  requires: ["hypothesis_evaluation"]
  produces: ["progress_report"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "progress_report"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "progress_report"
---
Help me create a progress report summarizing our work so far.

Include:
1. Problem statement and who it affects
2. Our hypothesis and how we tested it
3. Key findings (what worked, what didn't, surprises)
4. Current confidence level and evidence
5. Recommended next steps
6. Open questions and risks

Format for a non-technical audience. Keep it under 1 page.
