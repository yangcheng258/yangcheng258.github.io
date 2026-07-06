# Yang Cheng — personal website

Static site for Yang Cheng — Postdoctoral Research Associate, Department of Agricultural & Applied Economics, University of Wisconsin–Madison.

Live at **https://yangcheng258.github.io/**

---

## Stack

- Plain HTML, CSS, JavaScript — no framework, no build step at the JS layer
- One Python script (`build.py`, stdlib only) for content generation
- Hosted on GitHub Pages

## Architecture

The site is **template-driven**. Every paper, dataset, code release, talk, briefing, post is **one HTML file** in `content/<type>/` or `posts/`. Running `python3 build.py` reads those files and rewrites the cards/rows on the rest of the site automatically.

```
content/
├── publications/   ← papers (article, working paper, book chapter, dissertation, report)
├── code-data/      ← datasets and code releases
├── talks/          ← conference talks
├── briefings/      ← policy briefings
└── teaching/       ← courses
posts/              ← long-form blog posts
build.py            ← scans content/ + posts/ → injects HTML between marker comments
*.html              ← rendered pages
shared.css          ← design tokens (Geist + Newsreader, accent moss green)
```

## File index

What every file is, at a glance. **Don't rename the `.html` files at root** — their names are the public URLs (e.g. `yangcheng258.github.io/research/livability.html`), and `index.html` is what GitHub Pages serves as the homepage.

### Pages (public URLs)

| File | What it is |
|---|---|
| `index.html` | **Landing page** — hero with looping video + "Explore Research →" |
| `about.html` | Bio + sidebar |
| `research/index.html` | Research overview — the 3 theme cards |
| `research/livability.html` | Theme 01 · Rural Livability & Quality of Life |
| `research/workforce.html` | Theme 02 · Workforce & the Green Economy |
| `research/migration.html` | Theme 03 · Migration & Place Choice (lit-review stage) |
| `impact/index.html` | Make-an-Impact overview (category grid) |
| `impact/teaching.html` … | Impact subcategory pages (teaching, talks, media, policy-briefings, extension, conferences, consulting, public-good) |
| `resources.html` | The living library — posts, tutorials, datasets, code, reading lists, CV. (Papers live on the Research pages; talks & briefings under Make an Impact) |
| `contact.html` | Email, office address, "how to reach out" cards |

### Source & machinery (not public-facing)

| File / folder | What it is |
|---|---|
| `content/publications/` | One file per paper — `YYYY-slug.html` (e.g. `2026-air.html`) |
| `content/code-data/` | One file per dataset / code release |
| `content/talks/` · `briefings/` · `teaching/` | Same pattern; only `_template.html` so far |
| `posts/` | Blog posts — `YYYY-MM-DD-slug.html` |
| `build.py` | Reads `content/` + `posts/`, regenerates the auto-gen sections |
| `shared.css` | Design system (fonts, colors, layout) |
| `UPDATING.md` · `content/README.md` · `CLAUDE.md` | How-to docs |
| `Hero.html` | Legacy design reference — not linked from the site |
| `.nojekyll` | Required by GitHub Pages — **never delete** |

**Naming convention going forward:** pages keep plain descriptive names (they're URLs); content files are `YYYY-slug.html` so they sort chronologically inside their type folder — the folder itself is the category, so no prefix needed.

## Local development

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## Adding content

Three short docs cover everything:

- **`UPDATING.md`** — full how-to for adding/editing/deleting any kind of content
- **`content/README.md`** — schemas + AI prompts for new entries
- **`CLAUDE.md`** — project context (read by Claude Code in future sessions)

The short version: copy a template from `content/<type>/_template.html`, fill it in, run `python3 build.py`. Done.

## Deploy

GitHub Pages serves from the `main` branch root automatically. Push a commit, the site updates in ~1 minute.

```bash
python3 build.py        # regenerate HTML from content/
git add -A && git commit -m "..."
git push
```

## License

Site source: MIT. Content (papers, posts, etc.): © Yang Cheng, all rights reserved unless otherwise noted.
