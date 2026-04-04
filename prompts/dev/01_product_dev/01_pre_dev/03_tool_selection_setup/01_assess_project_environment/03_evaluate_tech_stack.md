---
metadata:
  id: "setup.01_assess.tech_stack"
  slug: "evaluate-tech-stack"
  title: "Evaluate Tech Stack"
  version: "0.1.0"
  status: "active"
  phase: "design"
  category: "Tool Selection & Setup"
  type: "instruction"
  folder: "01_assess_project_environment"
  tags: ["setup"]
  purpose: "Evaluate and select technology stack"
  context: "Use when choosing languages, frameworks, and infrastructure"
  tier: 2
dependencies:
  requires: ["solution_concept","data_models"]
  produces: ["tech_stack_evaluation"]
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "tech_stack_evaluation"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "evaluate_tech_stack"
---
Based on our project requirements, help me evaluate and select the optimal technology stack for this project.

For each layer of the stack, provide:

1. Frontend Framework:
   - Confirm if Next.js with App Router is optimal for our requirements
   - Assess any specific Next.js features we should leverage
   - Identify any potential limitations or challenges

2. UI Component Strategy:
   - Evaluate if shadcn/ui with Tailwind CSS is the best approach
   - Suggest component structure and organization
   - Recommend state management approach

3. API Architecture:
   - Assess REST vs. GraphQL for our specific needs
   - Evaluate API gateway requirements
   - Suggest authentication and authorization implementations

4. Backend Services:
   - Evaluate serverless vs. containerized approaches
   - Assess microservices vs. monolith for our use case
   - Recommend specific backend frameworks

5. Database Selection:
   - Evaluate SQL vs. NoSQL based on our data models
   - Assess specific database technologies (PostgreSQL, etc.)
   - Suggest data access patterns and ORM approach

6. Infrastructure & Deployment:
   - Assess Vercel vs. alternatives for our specific needs
   - Evaluate containerization requirements
   - Suggest environment management strategy

For each recommendation, provide:
- Pros and cons relative to alternatives
- Specific justification based on our requirements
- Potential risks or limitations to be aware of
- Implementation considerations

The goal is to select a cohesive stack that optimally supports our specific requirements while leveraging team expertise and ensuring maintainability.
