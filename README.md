# _mediumroast (Astro CMS)

A personal site, research showcase, and publication platform for Jason Bauman, converted to [Astro](https://astro.build/) with type-safe Content Collections and a modern CMS workflow.

## Features

- **Homepage Terminal Animation**: Iconic `$ skills --list` terminal accent with typewriter cycling through skills and a blinking amber cursor.
- **Coffee Design System**: Coffee bean (dark mode) and coffee flower (light mode) theme toggle with zero flash of unstyled content (FOUC) and `localStorage` persistence.
- **Content Collections (`src/content.config.ts`)**: Type-safe frontmatter schema with validation for posts, tags, dates, reading times, and project crossposting.
- **Work & Research (`/work`)**: Automatic showcase aggregating research posts and projects with code-editor styled cards (macOS traffic-light window accents).
- **Interactive Blog & Tag System (`/blog`)**: Instant client-side tag filtering plus dedicated `/tags/[...tag]` archive routes.
- **RSS & Sitemap Feeds**: Auto-generated `/rss.xml` and `/sitemap-index.xml` for AI discovery and feed readers.
- **Mermaid Diagrams & GitHub Callouts**: Native support for architecture charts and styled callout boxes.

## Project Structure

```
├── astro.config.mjs         # Astro configuration (site: 'https://mediumroast.dev')
├── package.json             # Scripts and dependencies
├── tsconfig.json            # TypeScript configuration
├── public/                  # Static assets: favicon.svg, CNAME, robots.txt, photos/
└── src/
    ├── content.config.ts    # Content collections schema
    ├── content/
    │   └── blog/            # Markdown articles (*.md, *.mdx)
    ├── components/          # Astro components (Header, Footer, ThemeToggle, etc.)
    ├── layouts/             # BaseLayout and BlogPostLayout
    ├── pages/               # File-based routing (index, work, about, blog, contact, tags)
    └── styles/              # Global CSS with coffee-inspired custom properties
```

## Adding a New Post

Create a new `.md` or `.mdx` file in `src/content/blog/`:

```markdown
---
title: "Your Post Title"
date: "October 14, 2026"
pubDate: 2026-10-14
tags: ["ai", "architecture"]
crosspost: true          # Set true to feature on /work
type: "Research"         # Development, Research, or Project
summary: "A brief summary for the blog card and RSS feed."
reading_time: 5
draft: false             # Set true to hide from production builds
---

Your content here...
```

## Local Development

```bash
# Start the local development server (with hot reload)
npm run dev

# Check types and content collections
npm run check

# Build production static site (outputs to dist/)
npm run build

# Preview the production build locally
npm run preview
```
