#!/usr/bin/env node
/**
 * Second migration pass: files not covered by prompts.json indices.
 * Handles NFRs, tool selection, bridge, implementation, and stubs.
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const ROOT = new URL('..', import.meta.url).pathname;
const BASE = join(ROOT, 'prompts/dev/01_product_dev/01_pre_dev');

// Files to skip (non-prompts, will be relocated in cleanup)
const SKIP_FILES = [
  '01_ux_research/ux_framework_prompts.md',
  'mcp_idea.md',
  '03_tool_selection_setup/01_project_environment.md', // duplicate parent
];

// File definitions for everything not covered by prompts.json
const REMAINING = [
  // Phase 01 stubs (empty files - need content from Stream Deck doc)
  { path: '01_ux_research/01_define_problem/06_user_validation_questions.md', id: 'uxr.01_define_problem.user_validation_questions', slug: 'user-validation-questions', title: 'User Validation Questions', phase: 'discovery', category: 'Problem Definition', folder: '01_define_problem', tags: ['problem'], tier: 3, requires: ['problem_statement', 'proto_persona'], produces: ['validation_questions'], purpose: 'Generate questions to validate problem with real users', context: 'Use when preparing for user interviews or validation sessions', body: 'Based on our problem statement and proto-persona, help me create a set of questions to validate our assumptions with real users.\n\nPlease generate:\n1. 5-7 open-ended questions that test our core problem assumptions\n2. 2-3 questions that explore the user\'s current workarounds\n3. 2-3 questions that gauge severity and frequency of the problem\n4. 1-2 questions about willingness to adopt a new solution\n\nEnsure questions are neutral and don\'t lead the user toward confirming our assumptions.' },
  { path: '01_ux_research/01_define_problem/07_refine_problem.md', id: 'uxr.01_define_problem.refine_problem', slug: 'refine-problem', title: 'Refine Problem Statement', phase: 'discovery', category: 'Problem Definition', folder: '01_define_problem', tags: ['problem'], tier: 3, requires: ['problem_statement', 'problem_analysis'], produces: ['refined_problem_statement'], purpose: 'Refine the problem statement based on deeper analysis', context: 'Use after problem analysis to sharpen the statement', body: 'Based on our problem analysis, let\'s refine our original problem statement: "[insert problem statement]"\n\nConsider:\n1. Does the analysis suggest we should narrow or broaden our focus?\n2. Are there root causes we should address instead of symptoms?\n3. Should the user type be more specific based on what we\'ve learned?\n4. Does the insight still capture the core motivation?\n\nProvide a refined problem statement and explain what changed and why.' },
  { path: '01_ux_research/01_define_problem/08_problem_priority.md', id: 'uxr.01_define_problem.problem_priority', slug: 'problem-priority', title: 'Problem Priority Assessment', phase: 'discovery', category: 'Problem Definition', folder: '01_define_problem', tags: ['problem'], tier: 3, requires: ['problem_qualification'], produces: ['priority_assessment'], purpose: 'Assess problem priority and urgency for resource allocation', context: 'Use after qualifying the problem to determine investment level', body: 'Based on our problem qualification results, help me create a priority assessment.\n\nPlease evaluate:\n1. Where does this problem fall on a severity x frequency matrix?\n2. What is the estimated market size or user reach?\n3. How does this compare to alternative problems we could solve?\n4. What is the urgency - is this problem getting worse over time?\n5. What is the strategic fit with our capabilities and goals?\n\nRecommend a priority level (Critical / High / Medium / Low) with clear rationale.' },

  // Phase 04 stubs
  { path: '01_ux_research/04_user_flow/05_user_entry_exit_points.md', id: 'uxr.04_user_flow.entry_exit_points', slug: 'user-entry-exit-points', title: 'User Entry & Exit Points', phase: 'discovery', category: 'User Flow & Interaction', folder: '04_user_flow', tags: ['user_flow'], tier: 3, requires: ['user_flow'], produces: ['entry_exit_analysis'], purpose: 'Map where users enter and leave the experience', context: 'Use to understand user context before and after using the product', body: 'For our user flow, let\'s identify all entry and exit points.\n\nPlease map:\n1. Where do users come from before entering our experience? (referrals, search, direct)\n2. What is their mental state and expectation at each entry point?\n3. Where do users go after completing their task?\n4. What are the natural exit points (both successful and abandoned)?\n5. How might we design smooth transitions at each boundary?\n\nThis helps us design for the full user context, not just the in-app experience.' },
  { path: '01_ux_research/04_user_flow/06_validate_flow.md', id: 'uxr.04_user_flow.validate_flow', slug: 'validate-flow', title: 'Validate User Flow', phase: 'discovery', category: 'User Flow & Interaction', folder: '04_user_flow', tags: ['user_flow'], tier: 3, requires: ['user_flow', 'screen_inventory'], produces: ['flow_validation'], purpose: 'Validate the user flow against objectives and constraints', context: 'Use as a quality check before prototyping', body: 'Let\'s validate our user flow against our objectives and constraints.\n\nPlease check:\n1. Does every step contribute to the user achieving their goal?\n2. Are there any unnecessary steps that could be removed?\n3. Does the flow account for our identified constraints?\n4. Is the cognitive load reasonable at each step?\n5. Are there accessibility concerns with any step?\n6. Does this flow align with our core objective?\n\nIdentify any issues and suggest improvements.' },
  { path: '01_ux_research/04_user_flow/07_create_flow_diagram.md', id: 'uxr.04_user_flow.create_flow_diagram', slug: 'create-flow-diagram', title: 'Create Flow Diagram', phase: 'discovery', category: 'User Flow & Interaction', folder: '04_user_flow', tags: ['user_flow'], tier: 3, requires: ['user_flow', 'decision_points'], produces: ['flow_diagram'], purpose: 'Generate a structured flow diagram from the user flow', context: 'Use to create a visual representation of the flow', body: 'Based on our complete user flow including decision points and error paths, please create a structured flow diagram.\n\nUse this notation:\n- [Rectangle] for screens/states\n- <Diamond> for decision points\n- (Rounded) for start/end\n- --> for flow direction\n- [!] for error states\n\nInclude the happy path, key decision branches, and error recovery paths. Format as a text-based diagram that can be translated to a visual tool.' },

  // Phase 05 stubs
  { path: '01_ux_research/05_prototype/05_test_participant_goals.md', id: 'uxr.05_prototype.test_participant_goals', slug: 'test-participant-goals', title: 'Test Participant Goals', phase: 'discovery', category: 'Prototype Planning & Testing', folder: '05_prototype', tags: ['mvp_feature'], tier: 3, requires: ['test_questions'], produces: ['participant_goals'], purpose: 'Define what each test participant should try to accomplish', context: 'Use when designing specific tasks for test participants', body: 'For our prototype test, let\'s define specific goals for test participants.\n\nFor each test task:\n1. What should the participant try to accomplish?\n2. What context should we provide without biasing them?\n3. What does successful completion look like?\n4. What should we observe during this task?\n5. What follow-up questions should we ask?\n\nDesign 3-4 tasks that map directly to our test questions and hypothesis.' },
  { path: '01_ux_research/05_prototype/06_test_script.md', id: 'uxr.05_prototype.test_script_outline', slug: 'test-script-outline', title: 'Test Script Outline', phase: 'discovery', category: 'Prototype Planning & Testing', folder: '05_prototype', tags: ['mvp_feature'], tier: 3, requires: ['test_questions'], produces: ['test_script_outline'], purpose: 'Create an outline for the test script', context: 'Use as a quick alternative to the full test script', body: 'Create a brief test script outline covering:\n1. Introduction (2 min) - welcome, context setting\n2. Background questions (3 min) - relevant user context\n3. Tasks (15 min) - 3-4 specific tasks to attempt\n4. Debrief (5 min) - overall impressions, hypothesis-specific questions\n\nKeep it concise - this is a planning outline, not the final script.' },
  { path: '01_ux_research/05_prototype/07_tool_selection.md', id: 'uxr.05_prototype.prototype_tool_selection', slug: 'prototype-tool-selection', title: 'Prototype Tool Selection', phase: 'discovery', category: 'Prototype Planning & Testing', folder: '05_prototype', tags: ['mvp_feature'], tier: 3, requires: ['prototype_scope', 'fidelity_decision'], produces: ['prototype_tool_choice'], purpose: 'Select appropriate prototyping tools', context: 'Use when deciding how to build the prototype', body: 'Based on our prototype scope and fidelity decisions, help me select the right prototyping tool.\n\nConsider:\n1. Required fidelity level (low/mid/high for visual, interaction, content)\n2. Key interactions that need to be functional\n3. Team skills and tool familiarity\n4. Time available for prototype development\n5. Testing requirements (remote vs. in-person, recording needs)\n\nRecommend 1-2 tools with rationale and note any trade-offs.' },

  // Phase 06 stubs
  { path: '01_ux_research/06_post_test_synthesis/05_refine_problem_statement.md', id: 'uxr.06_post_test_synthesis.refine_problem_statement', slug: 'post-test-refine-problem', title: 'Refine Problem Statement Post-Test', phase: 'discovery', category: 'Post-Test Analysis', folder: '06_post_test_synthesis', tags: ['mvp_feature'], tier: 3, requires: ['hypothesis_evaluation', 'problem_statement'], produces: ['updated_problem_statement'], purpose: 'Refine problem statement based on test learnings', context: 'Use when test results suggest the problem needs reframing', body: 'Based on our test results and hypothesis evaluation, let\'s revisit our problem statement: "[insert problem statement]"\n\nConsider:\n1. Did testing reveal aspects of the problem we didn\'t anticipate?\n2. Should we narrow or broaden the problem scope?\n3. Did users describe the problem differently than we framed it?\n4. Are there adjacent problems that emerged as more important?\n\nProvide an updated problem statement with clear rationale for changes.' },
  { path: '01_ux_research/06_post_test_synthesis/06_progress_report.md', id: 'uxr.06_post_test_synthesis.progress_report', slug: 'progress-report', title: 'Progress Report', phase: 'discovery', category: 'Post-Test Analysis', folder: '06_post_test_synthesis', tags: ['mvp_feature'], tier: 3, requires: ['hypothesis_evaluation'], produces: ['progress_report'], purpose: 'Generate a structured progress report for stakeholders', context: 'Use to communicate findings to team or stakeholders', body: 'Help me create a progress report summarizing our work so far.\n\nInclude:\n1. Problem statement and who it affects\n2. Our hypothesis and how we tested it\n3. Key findings (what worked, what didn\'t, surprises)\n4. Current confidence level and evidence\n5. Recommended next steps\n6. Open questions and risks\n\nFormat for a non-technical audience. Keep it under 1 page.' },
  { path: '01_ux_research/06_post_test_synthesis/07_future_roadmap.md', id: 'uxr.06_post_test_synthesis.future_roadmap', slug: 'future-roadmap', title: 'Future Roadmap', phase: 'discovery', category: 'Post-Test Analysis', folder: '06_post_test_synthesis', tags: ['mvp_feature'], tier: 3, requires: ['iteration_plan'], produces: ['future_roadmap'], purpose: 'Define a forward-looking roadmap based on validated learnings', context: 'Use after completing a test cycle to plan ahead', body: 'Based on everything we\'ve learned, help me outline a forward-looking roadmap.\n\nPlease define:\n1. Immediate next steps (next 1-2 weeks)\n2. Short-term goals (next 1-3 months)\n3. Medium-term vision (3-6 months)\n4. Key milestones and decision points\n5. Assumptions that need continued validation\n6. Resources or capabilities we\'ll need\n\nThis roadmap should be grounded in what we\'ve validated, not speculation.' },

  // NFR files (have content, no frontmatter, no JSON index)
  { path: '02_tech_requirements/04_non_functional_requirements/01_performance_requirements.md', id: 'tech.04_nfr.performance_requirements', slug: 'performance-requirements', title: 'Performance Requirements', phase: 'spec', category: 'Non-Functional Requirements', folder: '04_non_functional_requirements', tags: ['nfr'], tier: 2, requires: ['solution_concept', 'user_flow'], produces: ['performance_requirements'], purpose: 'Define performance targets and constraints', context: 'Use when specifying how fast and responsive the system must be' },
  { path: '02_tech_requirements/04_non_functional_requirements/02_security_requirements.md', id: 'tech.04_nfr.security_requirements', slug: 'security-requirements', title: 'Security Requirements', phase: 'spec', category: 'Non-Functional Requirements', folder: '04_non_functional_requirements', tags: ['nfr'], tier: 2, requires: ['data_models', 'api_contracts'], produces: ['security_requirements'], purpose: 'Define security requirements and threat model', context: 'Use when specifying authentication, authorization, and data protection needs' },
  { path: '02_tech_requirements/04_non_functional_requirements/03_accessibility_requirements.md', id: 'tech.04_nfr.accessibility_requirements', slug: 'accessibility-requirements', title: 'Accessibility Requirements', phase: 'spec', category: 'Non-Functional Requirements', folder: '04_non_functional_requirements', tags: ['nfr'], tier: 2, requires: ['user_flow', 'screen_inventory'], produces: ['accessibility_requirements'], purpose: 'Define accessibility standards and requirements', context: 'Use to ensure the product meets WCAG and inclusive design standards' },
  { path: '02_tech_requirements/04_non_functional_requirements/04_localization_requirements.md', id: 'tech.04_nfr.localization_requirements', slug: 'localization-requirements', title: 'Localization Requirements', phase: 'spec', category: 'Non-Functional Requirements', folder: '04_non_functional_requirements', tags: ['nfr'], tier: 3, requires: ['solution_concept'], produces: ['localization_requirements'], purpose: 'Define internationalization and localization needs', context: 'Use when the product will serve multiple locales or languages' },
  { path: '02_tech_requirements/04_non_functional_requirements/05_device_browser_compatibility.md', id: 'tech.04_nfr.device_browser_compatibility', slug: 'device-browser-compatibility', title: 'Device & Browser Compatibility', phase: 'spec', category: 'Non-Functional Requirements', folder: '04_non_functional_requirements', tags: ['nfr'], tier: 3, requires: ['platform_strategy'], produces: ['compatibility_requirements'], purpose: 'Define device and browser support requirements', context: 'Use when specifying cross-platform compatibility targets' },

  // Tool Selection files
  { path: '03_tool_selection_setup/01_assess_project_environment/01_assess_project_tools.md', id: 'setup.01_assess.project_tools', slug: 'assess-project-tools', title: 'Assess Project Tools', phase: 'design', category: 'Tool Selection & Setup', folder: '01_assess_project_environment', tags: ['setup'], tier: 2, requires: ['solution_concept'], produces: ['tool_assessment'], purpose: 'Evaluate current and needed development tools', context: 'Use when setting up a new project environment' },
  { path: '03_tool_selection_setup/01_assess_project_environment/02_strategize_tool_integration.md', id: 'setup.01_assess.tool_integration', slug: 'strategize-tool-integration', title: 'Strategize Tool Integration', phase: 'design', category: 'Tool Selection & Setup', folder: '01_assess_project_environment', tags: ['setup'], tier: 2, requires: ['tool_assessment'], produces: ['integration_strategy'], purpose: 'Plan how tools will work together', context: 'Use after assessing tools to plan integration approach' },
  { path: '03_tool_selection_setup/01_assess_project_environment/03_evaluate_tech_stack.md', id: 'setup.01_assess.tech_stack', slug: 'evaluate-tech-stack', title: 'Evaluate Tech Stack', phase: 'design', category: 'Tool Selection & Setup', folder: '01_assess_project_environment', tags: ['setup'], tier: 2, requires: ['solution_concept', 'data_models'], produces: ['tech_stack_evaluation'], purpose: 'Evaluate and select technology stack', context: 'Use when choosing languages, frameworks, and infrastructure' },
  { path: '03_tool_selection_setup/02_environment_setup_config/01_setup_prompt_lib.md', id: 'setup.02_env.setup_prompt_lib', slug: 'setup-prompt-library', title: 'Setup Prompt Library', phase: 'design', category: 'Environment Setup', folder: '02_environment_setup_config', tags: ['setup'], tier: 3, requires: [], produces: ['prompt_lib_setup'], purpose: 'Configure the prompt library for the project', context: 'Use when initializing the framework for a new project' },
  { path: '03_tool_selection_setup/02_environment_setup_config/02_config_dev_env.md', id: 'setup.02_env.config_dev_env', slug: 'configure-dev-environment', title: 'Configure Development Environment', phase: 'design', category: 'Environment Setup', folder: '02_environment_setup_config', tags: ['setup'], tier: 2, requires: ['tech_stack_evaluation'], produces: ['dev_env_config'], purpose: 'Set up the development environment', context: 'Use when configuring IDE, linting, testing, and CI' },
  { path: '03_tool_selection_setup/02_environment_setup_config/03_define_project_structure.md', id: 'setup.02_env.project_structure', slug: 'define-project-structure', title: 'Define Project Structure', phase: 'design', category: 'Environment Setup', folder: '02_environment_setup_config', tags: ['setup'], tier: 2, requires: ['tech_stack_evaluation'], produces: ['project_structure'], purpose: 'Define directory structure and file organization', context: 'Use when scaffolding a new project' },
  { path: '03_tool_selection_setup/02_environment_setup_config/04_setup_security_quality_standards.md', id: 'setup.02_env.security_quality', slug: 'setup-security-quality', title: 'Setup Security & Quality Standards', phase: 'design', category: 'Environment Setup', folder: '02_environment_setup_config', tags: ['setup'], tier: 3, requires: ['security_requirements'], produces: ['security_quality_setup'], purpose: 'Configure security and quality tooling', context: 'Use when setting up linting, SAST, and quality gates', body: 'Help me set up security and code quality standards for our project.\n\nPlease recommend:\n1. Static analysis tools appropriate for our tech stack\n2. Security scanning configuration (SAST, dependency auditing)\n3. Code quality rules and linting configuration\n4. Pre-commit hooks for automated checks\n5. CI/CD quality gates\n\nFocus on practical, automatable standards that catch issues early.' },
  { path: '03_tool_selection_setup/03_team_collaboration_setup/01_define_team_wf.md', id: 'setup.03_collab.team_workflow', slug: 'define-team-workflow', title: 'Define Team Workflow', phase: 'design', category: 'Team Collaboration', folder: '03_team_collaboration_setup', tags: ['setup'], tier: 2, requires: ['tech_stack_evaluation'], produces: ['team_workflow'], purpose: 'Define team development workflow and processes', context: 'Use when establishing how the team will work together' },
  { path: '03_tool_selection_setup/03_team_collaboration_setup/02_documentation_standards.md', id: 'setup.03_collab.doc_standards', slug: 'documentation-standards', title: 'Documentation Standards', phase: 'design', category: 'Team Collaboration', folder: '03_team_collaboration_setup', tags: ['setup'], tier: 3, requires: ['project_structure'], produces: ['documentation_standards'], purpose: 'Define documentation conventions and standards', context: 'Use when establishing how the team documents code and decisions', body: 'Help me define documentation standards for our project.\n\nPlease recommend:\n1. Code documentation approach (inline comments, JSDoc/TSDoc, etc.)\n2. API documentation format and tools\n3. Architecture decision records (ADR) process\n4. README structure and requirements\n5. Change log management\n\nKeep standards practical and enforceable.' },
  { path: '03_tool_selection_setup/03_team_collaboration_setup/03_strategize_version_control.md', id: 'setup.03_collab.version_control', slug: 'strategize-version-control', title: 'Strategize Version Control', phase: 'design', category: 'Team Collaboration', folder: '03_team_collaboration_setup', tags: ['setup'], tier: 2, requires: ['team_workflow'], produces: ['version_control_strategy'], purpose: 'Define branching strategy and version control practices', context: 'Use when setting up Git workflow for the team' },

  // Bridge to Architecture
  { path: '04_bridge_to_architecture/analytics_strategy.md', id: 'bridge.analytics_strategy', slug: 'analytics-strategy', title: 'Analytics Strategy', phase: 'design', category: 'Bridge to Architecture', folder: '04_bridge_to_architecture', tags: ['architecture'], tier: 2, requires: ['success_metrics', 'user_flow'], produces: ['analytics_strategy'], purpose: 'Define analytics implementation strategy', context: 'Use when planning how to measure product usage and success' },
  { path: '04_bridge_to_architecture/ai_integration_strategy.md', id: 'bridge.ai_integration_strategy', slug: 'ai-integration-strategy', title: 'AI Integration Strategy', phase: 'design', category: 'Bridge to Architecture', folder: '04_bridge_to_architecture', tags: ['architecture'], tier: 3, requires: ['solution_concept'], produces: ['ai_integration_strategy'], purpose: 'Plan AI/ML integration approach', context: 'Use when the product includes AI-powered features' },
  { path: '04_bridge_to_architecture/api_first_planning.md', id: 'bridge.api_first_planning', slug: 'api-first-planning', title: 'API-First Planning', phase: 'design', category: 'Bridge to Architecture', folder: '04_bridge_to_architecture', tags: ['architecture'], tier: 2, requires: ['api_contracts', 'data_models'], produces: ['api_first_plan'], purpose: 'Plan API-first development approach', context: 'Use when designing the system as API-first' },
  { path: '04_bridge_to_architecture/security_by_design.md', id: 'bridge.security_by_design', slug: 'security-by-design', title: 'Security by Design', phase: 'design', category: 'Bridge to Architecture', folder: '04_bridge_to_architecture', tags: ['architecture'], tier: 2, requires: ['security_requirements', 'data_models'], produces: ['security_design'], purpose: 'Embed security into the architecture from the start', context: 'Use when designing system architecture with security as a first-class concern' },

  // Implementation Docs
  { path: '05_implementation_docs/tech_complexity.md', id: 'impl.tech_complexity', slug: 'tech-complexity-assessment', title: 'Technical Complexity Assessment', phase: 'dev', category: 'Implementation', folder: '05_implementation_docs', tags: ['implementation'], tier: 2, requires: ['data_models', 'api_contracts', 'business_rules'], produces: ['complexity_assessment'], purpose: 'Assess technical complexity and identify high-risk areas', context: 'Use before starting development to prioritize effort' },
  { path: '05_implementation_docs/tech_selection.md', id: 'impl.tech_selection', slug: 'tech-selection-rationale', title: 'Technology Selection Rationale', phase: 'dev', category: 'Implementation', folder: '05_implementation_docs', tags: ['implementation'], tier: 2, requires: ['tech_stack_evaluation', 'solution_concept'], produces: ['tech_selection_rationale'], purpose: 'Document technology selection decisions with rationale', context: 'Use when finalizing technology choices for implementation' },
];

function generateFrontmatter(def) {
  const operation = def.slug.replace(/-/g, '_');
  return `---
metadata:
  id: "${def.id}"
  slug: "${def.slug}"
  title: "${def.title}"
  version: "0.1.0"
  status: "active"
  phase: "${def.phase}"
  category: "${def.category}"
  type: "instruction"
  folder: "${def.folder}"
  tags: ${JSON.stringify(def.tags)}
  purpose: "${def.purpose}"
  context: "${def.context}"
  tier: ${def.tier}
dependencies:
  requires: ${JSON.stringify(def.requires)}
  produces: ${JSON.stringify(def.produces)}
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "${def.produces[0] || operation}"
modes:
  simulation: true
  synthesis: true
validation:
  gate: ""
  criteria: []
mcp:
  exposed: true
  operation: "${operation}"
---`;
}

let stats = { created: 0, updated: 0, skipped: 0, errors: 0 };

for (const def of REMAINING) {
  const filePath = join(BASE, def.path);

  if (!existsSync(filePath)) {
    console.log(`  WARN: ${def.path} not found`);
    stats.errors++;
    continue;
  }

  const content = readFileSync(filePath, 'utf-8').trim();
  const frontmatter = generateFrontmatter(def);

  // Check if already has complete frontmatter
  if (content.startsWith('---') && content.includes('tier:') && content.includes('artifact_name:')) {
    console.log(`  SKIP: ${def.path} (already complete)`);
    stats.skipped++;
    continue;
  }

  if (content.length === 0 && def.body) {
    // Empty file with body provided in definition
    writeFileSync(filePath, `${frontmatter}\n${def.body}\n`);
    console.log(`  CREATE: ${def.path} (wrote frontmatter + body)`);
    stats.created++;
  } else if (content.length === 0) {
    // Empty file, no body provided - write frontmatter only as stub
    writeFileSync(filePath, `${frontmatter}\n`);
    console.log(`  STUB: ${def.path} (frontmatter only, needs content)`);
    stats.created++;
  } else if (content.startsWith('---')) {
    // Has incomplete frontmatter - replace
    const endIdx = content.indexOf('---', 3);
    if (endIdx > 0) {
      const body = content.substring(endIdx + 3).trim();
      writeFileSync(filePath, `${frontmatter}\n${body}\n`);
      console.log(`  UPDATE: ${def.path} (replaced frontmatter)`);
      stats.updated++;
    }
  } else {
    // Has content but no frontmatter - prepend
    writeFileSync(filePath, `${frontmatter}\n${content}\n`);
    console.log(`  CREATE: ${def.path} (prepended frontmatter)`);
    stats.created++;
  }
}

console.log(`\n=== Remaining Migration Summary ===`);
console.log(`Created: ${stats.created}`);
console.log(`Updated: ${stats.updated}`);
console.log(`Skipped: ${stats.skipped}`);
console.log(`Errors:  ${stats.errors}`);
