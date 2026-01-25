import os
import json
import re
from datetime import datetime

BLOG_DIR = 'blog'

def parse_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Title
    title_match = re.search(r'<h1 class="article-title">(.*?)</h1>', content)
    title = title_match.group(1) if title_match else "Untitled"

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
    tags = tags_match.group(1) if tags_match else ""

    # Extract Summary (First paragraph in article-content)
    # Search for the first <p> tag anywhere after <div class="article-content">
    summary_match = re.search(r'<div class="article-content">.*?<p>(.*?)</p>', content, re.DOTALL)
    summary = summary_match.group(1) if summary_match else ""
    
    # Clean up summary (remove any internal tags if present, simple clean)
    summary = re.sub(r'<[^>]+>', '', summary)

    return {
        "title": title,
        "date": date_str,
        "iso_date": iso_date,
        "tags": tags,
        "summary": summary,
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

if __name__ == "__main__":
    main()
