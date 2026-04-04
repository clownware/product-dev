/**
 * Markdown loader for parsing prompt files with YAML frontmatter
 */

import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';
import { Prompt, PromptFrontmatter } from '../types/prompt.js';

export class MarkdownLoader {
  private promptsDir: string;

  constructor(promptsDir: string) {
    this.promptsDir = promptsDir;
  }

  /**
   * Recursively find all markdown files in a directory
   */
  async findMarkdownFiles(dir: string): Promise<string[]> {
    const files: string[] = [];
    
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          const subFiles = await this.findMarkdownFiles(fullPath);
          files.push(...subFiles);
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          files.push(fullPath);
        }
      }
    } catch (error) {
      console.error(`Error reading directory ${dir}:`, error);
    }
    
    return files;
  }

  /**
   * Load and parse a single prompt file
   */
  async loadPrompt(filePath: string): Promise<Prompt | null> {
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      const parsed = matter(content);
      
      // Check if this is a prompt file (has metadata.id) and not a rules file.
      // NOTE: Tier 1 prompts (v2 frontmatter, ADR 0009) use flat `name:` fields
      // instead of `metadata.id` and are intentionally excluded here. The MCP
      // server currently only serves v1 (Tier 2/3) prompts. V2 loader support
      // is deferred to Phase 5 — see ADR 0008 and the implementation roadmap.
      if (!parsed.data.metadata?.id || parsed.data.type === 'rules') {
        return null;
      }

      const frontmatter = parsed.data as PromptFrontmatter;
      
      // Validate required fields
      if (!frontmatter.metadata || !frontmatter.mcp) {
        console.warn(`Prompt ${filePath} missing required frontmatter fields`);
        return null;
      }

      return {
        frontmatter,
        body: parsed.content.trim(),
        filePath: path.relative(this.promptsDir, filePath),
      };
    } catch (error) {
      console.error(`Error loading prompt ${filePath}:`, error);
      return null;
    }
  }

  /**
   * Load all prompts from the prompts directory
   */
  async loadAllPrompts(): Promise<Prompt[]> {
    const markdownFiles = await this.findMarkdownFiles(this.promptsDir);
    const prompts: Prompt[] = [];

    for (const file of markdownFiles) {
      const prompt = await this.loadPrompt(file);
      if (prompt && prompt.frontmatter.mcp.exposed) {
        prompts.push(prompt);
      }
    }

    return prompts;
  }

  /**
   * Get a single prompt by ID
   */
  async getPromptById(id: string): Promise<Prompt | null> {
    const prompts = await this.loadAllPrompts();
    return prompts.find(p => p.frontmatter.metadata.id === id) || null;
  }

  /**
   * Get a single prompt by slug
   */
  async getPromptBySlug(slug: string): Promise<Prompt | null> {
    const prompts = await this.loadAllPrompts();
    return prompts.find(p => p.frontmatter.metadata.slug === slug) || null;
  }
}
