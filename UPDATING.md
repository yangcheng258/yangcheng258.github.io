# How to update the site

**Live at:** https://yangcheng258.github.io/

The site is **template-driven**. Every paper, post, dataset, code release, talk, briefing, and course is one small HTML file. A build script (`python3 build.py`) reads them and rewrites the rest of the site automatically.

You do not edit livability.html, workforce.html, resources.html, or any other "main" page to add a paper. You add a content file and run the build.

---

## Folder map

```
Personal website beta/
├── content/                       ← source-of-truth for everything
│   ├── publications/              ← papers, working papers, book chapters, dissertation, reports
│   ├── code-data/                 ← datasets and code releases
│   ├── talks/                     ← conference talks (empty until used)
│   ├── briefings/                 ← policy briefings (empty until used)
│   ├── teaching/                  ← courses (empty until used)
│   └── README.md                  ← schemas + AI prompts
├── posts/                         ← blog-style posts (long-form articles)
├── assets/
│   ├── pdfs/                      ← drop CVs, paper PDFs, briefings, slides
│   ├── images/                    ← portraits, photos, thumbnails
│   └── videos/                    ← hero videos, talk recordings
├── build.py                       ← regenerates the site from content/
├── *.html                         ← rendered pages (don't hand-edit auto-gen sections)
├── shared.css                     ← design tokens
└── UPDATING.md                    ← this file
```

---

## The core loop (every change goes through this)

1. **Add or edit** a file in `content/<type>/` or `posts/`
2. **Run** `python3 build.py` from the project root
3. **Done** — every relevant page on the site is regenerated

That's it. No HTML editing across multiple files, no copy-paste between cards.

---

## Adding content

### A new paper

1. Copy the template:
   ```
   cp content/publications/_template.html content/publications/2026-myslug.html
   ```
2. Edit the meta tags + abstract in the new file. The most important meta tag is:
   ```html
   <meta name="pub:sections" content="livability-B,resources">
   ```
   This tells the build script which page-sections to feature the paper on. Multi-section is just comma-separated.

   Allowed sections: `livability-A` · `livability-B` · `livability-C` · `workforce-A` · `workforce-B` · `migration` · `resources`
3. Run `python3 build.py`. The paper appears on every named section.

### A new code release / dataset

```
cp content/code-data/_template.html content/code-data/my-tool.html
```
Edit. Run build.

### A new talk / briefing / course

Same pattern: copy the template in `content/talks/`, `content/briefings/`, or `content/teaching/`, edit, build.

(These don't yet have target page injection wired up — they'll appear once impact subpages get their markers. Until then the files exist as ready records.)

### A new blog post

```
cp posts/_template-post.html posts/2026-05-15-my-post.html
```
Fill in metadata + body. Run build. Card appears on resources.html.

---

## Common tasks

### Update a paper title

Open `content/publications/2026-pirs-methods.html`. Change the `<meta name="pub:title">` value. Run build. Every page that lists this paper updates.

### Move a paper to a different theme section

Open the paper's content file. Change `<meta name="pub:sections">` (e.g. `livability-A,resources` → `livability-B,resources`). Run build. Paper moves to the new section, disappears from the old.

### Delete a paper

Delete the file in `content/publications/`. Run build. Card gone everywhere.

### Drop a real PDF in

1. Save the file in `assets/pdfs/` with a clean filename (lowercase, hyphens, no spaces).
2. In the paper's content file, set `<meta name="pub:pdf" content="assets/pdfs/your-file.pdf">`.
3. Run build.

### Update CV

Drop new file at `assets/pdfs/CV.pdf`. The nav link is hardcoded to that path — no edits needed.

### Update bio / hero / contact text

These are hand-edited (they're one-off content). Open `about.html`, `index.html`, or `contact.html` directly.

---

## AI workflow

`content/README.md` has copy-paste prompts for each content type. The pattern:

> "Generate a file at `content/publications/[slug].html` using the schema in `content/publications/_template.html`. Here are the details: [paste informally]. Reply with the full file contents I can save directly."

Save Claude's reply to disk. Run build. Done.

---

## Allowed values (match exactly — typos warn + skip)

| Field | Values |
|---|---|
| `pub:type` | `article` · `working-paper` · `book-chapter` · `dissertation` · `report` |
| `pub:status` | `published` · `in-revision` · `in-progress` · `drafted` |
| `pub:themes` (space-sep) | `rural` · `qol` · `green` · `housing` · `health` · `datasci` · `ai` |
| `pub:sections` (comma-sep) | `livability-A` · `livability-B` · `livability-C` · `workforce-A` · `workforce-B` · `migration` · `resources` |
| `code:subtype` | `dataset` · `code` |
| `code:sections` | `resources` · `impact-public-good` |
| `post:type` | `tutorial` · `news` · `paper` · `event` |
| `post:theme` (single) | from same theme list above |

---

## Site-wide find-and-replace (the rare bulk edits)

Some things appear on every page and aren't in `content/`. To change globally, search across the project:

| What | Where to search/replace |
|---|---|
| Email | `cheng297@wisc.edu` |
| GitHub URL | `https://github.com/yangcheng258` |
| LinkedIn URL | `linkedin.com/in/yangcheng2019` |
| Google Scholar | `scholar.google.com/citations?user=6o_n2I4AAAAJ` |
| ORCID | `orcid.org/0009-0007-6102-4742` |
| Bio paragraphs | only in `about.html` |
| Office address | only in `contact.html` |
| Hero text | only in `index.html` |

---

## Run locally

```bash
python3 -m http.server 8000
```
Open http://localhost:8000/ in your browser.

## Deploy (push to GitHub Pages)

The site is **already deployed** — every push to `main` updates https://yangcheng258.github.io/ in about 30 seconds. There's no build step on GitHub's side; Pages just serves the files in the repo as-is.

The deploy loop:

```bash
python3 build.py                          # regenerate auto-gen sections from content/
git add -A
git commit -m "Describe the change"
git push
# wait ~30 seconds, hard-refresh the live site
```

That's the whole loop. No CI, no GitHub Actions, no Vercel — just push.

**Important: do not delete `.nojekyll`** (empty file at project root). It tells GitHub Pages "skip Jekyll processing." Without it, files in folders starting with `_` (like our `_template.html` files) get hidden, and pages 404.

For a custom domain later: add a `CNAME` file with the domain, point DNS at GitHub Pages.

---

## What build.py does (under the hood)

When you run it:
1. Scans `posts/` and every `content/<type>/` folder
2. Parses each file's `<meta name="ns:...">` tags + `<body>` content
3. Sorts by date (newest first)
4. Generates the right HTML format per destination:
   - Theme pages (livability/workforce/migration) get `<div class="pub-full">` blocks
   - resources.html grid gets `<a class="post-card">` cards
   - resources.html sections get `<a class="record-row">` rows
5. Writes inside `<!-- AUTO-GENERATED ... START / END -->` markers
6. Leaves everything outside the markers untouched

If a paper has `pub:sections="livability-A,resources"`, the build:
- Generates a `pub-full` block for livability.html Section A
- Generates a `post-card` for resources.html grid
- Generates a `record-row` for resources.html sections-view Paper section

All from one source file. Edit it once, propagates everywhere.

---

## When you hit something the system doesn't handle

The build script can be extended. Examples of changes that'd need a script update:
- New content type (e.g. "thesis advising")
- New section on a theme page
- New target page (e.g. an awards page)
- Changing the card layout

Send me the requirement and I'll extend `build.py` accordingly. The pattern is consistent: each new content type gets a `load_files()` call + an inject function + marker comments in the target HTML.

The script is ~350 lines, no dependencies, easy to read and modify.
