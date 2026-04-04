#!/usr/bin/env node
/**
 * Frontmatter Migration Script
 *
 * Reads prompts.json indices and ensures every prompt file has
 * ADR 0001-compliant frontmatter. Handles:
 * - Empty files (writes frontmatter + body from JSON)
 * - Files with content but no frontmatter (prepends frontmatter)
 * - Skips files that already have complete frontmatter
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';

const ROOT = new URL('..', import.meta.url).pathname;
const UX_BASE = join(ROOT, 'prompts/dev/01_product_dev/01_pre_dev/01_ux_research');
const TECH_BASE = join(ROOT, 'prompts/dev/01_product_dev/01_pre_dev/02_tech_requirements');

// Phase configuration with metadata
const PHASES = [
  // UX Research phases
  {
    jsonPath: join(UX_BASE, '00_fuzzy_front_end/prompts.json'),
    dir: join(UX_BASE, '00_fuzzy_front_end'),
    idPrefix: 'uxr.00_fuzzy_front_end',
    phase: 'discovery',
    category: 'Early Ideation & Exploration',
    folder: '00_fuzzy_front_end',
    tierMap: { 'capture-initial-idea': 1, 'explore-problem-space': 1, 'industry-analysis': 2, 'competitive-analysis': 2, 'explore-user-segments': 2, 'predict-trend-evolution': 3, 'combine-ideas': 3 },
    producesMap: { 'capture-initial-idea': 'initial_concept', 'industry-analysis': 'industry_pain_points', 'predict-trend-evolution': 'trend_analysis', 'combine-ideas': 'combined_concept', 'explore-problem-space': 'problem_space_map', 'competitive-analysis': 'competitive_landscape', 'explore-user-segments': 'user_segment_analysis' },
    requiresMap: {}
  },
  {
    jsonPath: join(UX_BASE, '01_define_problem/prompts.json'),
    dir: join(UX_BASE, '01_define_problem'),
    idPrefix: 'uxr.01_define_problem',
    phase: 'discovery',
    category: 'Problem Definition',
    folder: '01_define_problem',
    tierMap: { 'create-problem-statement': 1, 'create-proto-persona': 1, 'analyze-problem': 2, 'scope-problem': 2, 'qualify-problem': 2, 'problem-ecosystem': 3 },
    producesMap: { 'create-problem-statement': 'problem_statement', 'create-proto-persona': 'proto_persona', 'analyze-problem': 'problem_analysis', 'scope-problem': 'problem_scope', 'qualify-problem': 'problem_qualification', 'problem-ecosystem': 'ecosystem_map' },
    requiresMap: { 'create-proto-persona': ['problem_statement'], 'analyze-problem': ['problem_statement'], 'scope-problem': ['problem_statement'], 'qualify-problem': ['problem_statement'], 'problem-ecosystem': ['problem_statement'] }
  },
  {
    jsonPath: join(UX_BASE, '02_objectives/prompts.json'),
    dir: join(UX_BASE, '02_objectives'),
    idPrefix: 'uxr.02_objectives',
    phase: 'discovery',
    category: 'Objectives & Success Metrics',
    folder: '02_objectives',
    tierMap: { 'identify-core-objective': 1, 'define-success-metrics': 2, 'set-constraints': 2, 'define-anti-goals': 2, 'test-metrics': 3, 'platform-strategy': 3 },
    producesMap: { 'identify-core-objective': 'core_objective', 'define-success-metrics': 'success_metrics', 'set-constraints': 'constraints', 'test-metrics': 'metric_test_plan', 'define-anti-goals': 'anti_goals', 'platform-strategy': 'platform_strategy' },
    requiresMap: { 'identify-core-objective': ['problem_statement'], 'define-success-metrics': ['core_objective'], 'set-constraints': ['core_objective'], 'test-metrics': ['success_metrics'], 'define-anti-goals': ['core_objective'], 'platform-strategy': ['problem_statement'] }
  },
  {
    jsonPath: join(UX_BASE, '03_solution_hypothesis/prompts.json'),
    dir: join(UX_BASE, '03_solution_hypothesis'),
    idPrefix: 'uxr.03_solution_hypothesis',
    phase: 'discovery',
    category: 'Solution Hypothesis',
    folder: '03_solution_hypothesis',
    tierMap: { 'generate-solution-concept': 1, 'format-hypothesis-statement': 1, 'generate-essential-features': 2, 'risk-assessment': 2, 'solution-alternatives': 3, 'iteration-strategy': 3 },
    producesMap: { 'generate-solution-concept': 'solution_concept', 'format-hypothesis-statement': 'hypothesis_statement', 'generate-essential-features': 'feature_list', 'risk-assessment': 'risk_assessment', 'solution-alternatives': 'alternative_solutions', 'iteration-strategy': 'iteration_strategy' },
    requiresMap: { 'generate-solution-concept': ['problem_statement', 'core_objective'], 'format-hypothesis-statement': ['solution_concept'], 'generate-essential-features': ['hypothesis_statement'], 'risk-assessment': ['solution_concept'], 'solution-alternatives': ['problem_statement', 'core_objective'], 'iteration-strategy': ['solution_concept'] }
  },
  {
    jsonPath: join(UX_BASE, '04_user_flow/prompts.json'),
    dir: join(UX_BASE, '04_user_flow'),
    idPrefix: 'uxr.04_user_flow',
    phase: 'discovery',
    category: 'User Flow & Interaction',
    folder: '04_user_flow',
    tierMap: { 'map-primary-user-flow': 1, 'identify-screens-states': 1, 'identify-decision-points': 2, 'plan-error-handling': 2 },
    producesMap: { 'map-primary-user-flow': 'user_flow', 'identify-screens-states': 'screen_inventory', 'identify-decision-points': 'decision_points', 'plan-error-handling': 'error_handling_plan' },
    requiresMap: { 'map-primary-user-flow': ['solution_concept'], 'identify-screens-states': ['user_flow'], 'identify-decision-points': ['user_flow'], 'plan-error-handling': ['user_flow'] }
  },
  {
    jsonPath: join(UX_BASE, '05_prototype/prompts.json'),
    dir: join(UX_BASE, '05_prototype'),
    idPrefix: 'uxr.05_prototype',
    phase: 'discovery',
    category: 'Prototype Planning & Testing',
    folder: '05_prototype',
    tierMap: { 'define-prototype-scope': 1, 'define-test-questions': 1, 'choose-fidelity-level': 2, 'identify-key-interactions': 2, 'define-participant-criteria': 3, 'create-test-script': 3 },
    producesMap: { 'define-prototype-scope': 'prototype_scope', 'choose-fidelity-level': 'fidelity_decision', 'identify-key-interactions': 'key_interactions', 'define-test-questions': 'test_questions', 'define-participant-criteria': 'participant_criteria', 'create-test-script': 'test_script' },
    requiresMap: { 'define-prototype-scope': ['user_flow'], 'choose-fidelity-level': ['prototype_scope'], 'identify-key-interactions': ['prototype_scope'], 'define-test-questions': ['hypothesis_statement'], 'define-participant-criteria': ['test_questions'], 'create-test-script': ['test_questions'] }
  },
  {
    jsonPath: join(UX_BASE, '06_post_test_synthesis/prompts.json'),
    dir: join(UX_BASE, '06_post_test_synthesis'),
    idPrefix: 'uxr.06_post_test_synthesis',
    phase: 'discovery',
    category: 'Post-Test Analysis',
    folder: '06_post_test_synthesis',
    tierMap: { 'synthesize-test-patterns': 1, 'evaluate-hypothesis': 1, 'plan-next-iteration': 2, 'explore-pivot-options': 2 },
    producesMap: { 'synthesize-test-patterns': 'test_insights', 'evaluate-hypothesis': 'hypothesis_evaluation', 'plan-next-iteration': 'iteration_plan', 'explore-pivot-options': 'pivot_options' },
    requiresMap: { 'evaluate-hypothesis': ['hypothesis_statement'], 'plan-next-iteration': ['hypothesis_evaluation'], 'explore-pivot-options': ['hypothesis_evaluation'] }
  },
  // Tech Requirements phases
  {
    jsonPath: join(TECH_BASE, '01_data_models/prompts.json'),
    dir: join(TECH_BASE, '01_data_models'),
    idPrefix: 'tech.01_data_models',
    phase: 'spec',
    category: 'Data Models',
    folder: '01_data_models',
    tierMap: { 'define-data-model': 1, 'validate-data-model': 2, 'data-access-patterns': 2, 'data-volume-scaling': 3 },
    producesMap: { 'define-data-model': 'data_models', 'validate-data-model': 'data_model_validation', 'data-access-patterns': 'data_access_patterns', 'data-volume-scaling': 'scaling_assessment' },
    requiresMap: { 'define-data-model': ['solution_concept'], 'validate-data-model': ['data_models'], 'data-access-patterns': ['data_models'], 'data-volume-scaling': ['data_models'] }
  },
  {
    jsonPath: join(TECH_BASE, '02_api_contracts_interfaces/prompts.json'),
    dir: join(TECH_BASE, '02_api_contracts_interfaces'),
    idPrefix: 'tech.02_api_contracts',
    phase: 'spec',
    category: 'API Contracts & Interfaces',
    folder: '02_api_contracts_interfaces',
    tierMap: { 'define-api-endpoints': 1, 'interface-boundaries': 2, 'api-standards': 2, 'integration-requirements': 3 },
    producesMap: { 'define-api-endpoints': 'api_contracts', 'interface-boundaries': 'interface_spec', 'api-standards': 'api_standards', 'integration-requirements': 'integration_spec' },
    requiresMap: { 'define-api-endpoints': ['data_models', 'user_flow'], 'interface-boundaries': ['api_contracts'], 'api-standards': ['api_contracts'], 'integration-requirements': ['api_contracts'] }
  },
  {
    jsonPath: join(TECH_BASE, '03_business_logic_rules/prompts.json'),
    dir: join(TECH_BASE, '03_business_logic_rules'),
    idPrefix: 'tech.03_business_logic',
    phase: 'spec',
    category: 'Business Logic & Rules',
    folder: '03_business_logic_rules',
    tierMap: { 'define-business-rules': 1, 'map-decision-logic': 2, 'spec-calculations': 2, 'authorization-rules': 2 },
    producesMap: { 'define-business-rules': 'business_rules', 'map-decision-logic': 'decision_logic', 'spec-calculations': 'calculation_specs', 'authorization-rules': 'authorization_rules' },
    requiresMap: { 'define-business-rules': ['solution_concept', 'user_flow'], 'map-decision-logic': ['business_rules'], 'spec-calculations': ['business_rules'], 'authorization-rules': ['business_rules'] }
  }
];

function slugToOperation(slug) {
  return slug.replace(/-/g, '_');
}

function generateFrontmatter(prompt, phase) {
  const slug = prompt.slug;
  const operation = slugToOperation(slug);
  const tier = phase.tierMap[slug] || 2;
  const produces = phase.producesMap[slug] ? [phase.producesMap[slug]] : [];
  const requires = phase.requiresMap[slug] || [];
  const artifactName = phase.producesMap[slug] || operation;

  return `---
metadata:
  id: "${phase.idPrefix}.${operation}"
  slug: "${slug}"
  title: "${prompt.title}"
  version: "0.1.0"
  status: "active"
  phase: "${phase.phase}"
  category: "${phase.category}"
  type: "instruction"
  folder: "${phase.folder}"
  tags: ${JSON.stringify(prompt.tags || ['general'])}
  purpose: "${prompt.purpose || ''}"
  context: "${prompt.context || ''}"
  tier: ${tier}
dependencies:
  requires: ${JSON.stringify(requires)}
  produces: ${JSON.stringify(produces)}
  optional: []
output:
  format: "markdown"
  sections: []
  max_length: "500 words"
  artifact_name: "${artifactName}"
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

function hasCompleteFrontmatter(content) {
  if (!content.startsWith('---')) return false;
  return content.includes('tier:') && content.includes('simulation:') && content.includes('artifact_name:');
}

let stats = { created: 0, updated: 0, skipped: 0, errors: 0 };

for (const phase of PHASES) {
  if (!existsSync(phase.jsonPath)) {
    console.log(`SKIP: ${phase.jsonPath} not found`);
    continue;
  }

  const json = JSON.parse(readFileSync(phase.jsonPath, 'utf-8'));
  console.log(`\n=== ${json.category || phase.folder} (${json.prompts.length} prompts) ===`);

  for (const prompt of json.prompts) {
    const filePath = join(phase.dir, prompt.filename);

    if (!existsSync(filePath)) {
      console.log(`  WARN: ${prompt.filename} not found, skipping`);
      stats.errors++;
      continue;
    }

    const content = readFileSync(filePath, 'utf-8').trim();

    // Already has complete frontmatter
    if (hasCompleteFrontmatter(content)) {
      console.log(`  SKIP: ${prompt.filename} (already complete)`);
      stats.skipped++;
      continue;
    }

    const frontmatter = generateFrontmatter(prompt, phase);

    if (content.length === 0) {
      // Empty file: write frontmatter + body from JSON
      const body = prompt.prompt || '';
      writeFileSync(filePath, `${frontmatter}\n${body}\n`);
      console.log(`  CREATE: ${prompt.filename} (was empty, wrote from JSON)`);
      stats.created++;
    } else if (content.startsWith('---')) {
      // Has old/incomplete frontmatter: replace entirely
      const endOfFrontmatter = content.indexOf('---', 3);
      if (endOfFrontmatter > 0) {
        const body = content.substring(endOfFrontmatter + 3).trim();
        writeFileSync(filePath, `${frontmatter}\n${body}\n`);
        console.log(`  UPDATE: ${prompt.filename} (replaced incomplete frontmatter)`);
        stats.updated++;
      }
    } else {
      // Has content but no frontmatter: prepend
      writeFileSync(filePath, `${frontmatter}\n${content}\n`);
      console.log(`  CREATE: ${prompt.filename} (prepended frontmatter)`);
      stats.created++;
    }
  }
}

console.log(`\n=== Migration Summary ===`);
console.log(`Created: ${stats.created}`);
console.log(`Updated: ${stats.updated}`);
console.log(`Skipped: ${stats.skipped}`);
console.log(`Errors:  ${stats.errors}`);
