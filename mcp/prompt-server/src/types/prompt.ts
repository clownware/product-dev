/**
 * Type definitions for prompt metadata schema (per ADR 0001)
 */

export interface PromptMetadata {
  id: string;
  slug: string;
  title: string;
  version: string;
  status: 'draft' | 'active' | 'deprecated';
  phase: string;
  category: string;
  type: 'template' | 'instruction' | 'workflow' | 'context';
  folder: string;
  tags: string[];
  purpose: string;
  context: string;
}

export interface PromptDependencies {
  requires: string[];
  produces: string[];
}

export interface PromptValidation {
  gate: string;
  criteria: string[];
}

export interface PromptMCP {
  exposed: boolean;
  operation: string;
}

export interface PromptFrontmatter {
  metadata: PromptMetadata;
  dependencies: PromptDependencies;
  validation: PromptValidation;
  mcp: PromptMCP;
}

export interface Prompt {
  frontmatter: PromptFrontmatter;
  body: string;
  filePath: string;
}

export interface ListPromptsFilters {
  tags?: string[];
  phase?: string;
  category?: string;
  status?: string;
}
