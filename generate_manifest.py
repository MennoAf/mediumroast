import os
import json
import re
from datetime import datetime

BLOG_DIR = 'blog'

def parse_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Helper to strip HTML tags
    from html.parser import HTMLParser
    
    class MLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.text = []
        def handle_data(self, d):
            self.text.append(d)
        def get_data(self):
            return "".join(self.text)

    def strip_tags(html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    # Extract Title
    title_match = re.search(r'<h1 class="article-title">(.*?)</h1>', content)
    raw_title = title_match.group(1) if title_match else "Untitled"
    title = strip_tags(raw_title)

    # Extract Date
    date_match = re.search(r'<span class="post-date">(.*?)</span>', content)
    date_str = date_match.group(1) if date_match else ""
    
    # Parse Date for sorting (assuming format "Month DD, YYYY")
    try:
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        iso_date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        iso_date = "1970-01-01"

    # Extract Tags
    tags_match = re.search(r'<span class="post-tags">(.*?)</span>', content)
    raw_tags = tags_match.group(1) if tags_match else ""
    tags = strip_tags(raw_tags)
    
    # Extract Crosspost & Type
    crosspost_match = re.search(r'<meta name="crosspost" content="(true|false)">', content)
    crosspost = crosspost_match.group(1) == 'true' if crosspost_match else False

    type_match = re.search(r'<meta name="project_type" content="(.*?)">', content)
    project_type = type_match.group(1) if type_match else "Project"

    # Extract Summary (First paragraph in article-content)
    # Search for the first <p> tag anywhere after <div class="article-content">
    summary_match = re.search(r'<div class="article-content">.*?<p>(.*?)</p>', content, re.DOTALL)
    raw_summary = summary_match.group(1) if summary_match else ""
    
    # Clean up summary
    summary = strip_tags(raw_summary)

    # Calculate reading time
    # Extract all text content from article — greedy match to capture nested divs
    article_content_match = re.search(
        r'<div class="article-content">(.*)</div>\s*(?:</div>)?\s*<!-- Social',
        content, re.DOTALL
    )
    if article_content_match:
        article_text = strip_tags(article_content_match.group(1))
        word_count = len(article_text.split())
        # Average reading speed: 200 words per minute
        reading_time = max(1, round(word_count / 200))
    else:
        reading_time = 1

    return {
        "title": title,
        "date": date_str,
        "iso_date": iso_date,
        "tags": tags,
        "crosspost": crosspost,
        "type": project_type,
        "summary": summary,
        "reading_time": reading_time,
        "filename": os.path.basename(filepath)
    }

def generate_blog_html(posts):
    """Generate blog.html with static post cards baked in.

    Crawlers see real content. Tag filtering is progressive enhancement via JS.
    """
    # Build static post cards
    post_cards = []
    for post in posts:
        tags_html = ''
        if post['tags']:
            tag_list = post['tags'].split()
            tags_html = ' '.join(
                f'<span class="tag-label">{t}</span>' for t in tag_list if t.startswith('#')
            )

        # data-tags attribute for JS filtering
        card = f'''            <article class="blog-post" data-date="{post['iso_date']}" data-tags="{post['tags']}">
                <h2><a href="blog/{post['filename']}" style="color: inherit;">{post['title']}</a></h2>
                <div class="post-meta">
                    <span class="post-date">{post['date']}</span>
                    <span class="post-reading-time">{post['reading_time']} min read</span>
                    <span class="post-tags">{tags_html}</span>
                </div>
                <div class="post-content">
                    <p>{post['summary']}</p>
                    <a href="blog/{post['filename']}" class="read-more">Read Article &rarr;</a>
                </div>
            </article>'''
        post_cards.append(card)

    posts_html = '\n'.join(post_cards) if post_cards else \
        '            <p style="text-align: center; color: var(--text-secondary);">No posts yet.</p>'

    # Collect unique tags for filter buttons
    all_tags = set()
    for post in posts:
        if post['tags']:
            for tag in post['tags'].split():
                if tag.startswith('#'):
                    all_tags.add(tag)

    filter_buttons = '<button class="tag-filter active" data-tag="all">All</button>'
    for tag in sorted(all_tags):
        filter_buttons += f'<button class="tag-filter" data-tag="{tag}">{tag}</button>'

    # Build the full page
    html = f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog | _mediumroast</title>
    <link rel="icon" type="image/svg+xml" href="favicon.svg">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&family=Inter:wght@400;600;700&display=swap"
        rel="stylesheet">

    <link rel="stylesheet" href="style.css">

    <!-- Analytics -->
    <script defer data-domain="mediumroast.dev" src="https://plausible.io/js/script.js"></script>
</head>

<body>

    <div id="site-header"></div>
    <script src="components/header.js"></script>
    <script>renderHeader('.');</script>

    <div style="height: 80px;"></div> <!-- Spacer for fixed header -->

    <section class="blog-section">
        <div class="container">
            <!-- Tag Filters -->
            <div class="tag-filters" id="tag-filters">
                {filter_buttons}
            </div>

            <div class="blog-list" id="blog-container">
{posts_html}
            </div>
        </div>
    </section>

    <!-- Progressive enhancement: tag filtering via JS -->
    <script>
        document.addEventListener("DOMContentLoaded", function () {{
            const container = document.getElementById('blog-container');
            const posts = container.querySelectorAll('.blog-post');

            document.querySelectorAll('.tag-filter').forEach(btn => {{
                btn.addEventListener('click', function () {{
                    document.querySelectorAll('.tag-filter').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');

                    const selectedTag = this.getAttribute('data-tag');
                    posts.forEach(post => {{
                        if (selectedTag === 'all' || (post.dataset.tags && post.dataset.tags.includes(selectedTag))) {{
                            post.style.display = '';
                        }} else {{
                            post.style.display = 'none';
                        }}
                    }});
                }});
            }});
        }});
    </script>

    <div id="site-footer"></div>
    <script src="components/footer.js"></script>
    <script>renderFooter(".");</script>
</body>

</html>'''

    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Successfully generated blog.html with static post cards.")


def main():
    posts = []
    if not os.path.exists(BLOG_DIR):
        print(f"Error: Directory '{BLOG_DIR}' not found.")
        return

    for filename in os.listdir(BLOG_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(BLOG_DIR, filename)
            try:
                post = parse_post(filepath)
                posts.append(post)
                print(f"Parsed: {filename}")
            except Exception as e:
                print(f"Failed to parse {filename}: {e}")

    # Sort by Date (Newest First)
    posts.sort(key=lambda x: x['iso_date'], reverse=True)

    # Generate static blog.html with post cards baked in
    generate_blog_html(posts)

    # Keep blog_posts.js for backwards compatibility (local dev, etc.)
    js_content = f"window.BLOG_POSTS = {json.dumps(posts, indent=4)};"

    output_js = "blog_posts.js"
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Successfully generated {output_js} with {len(posts)} posts.")

    # Update work.html with crossposts
    crossposts = [p for p in posts if p.get('crosspost')]
    crossposts_html = []
    for post in crossposts:
        card = f'''
            <div class="project-card code-editor" style="margin-bottom: 2rem;">
                <div class="editor-header" style="display: flex; align-items: center;">
                    <span class="dot red"></span>
                    <span class="dot yellow"></span>
                    <span class="dot green"></span>
                    <span class="filename" style="margin-left: 10px; font-size: 0.85rem; font-family: 'Fira Code', monospace;">{post['type']}</span>
                    <span style="margin-left: auto; font-size: 0.85rem; color: var(--text-secondary);">{post['date']}</span>
                </div>
                <div class="editor-content" style="padding: 1.5rem; background: var(--bg-card);">
                    <h2 style="margin-top: 0; margin-bottom: 1rem;"><a href="blog/{post['filename']}" style="color: inherit; text-decoration: none;">{post['title']}</a></h2>
                    <p style="color: var(--text-secondary); line-height: 1.6; margin-bottom: 1.5rem;">{post['summary']}</p>
                    <a href="blog/{post['filename']}" class="read-more" style="color: var(--accent-color); text-decoration: none; font-weight: 600; font-family: 'Fira Code', monospace; display: inline-block;">View Details &rarr;</a>
                </div>
            </div>'''
        crossposts_html.append(card)
        
    crosspost_content = '\n'.join(crossposts_html) if crossposts_html else '<p style="color: var(--text-secondary);">More projects coming soon.</p>'
    
    if os.path.exists("work.html"):
        with open("work.html", "r", encoding="utf-8") as f:
            work_content = f.read()
            
        work_content = re.sub(
            r'<!-- CROSSPOST_START -->.*?<!-- END_CROSSPOST -->',
            f'<!-- CROSSPOST_START -->\n{crosspost_content}\n                <!-- END_CROSSPOST -->',
            work_content,
            flags=re.DOTALL
        )
        
        with open("work.html", "w", encoding="utf-8") as f:
            f.write(work_content)
        print("Successfully updated work.html with crossposts.")

    # Generate Sitemap
    BASE_URL = "https://mediumroast.dev"
    static_pages = ["index.html", "about.html", "work.html", "blog.html", "contact.html"]
    
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Static Pages
    for page in static_pages:
        sitemap_content += '  <url>\n'
        sitemap_content += f'    <loc>{BASE_URL}/{page}</loc>\n'
        sitemap_content += '  </url>\n'

    # Blog Posts
    for post in posts:
        sitemap_content += '  <url>\n'
        sitemap_content += f'    <loc>{BASE_URL}/blog/{post["filename"]}</loc>\n'
        sitemap_content += f'    <lastmod>{post["iso_date"]}</lastmod>\n'
        sitemap_content += '  </url>\n'

    sitemap_content += '</urlset>'

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    
    print("Successfully generated sitemap.xml")

    # Generate RSS Feed
    rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content += '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
    rss_content += '  <channel>\n'
    rss_content += f'    <title>_mediumroast</title>\n'
    rss_content += f'    <link>{BASE_URL}</link>\n'
    rss_content += f'    <description>Technical blog by Jason Bauman - SEO, Data Engineering, AI, and more</description>\n'
    rss_content += f'    <language>en-us</language>\n'
    rss_content += f'    <atom:link href="{BASE_URL}/rss.xml" rel="self" type="application/rss+xml" />\n'
    
    # Add posts to RSS (already sorted by date, newest first)
    for post in posts:
        rss_content += '    <item>\n'
        rss_content += f'      <title>{post["title"]}</title>\n'
        rss_content += f'      <link>{BASE_URL}/blog/{post["filename"]}</link>\n'
        rss_content += f'      <description>{post["summary"]}</description>\n'
        rss_content += f'      <pubDate>{format_rfc822_date(post["iso_date"])}</pubDate>\n'
        rss_content += f'      <guid isPermaLink="true">{BASE_URL}/blog/{post["filename"]}</guid>\n'
        rss_content += '    </item>\n'
    
    rss_content += '  </channel>\n'
    rss_content += '</rss>'

    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)
    
    print("Successfully generated rss.xml")

def format_rfc822_date(iso_date):
    """Convert ISO date (YYYY-MM-DD) to RFC 822 format for RSS"""
    try:
        dt = datetime.strptime(iso_date, "%Y-%m-%d")
        # RFC 822 format: "Wed, 25 Jan 2026 00:00:00 GMT"
        return dt.strftime("%a, %d %b %Y 00:00:00 GMT")
    except ValueError:
        # Fallback to current date if parsing fails
        return datetime.now().strftime("%a, %d %b %Y 00:00:00 GMT")

if __name__ == "__main__":
    main()
