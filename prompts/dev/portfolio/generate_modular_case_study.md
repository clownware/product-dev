You're helping draft a case study for a developer portfolio designed for time-constrained product leaders, founders, and hiring managers. This portfolio prioritizes **process clarity**, **systems thinking**, and **AI-native workflows**. The case study should follow a modular format and help the reviewer quickly answer:

> “Can this person solve problems the way we need?”

---

🧠 **Instructions:**

Use the following MDX case study structure to generate high-signal content. Assume this will be rendered on a developer portfolio site using Astro Content Collections.

⚠️ **Input Quality Reminder:**  
The quality of your output depends entirely on the quality of the project notes provided. Strong inputs include:  
- Clear project scope and outcomes  
- Detailed process steps and decisions  
- How AI was used or influenced the work  
- Any diagrams, frameworks, or system maps  
- Your specific role and contributions

---

📦 **MDX Template to Fill Out:**

```mdx
---
title: "Project Title"
summary: "Concise 1–2 sentence summary of your process and systems thinking"
role: "Your role (e.g. Product Designer, Prompt Engineer)"
outcome: "What changed as a result—clear and credible"
tags: ["LLM Integration", "Prompt Engineering", "System Design"]  # Suggest relevant tags
date: "2025-04-19"
---

<ProcessSummary>
Write a short, scannable summary (2–3 sentences):
- What problem or opportunity was addressed?
- How was it tackled?
- What was the outcome?
</ProcessSummary>

<ExpandableSection title="📍 Context & Challenge">
Describe the environment, problem, and constraints:
- What made the challenge non-trivial?
- Why was this work important to the team/org/user?
</ExpandableSection>

<ExpandableSection title="🧠 Process & Systems Thinking">
Explain your reasoning:
- How did you break the problem down?
- Any system maps, mental models, or feedback loops?
- Frameworks or decision patterns used?
</ExpandableSection>

<AnnotatedDiagram 
  imageSrc="/images/case-studies/[your-diagram].png" 
  alt="Diagram describing system or process"
>
(Optional) Diagram suggestion: consider a flow chart, feedback loop, architecture model, or system diagram that visualizes your thinking.
</AnnotatedDiagram>

<DecisionLog decisions={[
  {
    decision: "Key technical or design decision",
    rationale: "Why it was made",
    tradeoffs: "What you sacrificed or considered"
  },
  {
    decision: "Second major decision",
    rationale: "...",
    tradeoffs: "..."
  }
]} />

<AIWorkflowSection
  steps={[
    { label: "Prompt Design", detail: "Describe how prompts were structured or refined" },
    { label: "AI Collaboration", detail: "How AI tools like Claude, GPT, or Midjourney were integrated into your workflow" },
    { label: "Attribution", detail: "Clarify which parts were AI-generated vs human-authored" }
  ]}
/>

<ExpandableSection title="🧰 Role & Contribution">
Make your scope clear:
- What did you personally own?
- What was collaborative?
- Any leadership or cross-functional glue work?
</ExpandableSection>

<ExpandableSection title="📈 Outcome & Impact">
Describe tangible results:
- Metrics or qualitative feedback?
- Improvements in speed, clarity, experience, or decision-making?
</ExpandableSection>

<ExpandableSection title="🔁 Retrospective">
Show reflection:
- What would you improve or do differently?
- Any lessons, mindset shifts, or unexpected complexity?
</ExpandableSection>
