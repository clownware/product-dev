---
metadata:
  id: "impl.tech_complexity"
  slug: "tech-complexity-assessment"
  title: "Technical Complexity Assessment"
  version: "0.1.0"
  status: "active"
  phase: "dev"
  category: "Implementation"
  type: "instruction"
  folder: "05_implementation_docs"
  tags: ["implementation"]
  purpose: "Assess technical complexity and identify high-risk areas"
  context: "Use before starting development to prioritize effort"
  tier: 2
dependencies:
  requires: ["data_models","api_contracts","business_rules"]
  produces: ["complexity_assessment"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "complexity_assessment"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "tech_complexity_assessment"
---
For our solution concept: "[insert solution concept]" with key features: "[insert features]", let's assess implementation complexity to inform planning.

Please help me:

1. Break down each key feature into technical components
2. For each component:
   - Estimate relative complexity (High/Medium/Low)
   - Identify key technical challenges
   - Note dependencies on other components
   - Assess availability of existing libraries/solutions
   - Consider testing complexity

3. Identify cross-cutting technical concerns:
   - Performance considerations
   - Scalability factors
   - Security requirements
   - Accessibility needs
   - Cross-platform compatibility

4. Create a complexity/value matrix:
   - Map components by implementation effort vs. user value
   - Identify potential quick wins (high value, low effort)
   - Flag high-complexity items that might need rethinking

5. Suggest risk mitigation approaches:
   - Technical spikes or proof-of-concepts needed
   - Alternative approaches for high-risk elements
   - Phasing strategies to manage complexity

This assessment will help guide development planning, resource allocation, and technical risk management.
