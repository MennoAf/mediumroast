import os
import sys
import subprocess
import glob
import re
from datetime import datetime

# Configuration
DRAFTS_DIR = 'drafts'
BLOG_DIR = 'blog'

def get_frontmatter(filepath):
    """
    Reads the file and parses the YAML frontmatter.
    Returns a dict of metadata and the start index of the body.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    meta = {}
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        fm_text = match.group(1)
        for line in fm_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                meta[key.strip()] = value.strip().strip('"\'') # Strip quotes if present
    
    return meta

def should_publish(draft_path, html_path, meta):
    """
    Determines if a draft should be published.
    """
    is_published = meta.get('published', 'False').lower() == 'true'
    
    if not is_published:
        return False, "Not published"

    if not os.path.exists(html_path):
        return True, "New post"
    
    draft_mtime = os.path.getmtime(draft_path)
    html_mtime = os.path.getmtime(html_path)
    
    if draft_mtime > html_mtime:
        return True, "Draft updated"
    
    return False, "Up to date"

def main():
    print("--- Starting Blog Deployment ---")
    
    # Ensure drafts directory exists
    if not os.path.exists(DRAFTS_DIR):
        print(f"Error: {DRAFTS_DIR} not found.")
        return

    # 1. Process Drafts
    drafts = glob.glob(os.path.join(DRAFTS_DIR, '*.md'))
    changes_made = False
    
    for draft_path in drafts:
        filename = os.path.basename(draft_path)
        slug = filename.replace('.md', '.html')
        html_path = os.path.join(BLOG_DIR, slug)
        
        try:
            meta = get_frontmatter(draft_path)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            continue

        publish, reason = should_publish(draft_path, html_path, meta)
        
        if publish:
            print(f"Publishing {filename} ({reason})...")
            # Call publish.py
            result = subprocess.run(["python3", "publish.py", draft_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  Success.")
                changes_made = True
            else:
                print(f"  Failed: {result.stderr}")
        
        # Handle unpublishing (optional but good for syncing)
        is_published = meta.get('published', 'False').lower() == 'true'
        if not is_published and os.path.exists(html_path):
            print(f"Unpublishing {filename} (removing {html_path})...")
            os.remove(html_path)
            changes_made = True

    # 2. Refresh Manifest (if not already run by publish.py, or if unpublished changes occurred)
    # publish.py runs it, but if we unpublished something, we need to run it again. 
    # Or if we just want to be sure.
    print("Refreshing blog_posts.js...")
    subprocess.run(["python3", "generate_manifest.py"])

    # 3. Git Commit and Push
    if changes_made:
        print("Committing and pushing changes...")
        # Add all changes
        subprocess.run(["git", "add", "."])
        
        # Commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"Blog update {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_msg])
        
        # Push
        push_result = subprocess.run(["git", "push"])
        if push_result.returncode == 0:
            print("Successfully pushed to GitHub.")
        else:
            print("Error pushing to GitHub.")
    else:
        print("No changes to deploy.")

    print("--- Deployment Complete ---")

if __name__ == "__main__":
    main()
