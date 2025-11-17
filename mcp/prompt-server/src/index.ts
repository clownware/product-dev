/**
 * MCP Server for AI-Assisted Product Development Prompt Library
 * 
 * Exposes prompts via Model Context Protocol (MCP) as resources and tools.
 * See ADR 0002 for design decisions.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import path from 'path';
import { fileURLToPath } from 'url';
import { MarkdownLoader } from './loaders/markdown-loader.js';
import { filterPrompts, formatPromptListItem } from './tools/list-prompts.js';
import { formatPromptDetail } from './tools/get-prompt.js';
import { ListPromptsFilters } from './types/prompt.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Resolve prompts directory (../../prompts from the dist/ folder)
const PROMPTS_DIR = path.resolve(__dirname, '../../..', 'prompts');

class PromptMCPServer {
  private server: Server;
  private loader: MarkdownLoader;

  constructor() {
    this.server = new Server(
      {
        name: 'prompt-library',
        version: '0.1.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.loader = new MarkdownLoader(PROMPTS_DIR);
    this.setupHandlers();
  }

  private setupHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'list_prompts',
          description:
            'List available prompts with optional filters (tags, phase, category, status)',
          inputSchema: {
            type: 'object',
            properties: {
              tags: {
                type: 'array',
                items: { type: 'string' },
                description: 'Filter by tags (prompts matching any tag)',
              },
              phase: {
                type: 'string',
                description: 'Filter by lifecycle phase (e.g., discovery, spec)',
              },
              category: {
                type: 'string',
                description: 'Filter by category',
              },
              status: {
                type: 'string',
                enum: ['draft', 'active', 'deprecated'],
                description: 'Filter by status',
              },
            },
          },
        },
        {
          name: 'get_prompt',
          description: 'Get a single prompt by ID or slug',
          inputSchema: {
            type: 'object',
            properties: {
              id: {
                type: 'string',
                description: 'Prompt ID (e.g., uxr.00_fuzzy_front_end.capture_initial_idea)',
              },
              slug: {
                type: 'string',
                description: 'Prompt slug (e.g., capture-initial-idea)',
              },
            },
            oneOf: [{ required: ['id'] }, { required: ['slug'] }],
          },
        },
      ],
    }));

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      if (name === 'list_prompts') {
        const filters = args as ListPromptsFilters;
        const allPrompts = await this.loader.loadAllPrompts();
        const filtered = filterPrompts(allPrompts, filters);
        const formatted = filtered.map(formatPromptListItem);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(formatted, null, 2),
            },
          ],
        };
      }

      if (name === 'get_prompt') {
        const { id, slug } = args as { id?: string; slug?: string };
        
        let prompt;
        if (id) {
          prompt = await this.loader.getPromptById(id);
        } else if (slug) {
          prompt = await this.loader.getPromptBySlug(slug);
        }

        if (!prompt) {
          throw new Error(`Prompt not found: ${id || slug}`);
        }

        const formatted = formatPromptDetail(prompt);

        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(formatted, null, 2),
            },
          ],
        };
      }

      throw new Error(`Unknown tool: ${name}`);
    });

    // List resources (prompts as resources)
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      const prompts = await this.loader.loadAllPrompts();

      return {
        resources: prompts.map((p) => ({
          uri: `prompt://${p.frontmatter.metadata.id}`,
          name: p.frontmatter.metadata.title,
          description: p.frontmatter.metadata.purpose,
          mimeType: 'text/markdown',
        })),
      };
    });

    // Read resource (get prompt by URI)
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;
      
      if (!uri.startsWith('prompt://')) {
        throw new Error(`Invalid resource URI: ${uri}`);
      }

      const id = uri.replace('prompt://', '');
      const prompt = await this.loader.getPromptById(id);

      if (!prompt) {
        throw new Error(`Prompt not found: ${id}`);
      }

      const formatted = formatPromptDetail(prompt);

      return {
        contents: [
          {
            uri,
            mimeType: 'application/json',
            text: JSON.stringify(formatted, null, 2),
          },
        ],
      };
    });
  }

  async start() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Prompt MCP Server running on stdio');
  }
}

// Start the server
const server = new PromptMCPServer();
server.start().catch(console.error);
