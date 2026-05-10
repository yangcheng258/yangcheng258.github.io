# CLAUDE.md — context for future sessions

This file is read automatically when Claude opens this project. It captures the architectural decisions, conventions, and "how things work" so future sessions don't re-derive context from scratch.

---

## What this is

Yang Cheng's personal academic website. Static HTML/CSS/JS, no framework. Hosted on GitHub Pages.

**Live at:** https://yangcheng258.github.io/
**Repo:** https://github.com/yangcheng258/yangcheng258.github.io (public, `main` branch)

**Owner:** Yang Cheng — Postdoctoral Research Associate, Department of Agricultural & Applied Economics, UW–Madison.

**Two research themes (active) + one in lit-review:**
1. Rural Livability & Quality of Life (livability.html) — methods, wellbeing, housing/health
2. Workforce & the Green Economy (workforce.html) — OGP Index, NLP greenness, Vona wage-premium replication
3. Migration & Place Choice (migration.html) — lit-review stage

---

## Architecture

### Source-of-truth: `content/` folder

Every paper, dataset, code release, talk, briefing, and course is **one HTML file** in `content/<type>/`. Each file has metadata in `<meta name="ns:field" content="value">` tags + body content (abstract, description). The build script reads them and rewrites the rest of the site.

```
content/
├── publications/   ← papers (article, working paper, book chapter, dissertation, report)
├── code-data/      ← datasets and code releases
├── talks/          ← conference talks
├── briefings/      ← policy briefings
└── teaching/       ← courses
```

`posts/` (sibling of content/) holds long-form blog posts, also auto-built.

### Build script: `python3 build.py`

- Scans every `content/<type>/` folder + `posts/`
- Parses each file's metadata + body
- Generates appropriate HTML (pub-full blocks, post-cards, record-rows) per destination
- Replaces content between `<!-- AUTO-GENERATED ... START -->` / `END` markers in target HTML files
- Leaves everything outside markers untouched (so hand-edited copy is preserved)

### Routing via `pub:sections` (and similar)

Each content file declares which page-sections it should appear in:

```html
<meta name="pub:sections" content="livability-A,resources">
```

The build script reads this and injects accordingly. Multi-section is comma-separated.

Available section keys:
- `livability-A` (Methods) · `livability-B` (Wellbeing) · `livability-C` (Housing & rural health)
- `workforce-A` (OGP Index) · `workforce-B` (Wage premium)
- `migration`
- `resources`
- `impact-public-good` (for code-data only)

---

## Page inventory

| File | Purpose | Auto-gen sections |
|---|---|---|
| `index.html` | Home — hero with looping video + "Explore Research →" CTA | hand-edited only |
| `about.html` | Bio + sidebar | hand-edited only |
| `research.html` | Research overview — 3 theme cards | hand-edited only |
| `livability.html` | Theme 01 — 3 sections (A/B/C) with auto-injected pub blocks | 3 marker pairs |
| `workforce.html` | Theme 02 — 2 sections (A/B) | 2 marker pairs |
| `migration.html` | Theme 03 — empty Featured Publications section | 1 marker pair |
| `impact.html` | Make-an-Impact category grid + list (placeholders commented out) | n/a (commented) |
| `resources.html` | Filterable library (grid + sectioned list views) | 7 marker pairs |
| `contact.html` | Email/address + "How to reach out" intent cards | hand-edited only |
| `impact/policy-briefings.html` etc. | Stub pages for impact subcategories | not yet wired to build |

---

## Design system (in `shared.css`)

- **Fonts:** Geist (sans), Geist Mono (mono), Newsreader (serif)
- **Color tokens:**
  - `--bg: #f6f4ef` (cream background)
  - `--fg: #1a1a1a` (near-black text)
  - `--muted: #6a6a66`
  - `--line: #d8d4ca`
  - `--card: #fbfaf6`
  - `--accent: #4a5d3a` (moss green — used for italic emphasis, links, accent borders)
  - `--footer-bg: #e8e3d5` (slightly darker cream for footer block)
- **Convention:** italic Newsreader serif for emphasis (`<em>`), accent color for hover states + decorative letters
- **Topbar:** sticky, blurred bg, dropdown nav for Research themes, CV button on the right
- **Footer:** full-width gray block with Navigate column + Contact column (email + 4 social icons + disclaimer)

---

## Real vs placeholder content

**Real (verified from Yang's project files):**
- Identity: name, postdoc role, dept, UW–Madison, `cheng297@wisc.edu`
- Office: 321 Taylor Hall, 427 Lorch Street, Madison WI 53705
- PhD: Virginia Tech, Ag & Applied Economics, May 2024, dissertation *Tasks, Skills, and Jobs in the Green Economy* (advisor Susan E. Chen; committee Andrew Katz, Suqin Ge, Jeffrey Alwang)
- 9 publications (in content/publications/)
- 2 code/data items (OGP Index, Housing_health repo)
- Frequent collaborators: Tessa Conroy, Steven Deller, Erin Gaede, Mckenzie Boyce, Susan Chen, Andrew Katz
- Online: GitHub `yangcheng258`, LinkedIn `yangcheng2019`, Google Scholar `6o_n2I4AAAAJ`, ORCID `0009-0007-6102-4742`

**Placeholder (still to be replaced when ready):**
- Talks, briefings, teaching content (folders empty — `_template.html` only)
- Some entries in `impact.html` are commented-out placeholders, ready to uncomment when real entries exist
- `Hero.html` and `index_v1.html` are legacy files from the original design bundle — left in place but not linked

---

## Common workflows

| Task | Steps |
|---|---|
| Add a paper | Copy `content/publications/_template.html` → fill in → `python3 build.py` |
| Edit a paper | Open the content file → change one meta tag → `python3 build.py` |
| Delete a paper | Delete the file → `python3 build.py` |
| Add a post | Copy `posts/_template-post.html` → fill in → `python3 build.py` |
| Drop a real PDF | Save to `assets/pdfs/`, set the `pub:pdf` meta tag |
| Update CV | Drop `assets/pdfs/CV.pdf` (no edits needed — link is hardcoded) |
| Update bio / hero / contact text | Hand-edit `about.html` / `index.html` / `contact.html` (these are one-off) |
| Site-wide find/replace | Search for the literal value (email, URL, etc.) and replace across files |
| Deploy a change | `python3 build.py && git add -A && git commit -m "..." && git push` — Pages updates in ~30s |

Full guide for the user: `UPDATING.md` (in project root).

---

## Deployment (GitHub Pages)

The site is deployed via GitHub Pages from the `main` branch root of `yangcheng258/yangcheng258.github.io`.

**Critical file: `.nojekyll`** (empty file at repo root) — disables GitHub's default Jekyll processing. Without it, Pages tries to parse the site as a Jekyll project and 404s on most pages because folders starting with `_` (like `posts/_template-post.html` or any `_template.html`) are hidden from output. Don't delete this file.

**Deploy loop:**
```bash
python3 build.py                                # regenerate auto-gen sections
git add -A
git commit -m "Describe the change"
git push                                        # Pages picks up commit, updates in ~30s
```

No CI, no GitHub Actions — Pages serves the repo as-is.

**Local preview:**
```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

---

## Conventions / preferences

- **No emojis** in HTML or copy unless the user explicitly asks
- **Italic Newsreader for emphasis**, accent color for the italic em
- **Prefer pure CSS** over JS (no hamburger menu, no client-side rendering — everything ships pre-rendered)
- **No build dependencies** — Python stdlib only
- **Mobile responsive** via shared.css `@media (max-width: 720px)` + per-page inline mobile rules (because some theme pages have inline `<style>` that overrides shared)
- **Footer is full-width gray** with negative-margin breakout (`margin-left: calc(50% - 50vw); width: 100vw`)
- **Hero video** plays at full saturation, no `mix-blend-mode`, no big cream overlay (text sits at `align-items: flex-start` so it stays in the small cream zone at top of hero-wrap)

---

## When user makes changes

The user is a researcher, not a developer. Their preferred workflow:
1. Describe changes informally
2. Have Claude make the edits
3. Run `python3 build.py` if content files changed
4. Hard refresh browser to verify

**Never edit auto-generated sections by hand** — they get overwritten on next `build.py` run. If a change needs to persist, edit the source content file or extend the build script.

---

## Structural follow-ups (deferred)

- Wire `content/talks/`, `content/briefings/`, `content/teaching/` to their respective `impact/*.html` subpages (no real entries yet, so deferred)
- Consider migrating to a static site generator (Hugo / Eleventy / Astro) when content volume exceeds ~100 items per type — current Python script is fine until then
- The hero video src is a CloudFront URL from the original design tool; should be self-hosted in `assets/videos/` for long-term reliability

---

## Open question for the next session

The user asked, right before this session ended:

> "Sometimes when I want to hide some of the data or some of the files, how can I do that? A lot of people will scrape my data, so I need to make it not publicly available on GitHub. If I make it publicly available, people will be able to get it, so how do I hide it?"

**Context.** The repo `yangcheng258/yangcheng258.github.io` is currently public so GitHub Pages can serve it on the free tier. Anything in the repo (including `assets/pdfs/`, `assets/data/`, future `content/` files) is world-readable and trivially scrapable.

**Options to lay out for the user when this comes back up:**

1. **Make the repo private** — As of 2023, GitHub Pages on the free tier supports private repos for `username.github.io` user-sites *only if you upgrade to Pro/Team*. On the free plan, private-repo Pages requires a paid plan. So this is "$4/mo to flip a switch."

2. **Keep repo public, host private files elsewhere** — Cheapest. Drop sensitive datasets in:
   - A private Google Drive / Dropbox folder, link with "request access"
   - A private GitHub repo (no Pages), share via collaborator invite
   - An institutional file server (UW–Madison Box, OneDrive)
   - Zenodo with restricted access
   
   The site links out to those locations with a "request access" note. Public site, private data.

3. **Two repos, one private** — Keep `yangcheng258.github.io` public (only the rendered HTML/CSS/JS that's already meant to be public). Move sensitive files (data, drafts, working PDFs) to a private repo or a `private/` folder excluded via `.gitignore`. The build script would need a flag for "draft mode" so private content doesn't accidentally appear in HTML output.

4. **Per-file `.gitignore`** — Simplest if the user just wants to keep specific files off GitHub. Add patterns like `assets/data/raw/`, `*.csv`, `_drafts/` to `.gitignore`. Files stay on local disk, never uploaded. No protection if already pushed (need `git rm --cached` + force push to scrub history).

5. **Robots / scrape deterrents** — `robots.txt` and `<meta name="robots" content="noindex">` discourage well-behaved crawlers (Google, Bing) but do nothing against scrapers. Not real protection — only signals intent.

**Recommendation when user returns:** Ask which kind of file they want to hide (a) draft papers / working PDFs, (b) raw datasets, (c) personal info like full CV with phone number, (d) something else — the right answer differs sharply by category.
