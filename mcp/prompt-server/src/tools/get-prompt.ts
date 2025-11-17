/**
 * get_prompt tool - retrieve a single prompt by ID or slug
 */

import { Prompt } from '../types/prompt.js';

export function formatPromptDetail(prompt: Prompt) {
  return {
    metadata: prompt.frontmatter.metadata,
    dependencies: prompt.frontmatter.dependencies,
    validation: prompt.frontmatter.validation,
    mcp: prompt.frontmatter.mcp,
    body: prompt.body,
    filePath: prompt.filePath,
  };
}
