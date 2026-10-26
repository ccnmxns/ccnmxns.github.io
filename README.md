# Carlos Cañellas — personal site

A simple static website. Posts are Markdown files; no database or browser JavaScript is required.

## Add a post

Create `content/posts/my-new-post.md`:

```markdown
---
title: My new post
date: 2026-10-26
summary: A short description for the blog listing.
draft: false
---

Write your post here in **Markdown**.
```

Use lowercase filenames separated by hyphens. The filename becomes `/blog/my-new-post/`. Set `draft: true` to exclude a post. Dates use YYYY-MM-DD. Posts appear newest first. Fenced code blocks, tables, lists, links, and images are supported. Content is trusted author-written Markdown and may include HTML.

## Build and preview

Requires Python 3.10+.

```sh
python3 -m pip install -r requirements.txt
python3 build.py
python3 -m http.server 8765 --directory dist
```

Open http://localhost:8765. Upload the contents of `dist/` to your static host, or ask Codex to rebuild and publish this Site after editing your Markdown. Saving a Markdown file alone does not update the hosted site.

Edit `templates/home.html` for the homepage; `dist/` is generated. The original Alpine Linux post has been imported from ccnmxns.me without revalidating or updating its technical instructions.
