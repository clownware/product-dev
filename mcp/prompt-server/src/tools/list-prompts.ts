/**
 * list_prompts tool - list and filter available prompts
 */

import { Prompt, ListPromptsFilters } from '../types/prompt.js';

export function filterPrompts(
  prompts: Prompt[],
  filters: ListPromptsFilters
): Prompt[] {
  let filtered = prompts;

  // Filter by status
  if (filters.status) {
    filtered = filtered.filter(
      p => p.frontmatter.metadata.status === filters.status
    );
  }

  // Filter by phase
  if (filters.phase) {
    filtered = filtered.filter(
      p => p.frontmatter.metadata.phase === filters.phase
    );
  }

  // Filter by category
  if (filters.category) {
    filtered = filtered.filter(
      p => p.frontmatter.metadata.category === filters.category
    );
  }

  // Filter by tags (prompt must have at least one matching tag)
  if (filters.tags && filters.tags.length > 0) {
    filtered = filtered.filter(p =>
      filters.tags!.some(tag => p.frontmatter.metadata.tags.includes(tag))
    );
  }

  return filtered;
}

export function formatPromptListItem(prompt: Prompt) {
  return {
    id: prompt.frontmatter.metadata.id,
    slug: prompt.frontmatter.metadata.slug,
    title: prompt.frontmatter.metadata.title,
    purpose: prompt.frontmatter.metadata.purpose,
    phase: prompt.frontmatter.metadata.phase,
    category: prompt.frontmatter.metadata.category,
    tags: prompt.frontmatter.metadata.tags,
    status: prompt.frontmatter.metadata.status,
  };
}
