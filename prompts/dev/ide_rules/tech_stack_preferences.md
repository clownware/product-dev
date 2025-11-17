---
title: "Technology Stack Guidelines"
type: rules
scope: global
status: active
---
# Technology Stack Guidelines

_Living document outlining tech decisions, rationale, and tradeoffs_

## Table of Contents

- [Core Language Preferences](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#core-language-preferences)
- [Frontend Stack Options](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#frontend-stack-options)
- [CSS & Styling](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#css--styling)
- [Backend Stack](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#backend-stack)
- [BaaS & Infrastructure](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#baas--infrastructure)
- [Framework Selection Guide](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#framework-selection-guide)
- [Additional Specialized Tools](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#additional-specialized-tools)
- [Technologies to Avoid](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#technologies-to-avoid)
- [Experimental Tools](https://claude.ai/chat/c2602723-260f-40a0-9221-573c2bd185c9#experimental-tools)

## Core Language Preferences

- **TypeScript** (default) or **JavaScript** as primary language
- **Python** for backend tasks, API services, and data processing

## Frontend Stack Options

### Project Evaluation First

For new projects, always evaluate specific requirements before defaulting to any framework:

#### Primary Options Based on Project Needs:

- **Next.js/React** (React ecosystem)
    - When complex client-side state management is required
    - When leveraging the React ecosystem is advantageous
    - For applications with complex interactions and state
    - When team familiarity with React is high
- **Astro** (Content-focused)
    - For content-heavy websites and blogs
    - When minimal JavaScript and maximum performance are priorities
    - Can include React islands for interactive components
    - Excellent for marketing sites, documentation, and blogs
- **Qwik/Qwik City** (Performance-focused)
    - For instant load times and resumability in complex applications
    - When first-interaction performance is critical
    - Applications targeting mobile or low-bandwidth users
- **HTMX + Backend** (Server-driven)
    - For server-driven UIs with minimal client-side JavaScript
    - Good for CRUD applications, dashboards, and admin interfaces
    - Can be paired with any backend (FastAPI, Node.js, etc.)
    - When simplicity and maintainability are paramount
- **SvelteKit** (High-performance alternative)
    - When high-performance UI without React is desired
    - For smaller teams or projects where bundle size is critical
    - When reactive programming model is preferred

### Component Strategies:

- For **React**: Use **shadcn/ui** methodology (Radix UI primitives + Tailwind)
- For **Svelte**: Use lightweight component libraries or custom components
- For **Astro**: Mix and match components from different frameworks as needed
- For **HTMX**: Use backend templating with minimal frontend enhancements

## CSS & Styling

- Primary framework: **Tailwind CSS** (utility-first approach)
    - Preferred for all frontend frameworks (works with React, Svelte, HTMX, etc.)
    - Avoid custom CSS/inline styles unless absolutely necessary
    - For rare edge cases, prefer scoped CSS modules or CSS variables
- Theming: CSS variables preferred
- Avoid legacy CSS practices like BEM or global stylesheets
- Consider UnoCSS for Astro/Qwik projects (Tailwind-compatible but more performant)

## JavaScript Enhancement Options

- **Alpine.js**: For enhancing server-rendered HTML with minimal interactivity
- **HTMX**: For server-driven UI updates without full page refreshes
- **Stimulus**: For lightweight controllers when Alpine.js isn't sufficient

## Backend Stack

- **Next.js API Routes/Server Actions** (Node.js/TypeScript) for:
    - Data fetching tightly coupled to the frontend
    - Simple CRUD operations
    - Vercel edge functions
    - Authentication flows integrated with frontend
- **FastAPI** (Python) for:
    - Complex business logic and data processing
    - CPU-intensive tasks and background jobs
    - Standalone microservices
    - Leveraging Python's data science ecosystem
- Experimental: Open to exploring **Bun** for Node.js replacements

## BaaS & Infrastructure

- Primary Backend-as-a-Service: **Supabase** (PostgreSQL)
- Serverless/Edge Compute:
    - Options include Vercel, Netlify, or Cloudflare Pages for edge functions
    - Cloudflare Workers for global edge compute
- Container Standard: **Docker**
- Containerized Services:
    - Use **Docker** with platforms like Fly.io, Render, or Railway for:
        - Long-running background jobs
        - Complex stateful processes
        - Heavy computational workloads
        - Services requiring specific runtime environments

### Deployment Decision Timing

- Defer specific deployment platform decisions until:
    - Application architecture is defined
    - Performance requirements are clear
    - Scaling needs are understood
    - Budget constraints are established
- Design for platform flexibility when possible
- Use infrastructure-as-code to maintain deployment portability

## Framework Selection Guide

### Content-Heavy Websites

1. **Astro** (preferred)
    - Pros: Minimal JS, excellent performance, partial hydration
    - Ideal for: Marketing sites, blogs, documentation, portfolios
2. **Next.js with App Router**
    - Pros: Familiar React ecosystem, good SEO, static generation
    - Trade-offs: Heavier JS payload, more complex than needed

### Interactive Applications

1. **Next.js with App Router**
    - Pros: Rich ecosystem, server components, good DX
    - Ideal for: Complex web applications, dashboards with rich interactivity
2. **Qwik**
    - Pros: Instant interactivity, resumable hydration
    - Ideal for: Performance-critical applications, mobile-first experiences
3. **SvelteKit**
    - Pros: Smaller bundle size, simpler learning curve
    - Ideal for: Smaller teams, projects where bundle size matters

### Data-Heavy CRUD Applications

1. **HTMX + FastAPI/Node**
    - Pros: Server-driven, minimal JS, great performance
    - Ideal for: Admin interfaces, dashboards, forms
2. **Next.js with Server Actions**
    - Pros: Progressive enhancement, familiar React model
    - Trade-offs: More complex, larger bundle size

### Mixed Content + Interactions

1. **Astro with React/Svelte islands**
    - Pros: Best of both worlds - static content with interactive islands
    - Ideal for: Content sites with interactive elements

## Additional Specialized Tools

- **React Three Fiber (R3F)** → 3D visualizations using Three.js
- **Turso (libSQL)** → Edge-first, distributed database use cases
- **Electron / Tauri** → Desktop app delivery using web UI
- **RedwoodJS** → Full-stack apps with opinionated structure when React is required

## Alternative Ecosystems (Reference Only)

- **Remix, Gatsby** → React meta-frameworks with specific strengths
- **Vue/Nuxt.js** → For cross-framework context or comparisons
- **React Native / Expo** → For mobile development use cases

## Technologies to Avoid

- jQuery, Bootstrap, Laravel, or outdated/deprecated stacks
- Global CSS methodologies like BEM
- Traditional serverless functions (e.g., standard AWS Lambda) for:
    - Long-running processes (>10 seconds)
    - Memory-intensive operations
    - Stateful applications
    - (Instead, use containerized services for these cases)
- UI libraries like Ant Design, Chakra UI, or MUI unless specifically requested

## Experimental Tools

- **Bun** as Node.js alternative
- **Hono** for edge-optimized HTTP frameworks
- **tRPC** for type-safe APIs between TypeScript frontends and backends
- **Drizzle ORM** as a TypeScript-first alternative to Prisma
- **Lucia** as a lightweight auth library alternative to NextAuth
- **UnoCSS** as a faster Tailwind alternative