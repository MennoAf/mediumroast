import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.string(),
    pubDate: z.coerce.date().optional(),
    tags: z.union([z.array(z.string()), z.string()]).transform(val => {
      if (Array.isArray(val)) return val.map(t => t.replace(/^#/, '').trim()).filter(Boolean);
      if (typeof val === 'string' && val.length > 0) {
        return val.split(',').map(t => t.replace(/^#/, '').trim()).filter(Boolean);
      }
      return [];
    }).default([]),
    crosspost: z.boolean().default(false),
    type: z.string().default('Project'),
    reading_time: z.number().optional(),
    draft: z.boolean().default(false),
    command: z.string().optional(),
    tabLabel: z.string().optional(),
    status: z.string().optional(),
    terminalLogs: z.array(z.string()).optional(),
    takeaway: z.string().optional(),
  }),
});

export const collections = { blog };
