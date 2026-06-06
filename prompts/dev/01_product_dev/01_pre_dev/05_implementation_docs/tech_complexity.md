---
name: tech-complexity-assessment
description: >
  Assess technical complexity and identify high-risk areas.
  Use before starting development to prioritize effort.
run: context_gated
run_when: Project is a software product with client-server architecture
produces: complexity_assessment
requires: [data_models, api_contracts, business_rules, solution_concept, feature_list]
tier: 2
---
For our solution concept: {{solution_concept}} with key features: {{feature_list}}, let's assess implementation complexity to inform planning.

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
