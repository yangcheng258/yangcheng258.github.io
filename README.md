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
