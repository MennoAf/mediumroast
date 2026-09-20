// scripts/sync-drafts.js
// Synchronizes markdown files from the .gitignored drafts/ folder into src/content/blog/

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..');
const DRAFTS_DIR = path.join(ROOT_DIR, 'drafts');
const BLOG_DIR = path.join(ROOT_DIR, 'src', 'content', 'blog');

// Files to ignore in drafts folder
const IGNORE_FILES = new Set(['template.md', 'style-test.md', 'README.md']);

function parseFrontmatter(content) {
  const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/);
  if (!match) return { data: {}, body: content, hasFrontmatter: false };

  const yamlBlock = match[1];
  const body = match[2];
  const data = {};

  for (const line of yamlBlock.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const colonIdx = trimmed.indexOf(':');
    if (colonIdx === -1) continue;

    const key = trimmed.slice(0, colonIdx).trim();
    let val = trimmed.slice(colonIdx + 1).trim();

    // Strip quotes
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    // Parse booleans
    if (val.toLowerCase() === 'true') val = true;
    else if (val.toLowerCase() === 'false') val = false;

    data[key] = val;
  }

  return { data, body, hasFrontmatter: true, rawYaml: yamlBlock };
}

function syncDrafts() {
  if (!fs.existsSync(DRAFTS_DIR)) {
    console.log(`[INFO] No drafts directory found at ${DRAFTS_DIR}`);
    return;
  }

  if (!fs.existsSync(BLOG_DIR)) {
    fs.mkdirSync(BLOG_DIR, { recursive: true });
  }

  const files = fs.readdirSync(DRAFTS_DIR).filter(f => f.endsWith('.md') && !IGNORE_FILES.has(f));
  let updatedCount = 0;
  let skippedCount = 0;

  console.log(`\n☕ Scanning ${files.length} markdown file(s) in drafts/...\n`);

  for (const file of files) {
    const draftPath = path.join(DRAFTS_DIR, file);
    const content = fs.readFileSync(draftPath, 'utf-8');
    const { data } = parseFrontmatter(content);

    // If explicitly marked published: false or draft: true, skip
    if (data.published === false || data.draft === true) {
      console.log(`  [SKIPPED] ${file} (marked draft: true or published: false)`);
      skippedCount++;
      continue;
    }

    // Target file in src/content/blog/
    // Standardize slug to kebab-case
    const baseName = file.replace(/_/g, '-');
    const destPath = path.join(BLOG_DIR, baseName);

    const existingContent = fs.existsSync(destPath) ? fs.readFileSync(destPath, 'utf-8') : null;

    if (existingContent === content) {
      console.log(`  [UNCHANGED] ${baseName}`);
      continue;
    }

    fs.writeFileSync(destPath, content, 'utf-8');
    console.log(`  [UPDATED] ${file} -> src/content/blog/${baseName}`);
    updatedCount++;
  }

  console.log(`\n✓ Sync complete! ${updatedCount} updated, ${skippedCount} drafts skipped.\n`);
}

syncDrafts();
