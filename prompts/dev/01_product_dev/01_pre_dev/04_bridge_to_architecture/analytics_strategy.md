---
name: analytics-strategy
description: >
  Define analytics implementation strategy.
  Use when planning how to measure product usage and success.
run: always
produces: analytics_strategy
requires: [success_metrics, user_flow]
tier: 2
---
For our solution: {{solution_concept}} with core metrics: {{success_metrics}}, let's develop a comprehensive analytics strategy.

Please help me define:

1. Key events to track:
   - User actions and interactions
   - System events and state changes
   - Error conditions
   - Performance metrics
   - Business metrics

2. For each critical event:
   - Specific definition and trigger conditions
   - Properties/parameters to capture
   - Connection to product goals and hypotheses
   - Implementation considerations

3. User property/dimension strategy:
   - What user characteristics should we capture?
   - What segmentation dimensions are important?
   - What session/context data is relevant?

4. Implementation approach:
   - Recommended analytics tool/platform
   - Integration strategy (client vs. server-side)
   - Data layer requirements
   - Privacy and consent considerations

5. Reporting framework:
   - Key dashboards needed
   - Critical metrics for ongoing monitoring
   - Alert thresholds

This analytics strategy will ensure we collect the right data to measure success and inform future iterations.
