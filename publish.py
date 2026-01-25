import sys
import os
import re
import markdown
import datetime
import subprocess

TEMPLATE_FILE = 'blog_template.html'
BLOG_DIR = 'blog'

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    # Expecting:
    # ---
    # key: value
    # ---
    # Body...
    
    frontmatter = {}
    body = content

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        body = match.group(2)
        
        for line in fm_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                frontmatter[key.strip()] = value.strip()
    
    return frontmatter, body

def format_date(date_str):
    # Try different formats and standardize to "Month DD, YYYY"
    formats = [
        "%Y-%m-%d",       # 2026-01-25
        "%m/%d/%Y",       # 01/25/2026
        "%m/%d/%y",       # 01/25/26
        "%B %d, %Y"       # January 25, 2026
    ]
    
    for fmt in formats:
        try:
            dt = datetime.datetime.strptime(date_str, fmt)
            return dt.strftime("%B %d, %Y")
        except ValueError:
            continue
    
    # Return original if parsing fails, but warn
    print(f"Warning: Could not parse date '{date_str}'. Keeping original.")
    return date_str

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 publish.py drafts/your-post.md")
        return

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: Template '{TEMPLATE_FILE}' not found.")
        return

    print(f"Processing {filepath}...")
    
    # 1. Parse content
    frontmatter, body_markdown = parse_markdown(filepath)
    
    # 2. Extract metadata
    title = frontmatter.get('title', 'Untitled')
    raw_date = frontmatter.get('date', datetime.date.today().strftime("%Y-%m-%d"))
    tags = frontmatter.get('tags', '')
    meta_desc = frontmatter.get('meta', '')

    # 3. Check Published Status
    # Default to True if missing (for backward compatibility)
    published_status = str(frontmatter.get('published', 'True')).strip().lower()
    if published_status != 'true':
        print(f"Skipping {filepath}: Frontmatter 'published' is not True.")
        return

    # 4. Format Date
    formatted_date = format_date(raw_date)

    # 4. Convert Markdown to HTML
    html_content = markdown.markdown(body_markdown, extensions=['fenced_code', 'codehilite'])

    # 4b. Auto-rewrite image paths
    # Finds <img src="filename.jpg"> and converts to <img src="../photos/filename.jpg">
    # Ignores src starting with http, https, data:, /, or ../
    def rewrite_img_src(match):
        src = match.group(1)
        if src.startswith(('http:', 'https:', 'data:', '/', '../')):
            return match.group(0) # No change
        return f'<img src="../photos/{src}"'

    html_content = re.sub(r'<img\s+[^>]*src=["\']([^"\']+)["\']', rewrite_img_src, html_content)

    # 5. Read Template
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template = f.read()

    # 6. Inject Data
    final_html = template.replace('{{title}}', title)
    final_html = final_html.replace('{{date}}', formatted_date)
    final_html = final_html.replace('{{tags}}', tags)
    final_html = final_html.replace('{{meta}}', meta_desc)
    final_html = final_html.replace('{{content}}', html_content)

    # 7. Write to blog/ directory
    filename = os.path.basename(filepath).replace('.md', '.html')
    output_path = os.path.join(BLOG_DIR, filename)
    
    # Canonical URL
    canonical_url = f"https://mediumroast.dev/blog/{filename}"
    final_html = final_html.replace('{{url}}', canonical_url)
    
    # Create blog dir if not exists (though it should)
    if not os.path.exists(BLOG_DIR):
        os.makedirs(BLOG_DIR)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"Successfully published to {output_path}")

    # 8. Run Manifest Generator
    print("Updating blog manifest...")
    subprocess.run(["python3", "generate_manifest.py"])

if __name__ == "__main__":
    main()
