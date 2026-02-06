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

    # Extract Summary (First paragraph in article-content)
    # Search for the first <p> tag anywhere after <div class="article-content">
    summary_match = re.search(r'<div class="article-content">.*?<p>(.*?)</p>', content, re.DOTALL)
    raw_summary = summary_match.group(1) if summary_match else ""
    
    # Clean up summary
    summary = strip_tags(raw_summary)

    # Calculate reading time
    # Extract all text content from article
    article_content_match = re.search(r'<div class="article-content">(.*?)</div>', content, re.DOTALL)
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
        "summary": summary,
        "reading_time": reading_time,
        "filename": os.path.basename(filepath)
    }

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

    # Output as JavaScript file to avoid CORS/Fetch issues on local file:// protocol
    js_content = f"window.BLOG_POSTS = {json.dumps(posts, indent=4)};"
    
    output_js = "blog_posts.js"
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Successfully generated {output_js} with {len(posts)} posts.")

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
