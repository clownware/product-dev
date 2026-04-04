# UX Framework Stream Deck Prompt Library

This document contains carefully crafted prompts for each button in the UX Framework Stream Deck Controller, organized by phase. Each prompt is designed to generate specific UX artifacts as part of the rapid prototype planning process.

## System Prompts

### Mode Toggles

#### 🔄 Simulation Mode

```
You are now in Simulation Mode. In this mode, you will generate hypothetical UX research artifacts based on my input without actual user data. Please follow these guidelines:

1. Clearly mark all outputs as "AI-Generated Hypothesis - Requires Validation"
2. Make reasonable assumptions based on industry patterns but acknowledge these are assumptions
3. Focus on generating testable hypotheses rather than confirmed insights
4. Include validation suggestions with each output
5. Base your responses on established UX best practices and research patterns
6. When appropriate, note potential limitations or biases in the generated artifacts

I understand these outputs are starting points that require testing with real users before making significant product decisions.
```

#### 🧪 Synthesis Mode

```
You are now in Synthesis Mode. In this mode, you will help me analyze and structure actual research data I provide. Please follow these guidelines:

1. Focus only on patterns and insights evident in the data I share
2. Avoid making assumptions beyond what's directly supported by the research
3. Highlight areas where more data might be needed
4. Connect insights to previous phases while maintaining traceability to source data
5. Help identify potential biases in my research approach or interpretation
6. Suggest frameworks for organizing the provided research data into formal UX artifacts

Your role is to help synthesize genuine user insights rather than generate hypothetical data.
```

### Utility Functions

#### 💾 Quick Capture

```
I want to quickly capture this idea/observation without interrupting my current flow. Please:

1. Save this note: [user input]
2. Tag it with the current phase we're working on
3. Add a timestamp
4. Acknowledge receipt but don't analyze or expand on it yet
```

#### 🧹 Clear Session

```
Please clear our current working context and start fresh. Maintain awareness of the UX framework methodology but discard any specific project details we've been discussing. Confirm when the context has been reset.
```

#### 📤 Export Project

```
Please format all the outputs we've generated in this session into a well-structured document with clear headings for each phase. Include:

1. All problem statements, proto-personas, and objectives
2. All hypothesis statements and feature lists
3. User flow descriptions and key screens
4. Prototype plans and test questions
5. Any synthesis of test results if applicable

Format this in clean markdown suitable for export to notion, obsidian, or other documentation tools.
```

## Phase 0: Fuzzy Front End Prompts

### 💭 Capture Inspiration

```
I'm feeling inspired by this concept: [inspiration source/idea]. 

Please help me explore this direction as a potential product or feature concept. Consider:

1. What problem might this concept address?
2. Who might benefit from a solution in this space?
3. What interesting angles or approaches could be worth exploring?
4. How might this connect to current trends or user needs?

This is an early exploration, so focus on possibility rather than feasibility at this stage.
```

### 🔍 Industry Analysis

```
I'm interested in exploring problems worth solving in the [specific industry] industry.

Please help me identify:

1. 3-5 significant user pain points in this industry that might not be well-addressed
2. Emerging technology trends that could enable new solutions
3. Potential gaps between user expectations and current offerings
4. Interesting angles that might be overlooked by incumbents

Focus on identifying problem spaces rather than specific solutions at this stage.
```

### 🔮 Trend Extrapolation

```
I'm considering how [specific trend] might create new user needs or opportunities in the next 1-2 years.

Please help me explore:

1. How this trend might influence user behaviors or expectations
2. What new problems or needs might emerge as a result
3. What types of users might be most affected by this change
4. What capabilities or approaches might address these emerging needs

Think beyond current implementations to how this trend might evolve and create new opportunity spaces.
```

### 💡 Idea Mashup

```
Help me generate an innovative concept by combining elements from these two different products/services/domains:

1. [Product/Domain A]
2. [Product/Domain B]

Please explore:
- How core elements from each might be combined
- What unique user value might emerge from this combination
- What type of user might benefit from this hybrid approach
- What interesting problem this combination might solve

Feel free to think creatively rather than focusing on immediate feasibility.
```

### 🌱 Problem Space

```
Help me identify 5 potentially underserved problems in the [specific domain] space.

For each problem:
1. Briefly describe the user pain point
2. Suggest what type of user might experience this problem most acutely
3. Note why existing solutions might be insufficient
4. Rate its potential impact (high/medium/low)

Focus on identifying genuine user needs rather than technology or solution gaps.
```

## Phase 1: Define Problem Prompts

### 📝 Problem Statement

```
Based on our exploration so far, please help me craft a precise problem statement that will guide our design process.

Follow this format: "[User type] needs [need] because [insight]"

Requirements:
1. User type should be specific enough to be meaningful but not so narrow that it limits our thinking
2. The need should describe what the user wants to accomplish, not a feature or solution
3. The insight should explain the underlying motivation or pain point
4. The entire statement should be clear and concise (under 30 words)
5. The statement should be solution-agnostic (avoid implying a specific implementation)
6. Focus on emotional journey and processes users experience around the problem
7. Connect to specific user needs and frustrations identified in our exploration

This problem statement will be the foundation for all subsequent design activities, so it needs to capture the core user need accurately while providing a bridge between research insights and actionable design objectives.
```

### 👤 Proto-Persona

```
Based on our problem statement: "[insert problem statement]", please create a lightweight proto-persona that represents our target user.

Focus only on characteristics directly relevant to the identified problem:
1. Key demographics (only those relevant to the problem, not comprehensive)
2. Goals and motivations related to the problem space
3. Pain points and specific frustrations
4. Behaviors and habits that contextualize the need
5. Relevant skills, knowledge, or experience levels
6. A brief quote that captures their perspective on this problem
7. Context of use (when/where they would use similar products)

Remember that effective personas focus on behaviors over demographics unless demographic information is directly relevant to product use. Keep it concise but include specific details that make the persona memorable and distinct.

This is an initial hypothesis of our user, not a comprehensive persona. We'll refine this as we learn more through testing and validation.
```

### 🔍 Problem Analysis

```
For our problem statement: "[insert problem statement]", please help me understand the underlying factors.

Analyze this problem by identifying:
1. What are 3-5 root causes of this problem?
2. When and where does this problem typically occur for users?
3. What makes this problem particularly challenging to solve?
4. What workarounds might users currently employ?
5. What secondary problems might emerge from these workarounds?

This analysis will help us ensure we're addressing the fundamental need rather than just surface symptoms.
```

### 🎯 Problem Scope

```
Let's establish clear boundaries for our problem scope based on our statement: "[insert problem statement]"

Help me define:
1. What specific aspects of this problem we WILL address
2. What related aspects we will explicitly NOT address (at least initially)
3. How we might narrow the focus to ensure we can adequately address it in a prototype
4. What constraints might affect our ability to solve this problem completely

The goal is to define a problem scope that is narrow enough to be addressable in our prototype but significant enough to provide real user value.
```

### ⚖️ Problem Priority

```
For our problem statement: "[insert problem statement]", help me assess its priority from a user perspective.

Please evaluate:
1. Severity: How painful is this problem when users encounter it? (1-5 scale)
2. Frequency: How often do users encounter this problem? (1-5 scale)
3. Reach: What percentage of our target users likely experience this problem?
4. Trend: Is this problem becoming more or less significant over time?
5. Uniqueness: How well is this problem currently addressed by existing solutions?

This assessment will help validate whether this problem is worth solving and how urgently it needs attention.
```

## Phase 2: Objectives & Metrics Prompts

### 🎯 Core Objective

```
Based on our problem statement: "[insert problem statement]" and proto-persona, help me define the primary objective our solution should achieve.

Requirements for the objective:
1. Focus on the outcome for the user, not features or implementation
2. Be specific enough to guide design decisions
3. Be broad enough to allow creative solutions
4. Directly address the core need identified in the problem statement
5. Be realistic given our prototype constraints
6. Include a clear connection to the user's emotional or functional goals
7. Articulate what success looks like from the user's perspective

The objective should transform the user problem into an outcome-focused target that will guide our design decisions. It should define what the user should be able to achieve rather than prescribing how they'll achieve it.

This objective will define success for our design, so it needs to capture what truly matters to the user while establishing clear criteria for evaluating potential solutions.
```

### 📊 Success Metrics

```
For our core objective: "[insert core objective]", please help me define 1-2 specific, measurable metrics that will indicate success.

For each metric:
1. Provide a precise definition of what we'll measure
2. Suggest how we might measure it (method)
3. Define what threshold would indicate success
4. Explain why this metric is a good indicator of achieving our objective
5. Include both quantitative and qualitative measurement approaches
6. Connect the metric directly to user needs identified in our problem statement

Focus on metrics that measure outcomes rather than outputs (e.g., reduction in time to complete tasks rather than number of features implemented). Include baseline measurements where possible for comparison.

These metrics will be used to evaluate our prototype and determine if our solution is effective, so they need to be both measurable and meaningful indicators of user success, not just technical performance.
```

### ⚠️ Constraints

```
Let's identify the key constraints that will shape our solution for addressing: "[insert problem statement]"

Please help me identify constraints across these categories:
1. Technical: What capabilities or technologies must we work within?
2. Business: What business requirements or limitations apply?
3. User: What user expectations or limitations must we account for?
4. Resources: What time, budget, or team constraints will affect our prototype?
5. Ethical: What ethical considerations should guide our approach?

Understanding these constraints will help us design a solution that is not only desirable but also viable and feasible.
```

### 🔍 Metric Validation

```
For our success metrics: "[insert metrics]", help me plan how we'll measure these in a prototype test.

For each metric, please suggest:
1. What specific data we should collect during testing
2. How we might structure the test to gather this data
3. What baseline we should use for comparison
4. Potential challenges in accurately measuring this metric
5. How we might address those challenges

This will help ensure our metrics are practically measurable during prototype testing.
```

## Phase 3: Solution Hypothesis Prompts

### 💡 Core Concept

```
Based on our problem statement: "[insert problem statement]" and core objective: "[insert objective]", please generate a solution concept using design thinking principles.

Requirements:
1. The concept should directly address the user need identified in our problem statement
2. It should have a clear path to achieving our core objective
3. It should account for the constraints we've identified
4. It should be feasible to prototype relatively quickly
5. It should focus on the core user value, not peripheral features
6. Consider multiple approaches before settling on a recommended concept
7. Explain how the concept transforms the problem into an opportunity

Describe the concept in 2-3 paragraphs, focusing on the user experience rather than technical implementation. Consider both the functional solution and the emotional experience it creates for users.

Remember that this is a hypothesis to test, not a final solution. The goal is to create something concrete enough to prototype and validate with users.
```

### 📝 Hypothesis

```
Based on our solution concept, please formulate a testable hypothesis statement.

Use this format: "We believe that [solution/approach] will result in [outcome] for [user type], which we can measure by [metrics from Phase 2]."

Requirements:
1. Be specific about the solution approach without prescribing exact implementation
2. Clearly connect to our defined user need from the problem statement
3. Specify an outcome that directly addresses our core objective
4. Include our defined success metrics as measurement criteria
5. Be structured in a way that can be clearly validated or invalidated through testing
6. Focus on a single primary outcome rather than multiple goals
7. Frame it as an experiment rather than an assertion

The hypothesis should transform your solution concept into a structured prediction that can be tested. It connects your problem statement, user needs, solution concept, and success metrics into a cohesive statement that guides your prototype development.

This hypothesis will be the centerpiece of your experimental approach, defining exactly what you're testing and how you'll know if it works.
```

### 🧩 Key Features

```
For our solution concept and hypothesis: "[insert hypothesis]", please identify the 2-3 essential features needed to test this hypothesis.

For each feature:
1. Provide a brief description of functionality
2. Explain how it directly contributes to testing our hypothesis
3. Note why it's considered essential (vs. nice-to-have)
4. Describe the key user interaction(s) involved
5. Indicate any particular challenges in implementing it

Focus only on the minimum features needed to test our core hypothesis. We can expand later if the initial concept proves successful.
```

### ⚠️ Risk Assessment

```
For our solution hypothesis: "[insert hypothesis]", please help me identify and assess the key risks.

Please identify:
1. What are the top 3 risks that might cause our solution to fail?
2. For each risk, how likely is it to occur? (High/Medium/Low)
3. For each risk, how severe would the impact be? (High/Medium/Low)
4. What early indicators might suggest these risks are manifesting?
5. What mitigation strategies could we employ for each risk?

This assessment will help us focus our testing on the most critical assumptions and prepare contingency plans.
```

## Phase 4: User Flow Prompts

### 🔄 Happy Path

```
Based on our solution concept and key features, please map the primary user flow from start to goal completion.

Requirements:
1. Start with the user's entry point into the experience
2. Include each significant step the user takes
3. Note the user's goal or intention at each step
4. End with successful completion of the core task
5. Focus only on the "happy path" where everything goes as expected
6. Format as a numbered sequence for clarity
7. Identify the actions, screens, and decisions (using standard flow notation)
8. Keep the flow focused on the specific user goal identified in our problem statement

The flow should map the quickest and easiest path to goal completion, making sure each step logically leads to the next. This establishes the backbone for our prototype design.

Remember that user flows should map the user's perspective and mental model, not your technical or organizational structure. Focus on what the user is trying to accomplish at each stage.
```

### 🧩 Key Screens

```
Based on our user flow: "[insert flow summary]", please identify the essential screens or states needed in this flow.

For each screen/state:
1. Provide a descriptive name
2. Briefly describe its primary purpose
3. Note what key information should be displayed
4. Identify the primary user actions available
5. Explain how it connects to other screens in the flow

Focus only on screens that are essential to the core user journey we're testing. We can add refinements later.
```

### 🔀 Decision Points

```
Within our user flow, please identify the key decision points where users will need to make choices.

For each decision point:
1. What choice is the user making?
2. What information do they need to make this decision?
3. What are the possible paths they might take?
4. Which path is considered the "happy path"?
5. How might we guide users toward the optimal decision?

Understanding these decision points will help us design a flow that supports user decision-making and reduces cognitive load.
```

### ⚠️ Error Handling

```
For our user flow, let's identify potential critical errors and how to handle them.

Please consider:
1. What are 2-3 critical errors that might occur during the primary user flow?
2. For each error, at what point in the flow might it occur?
3. How should we communicate this error to the user?
4. What recovery path should we provide?
5. How can we help prevent this error in the first place?

Focus only on critical errors that would prevent the user from completing their task, not minor edge cases.
```

## Phase 5: Prototype Plan Prompts

### 📋 Prototype Scope

```
Based on our user flow and key screens, let's define the scope for our initial prototype.

Please help me determine:
1. Which specific screens from our flow should be included in the prototype?
2. Which user interactions need to be functional?
3. Which aspects can be simulated or "smoke and mirrors"?
4. What content needs to be realistic vs. placeholder?
5. Where should we set the boundaries of the prototype experience?
6. What minimum level of fidelity is required to test our hypothesis?
7. Which parts of the flow are most critical for testing our assumptions?

Consider both what to include and what to intentionally exclude at this stage. The prototype should be a focused tool for testing specific hypotheses, not a comprehensive implementation.

The goal is to define a prototype scope that is focused enough to build quickly but sufficient to test our core hypothesis. We want to learn the most important things with the minimum necessary investment of time and resources.
```

### 🔍 Fidelity Decision

```
Help me determine the appropriate fidelity level for our prototype based on our testing goals.

Please consider:
1. What level of visual fidelity is necessary to test our hypothesis?
2. What level of interaction fidelity is necessary?
3. What level of content fidelity is necessary?
4. How might different fidelity choices affect our test results?
5. What's the minimum fidelity needed to get valid feedback?
6. Which aspects would benefit from higher fidelity and which can remain lower?
7. How does our fidelity choice align with our specific testing questions?

For each decision, consider the trade-off between investment (time/resources) and learning value. Higher fidelity isn't always better - it depends entirely on what you're trying to learn.

Recommend a specific fidelity approach (low/mid/high) for each aspect (visual, interaction, content) with justification based on our specific testing needs. Consider a hybrid approach where critical components have higher fidelity while less important elements remain simpler.
```

### 🖱️ Key Interactions

```
For our prototype, please identify the specific interactions that need to be functional.

For each key interaction:
1. Describe the user action (e.g., "tap button", "swipe list")
2. Note the expected system response
3. Explain why this interaction is critical to test
4. Suggest how complex it might be to implement
5. Note any specific details needed for the interaction to feel realistic

Focus on interactions that are essential to testing our hypothesis rather than trying to make everything functional.
```

### 📝 Test Questions

```
Based on our hypothesis statement: "[insert hypothesis]", please help me formulate specific questions our prototype test should answer.

Requirements:
1. Each question should connect directly to an aspect of our hypothesis
2. Questions should be specific and answerable through observation or user feedback
3. Include 2-3 primary questions focused on validating/invalidating our core hypothesis
4. Include 1-2 secondary questions about usability or implementation details
5. Frame questions neutrally to avoid biasing our testing

These questions will guide our test plan and help us evaluate whether our prototype successfully addresses our core hypothesis.
```

## Phase 6: Post-Test Synthesis Prompts

### 📊 Test Results

```
I've completed prototype testing and have these observations:

[User should paste test observations here]

Please help me organize these observations into patterns and insights by:
1. Identifying recurring themes across different test participants
2. Noting significant points of friction or confusion
3. Highlighting areas where users succeeded easily
4. Distinguishing between usability issues and concept limitations
5. Summarizing both positive and negative feedback
6. Separating observed behavior from user statements
7. Connecting insights to our original hypothesis and success metrics
8. Identifying surprising or unexpected user reactions

Focus on what actually happened during testing rather than interpretations. Note both verbal feedback and non-verbal cues like hesitation, confusion, or delight.

This synthesis will help us understand what we've learned from our testing and provide a foundation for making evidence-based decisions about our next steps.
```

### ✅ Hypothesis Check

```
Based on our test results, let's evaluate our hypothesis: "[insert hypothesis]"

Please assess:
1. Was our hypothesis validated, invalidated, or are the results inconclusive?
2. What specific evidence supports this assessment?
3. Were there any unexpected findings that challenge our assumptions?
4. How did we perform against our success metrics?
5. What level of confidence should we have in these conclusions?
6. What variables or conditions might have influenced our results?
7. What limitations should we acknowledge in our testing approach?
8. How do these results connect back to our original problem statement?

Be careful not to overinterpret limited data. Recognize the difference between statistical significance and practical significance in your assessment.

This evaluation will help us determine our next steps - whether to proceed with the current direction, pivot, or gather more data. It's important to be honest about what we've learned and what remains uncertain.
```

### 🔄 Iteration Plan

```
Based on our test results and hypothesis evaluation, please help me plan the next iteration of our prototype.

Please suggest:
1. What aspects of the concept should remain the same?
2. What specific changes should we make to address issues identified?
3. How should we prioritize these changes?
4. Should we narrow or expand our prototype scope?
5. What new questions might we want to explore in the next round of testing?

This plan will guide our next iteration and help us continue refining our solution based on user feedback.
```

### 🔀 Pivot Options

```
Based on our test results suggesting our hypothesis wasn't validated, please help me identify potential pivot directions.

Please suggest:
1. 2-3 alternative approaches to addressing our original problem statement
2. How each approach differs from our current solution
3. The potential advantages of each alternative
4. What new assumptions each alternative would be based on
5. How we might quickly test these alternatives

These pivot options will help us explore new directions if our current approach isn't yielding the desired results.
```