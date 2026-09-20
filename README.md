# _mediumroast

The repository for Jason Bauman's personal website and research publications at [mediumroast.dev](https://mediumroast.dev).

Originally built with custom Python scripts and static HTML, the site is now powered by [Astro](https://astro.build/) with type-safe Content Collections, automated RSS/sitemap feeds, and a coffee-inspired design system.

## Writing & Publishing Posts

Published articles live in `src/content/blog/` as Markdown (`.md`) files. 

You can also draft or stage posts in the `.gitignored` `drafts/` folder:

```bash
# Sync completed drafts from drafts/ into src/content/blog/
npm run sync-drafts
```

### Frontmatter Schema

Each article uses standard frontmatter:

```markdown
---
title: "Your Post Title"
date: "October 14, 2026"
summary: "A crisp 1–2 sentence overview for the card, dossier, and RSS feed."
tags: ["coding/ai", "benchmarking"]
crosspost: true          # Set to true to feature as a tabbed console card on /work
type: "Research"         # Optional: "Research", "Project", or "Development"
reading_time: 5          # Optional: reading time in minutes
draft: false             # Set true to hold as draft, false to publish
---

Your markdown content here...
```

## Commands

```bash
# Start local development server (http://localhost:4321)
npm run dev

# Sync markdown files from drafts/ folder
npm run sync-drafts

# Validate types and frontmatter schemas
npm run check

# Build production static site (dist/)
npm run build
```
