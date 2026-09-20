import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const blog = await getCollection('blog', ({ data }) => !data.draft);
  const sorted = blog.sort((a, b) => {
    const dateA = a.data.pubDate ? new Date(a.data.pubDate).getTime() : 0;
    const dateB = b.data.pubDate ? new Date(b.data.pubDate).getTime() : 0;
    return dateB - dateA;
  });

  return rss({
    title: '_mediumroast',
    description: 'Technical Director & Maker. Thoughts on autonomous agents, AI evaluation, technical SEO, and engineering systems.',
    site: context.site ?? 'https://mediumroast.dev',
    items: sorted.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate ?? new Date(post.data.date),
      description: post.data.summary,
      link: `/blog/${post.id}`,
    })),
    customData: `<language>en-us</language>`,
  });
}
