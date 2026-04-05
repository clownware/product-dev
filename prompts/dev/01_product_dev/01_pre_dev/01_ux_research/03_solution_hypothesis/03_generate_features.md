---
name: generate-features
description: >
  Identify essential features needed to test the hypothesis.
  Use after formulating hypothesis to define minimum feature set for testing.
run: always
produces: feature_list
requires: [hypothesis_statement]
tier: 2
---

For our solution concept and hypothesis: {{hypothesis_statement}}, please identify the 2-3 essential features needed to test this hypothesis.

For each feature:
1. Provide a brief description of functionality
2. Explain how it directly contributes to testing our hypothesis
3. Note why it's considered essential (vs. nice-to-have)
4. Describe the key user interaction(s) involved
5. Indicate any particular challenges in implementing it

Focus only on the minimum features needed to test our core hypothesis. We can expand later if the initial concept proves successful.