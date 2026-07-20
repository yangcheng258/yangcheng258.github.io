# CLAUDE.md — context for future sessions

This file is read automatically when Claude opens this project. It captures the architectural decisions, conventions, and "how things work" so future sessions don't re-derive context from scratch.

---

## What this is

Yang Cheng's personal academic website. Static HTML/CSS/JS, no framework. Hosted on GitHub Pages.

**Live at:** https://yangcheng258.github.io/
**Repo:** https://github.com/yangcheng258/yangcheng258.github.io (public, `main` branch)

**Owner:** Yang Cheng — Postdoctoral Research Associate, Department of Agricultural & Applied Economics, UW–Madison.

**Two research themes (active) + one in lit-review:**
1. Rural Livability & Quality of Life (research/livability.html) — methods, wellbeing, housing/health
2. Workforce & the Green Economy (research/workforce.html) — OGP Index, NLP greenness, Vona wage-premium replication
3. Migration & Place Choice (research/migration.html) — lit-review stage

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
<meta name="pub:sections" content="livability">
```

The build script reads this and injects accordingly. Multi-section is comma-separated.

Available section keys:
- `livability` · `workforce` · `migration` — one flat, year-sorted publication list per theme page (July 2026 simplification; legacy sub-keys like `livability-A` are normalized to the theme by build.py)
- `resources` (code-data: dataset-subtype items with this key show in the resources Datasets section; code-subtype lives on impact/public-good.html “Research Tools”, hand-edited)
- `impact-public-good` (for code-data only)

---

## Page inventory

| File | Purpose | Auto-gen sections |
|---|---|---|
| `index.html` | Home — headshot left + name/intro right over hero; backdrop is a detail band of Wang Ximeng's 千里江山图 (assets/images/qianli-jiangshan.jpg, extracted from user's PDF; top edge feathered into cream via mask + multiply; credit line removed at user request; hero fixed ~660px tall); pup removed from home (July 2026) — runner remains on life.html (user moved it below the photo grid) | hand-edited only |
| `about.html` | Bio + sidebar | hand-edited only |
| `research/index.html` | ONE-PAGE research — 3 foldable theme sections (animated logo badges, sticky headers) | 3 PUBS + 3 PUBCOUNT marker pairs |
| `impact/index.html` | Make-an-Impact — bento: 1 big card (Extension) + 4 small (Research out loud / Reproducibility / Talks / Teaching), each led by an <image-slot> photo the user drops in | hand-edited |
| `resources.html` | Living library: tutorials + posts + datasets + reading lists + CV (news/code removed — code lives on impact Research Tools) | 5 marker pairs |
| `contact.html` | Email/address + "How to reach out" intent cards | hand-edited only |
| `life.html` | "Life, off the clock" — 6 image-slot photo grid + cavalier runner; nav tab between Resources and Contact | hand-edited |
| `impact/{extension,media,talks,public-good,teaching}.html` | The 5 category pages: 01 Working with Communities · 02 Media, Press & Public Talks · 03 Academic Community · 04 Research Tools · 05 Teaching & Mentoring | hand-edited |

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
  - Mineral palette sampled from 千里江山图: `--azurite: #2f5b84`, `--azurite-deep: #244c71`, `--malachite-pale: #6b9462`, `--silk-gold: #9c7d42`
  - **Hover rule (July 2026): rest = moss, hover = azurite** — all interactive hover states site-wide (nav, footer, cards, arrows, chips, hero CTA) answer in `--azurite`; moss stays for identity (tags, em, aria-current, borders at rest). Reference sheet: "Palette — Qianli Jiangshan.html"
  - `--footer-bg: #e8e3d5` (slightly darker cream for footer block)
- **Convention:** italic Newsreader serif for emphasis (`<em>`), accent color for hover states + decorative letters
- **Topbar:** sticky, blurred bg, dropdown nav for Research themes, CV button on the right — full-bleed since July 2026 (breaks out of .shell like the footer: negative side margins + `padding: 18px max(56px, calc(50vw - 544px))`, margin-top cancels shell top padding; per-breakpoint overrides at 900/720px keep gutters aligned)
- **Footer:** full-width gray block with Navigate column + Contact column (email + 4 social icons + disclaimer)

---

## Real vs placeholder content

**Real (verified from Yang's project files):**
- Identity: name, postdoc role, dept, UW–Madison, `cheng297@wisc.edu`
- Office: 321 Taylor Hall, 427 Lorch Street, Madison WI 53705
- PhD: Virginia Tech, Ag & Applied Economics, May 2024, dissertation *Tasks, Skills, and Jobs in the Green Economy* (advisor Susan E. Chen; committee Andrew Katz, Suqin Ge, Jeffrey Alwang)
- 10 publications (in content/publications/); Move, Stay, and Commit (Social Indicators Research 183:23, 2026) added July 2026 from the Springer page
- 2 code/data items (OGP Index, Housing_health repo)
- Frequent collaborators: Tessa Conroy, Steven Deller, Erin Gaede, Mckenzie Boyce, Susan Chen, Andrew Katz
- Online: GitHub `yangcheng258`, LinkedIn `yangcheng2019`, Google Scholar `6o_n2I4AAAAJ`, ORCID `0009-0007-6102-4742`

**Placeholder (still to be replaced when ready):**
- Talks, briefings, teaching content (folders empty — `_template.html` only)
- Some entries in `impact/index.html` are commented-out placeholders, ready to uncomment when real entries exist

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
- **Home hero** (July 2026): static headshot + Qianli Jiangshan painting band in marked STATIC SCENE block; old hero video kept at assets/videos/hero.mp4, wiring AND leftover .hero-video-layer CSS removed; uploads/ emptied pre-export (source PDF deleted after extracting assets/images/qianli-jiangshan.jpg + qianli-crop.png)

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
- ~~Hero video CloudFront URL~~ — done (July 2026): re-encoded to ~9 MB and self-hosted at `assets/videos/hero.mp4`; index.html points there

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

---

## Small pending items (July 2026)

- Book-chapter co-author confirmed July 2026: Danielle Schmidt-Larios (content/publications/2026-rural-livability-chapter.html)
- Talks: real titles confirmed from photos July 2026 — C2ER "Rural Livability" (Jun 17 2026, Memphis) and MCRSA/IMPLAN "Temporal Change in QoL across U.S. County Typologies" (Jun 12 2026, w/ Conroy & Deller); per-post LinkedIn URLs still pending; NARSC year still assumed 2025
- Real photos received July 2026: assets/images/{headshot,talk-c2er-2026,talk-mcrsa-2026,team-lunch,pup-ball}.jpg + pup-watercolor.png (pup is a tri-color cavalier PUPPY — art spec: whole-black body, white legs, white face w/ black crown+ears, brown eyebrow, CARRIES coral ball in mouth (no separate ball); pup-ball.jpg prefills the life-pup slot; watercolor unused so far) — headshot on home hero; other three prefill impact <image-slot> src (extension=team-lunch, talks=C2ER, outloud=MCRSA). the Whova promo card was deleted in the July 2026 cleanup
- content/code-data/ogp-index.html had title "open governance performance index" — corrected July 2026 to "Occupational Greenness Potential measures"; its github_url is still empty (impact page links the GitHub profile as fallback)

- papers/ per-publication pages REMOVED July 2026 at user request (Google Scholar citation_* tags went with them; revisit if Scholar indexing matters later)

- July 2026 pre-export cleanup (user request): DELETED Hero.html, Illustrated Hero (archived), logo iterations v1/v2 + standalone/offline bundles (kept "Research Theme Logos v3.html" as the editable logo source; final SVGs in assets/logos/), retired research theme pages + index-old-backup + all-research-draft, orphaned impact pages (policy-briefings/conferences/consulting), uploads/ (all copied to assets/images/ first), and the Whova C2ER card. assets/videos/hero.mp4 KEPT intentionally (user's archived asset). Revert for any of these = git history.

## Launch holdbacks (July 19 2026 — site published imperfect on purpose)

Hidden until real material exists; each is marked "LAUNCH HOLDBACK" at the spot:
1. CV button + Resources tab/footer links — two CSS rules at the bottom of shared.css (delete rule to restore). Restore CV when assets/pdfs/CV.pdf is dropped; restore Resources when there's a first real post + CV row.
2. life.html — 5 empty photo figures commented out (pup photo remains).
3. impact/index.html — cards 04/05 bx-media commented out (text-only cards).
4. posts/2026-05-09-example-post.html DELETED; its generated entries manually stripped from resources.html (identical to a build.py rerun).

## Publication display conventions (July 2026, per user)

- Working papers show NO target journal (venue = "Working paper").
- Under review / R&R shown in venue text: "Under review at <i>Journal</i>" / "Revise & resubmit at <i>Journal</i>".
- Cite button (build.py apa_citation) copies an APA one-liner to the clipboard; pub:cite meta overrides the generated text (used for WIndicator's official suggested citation, DOI 10.21231/pv02-aa79). Copy JS lives in research/index.html (hand-edited, outside markers).
- research/index.html generated sections were regenerated manually in-editor July 2026 to match; a build.py rerun produces the same output.
- Author-order corrections applied July 2026 (housing-health: Gaede first; livability chapter: Boyce, Schmidt-Larios, Gaede, Cheng — now R&R at Journal of Rural Studies, type working-paper).
- "Under review at Rural Sociology" (housing-health): journal name from user's note ("journal of rural sociology") — CONFIRM whether Rural Sociology or Journal of Rural Social Sciences.
- DOI-verified July 2026: PiRS title corrected to official "Multidimensional Measures of Quality of Life: A Comparison of Methods Using U.S. County-level Data"; Deller = "Steven C. Deller" on both published papers; exact APA set in pub:cite for PiRS + Move-Stay-Commit.
- Link chips on research/index.html: single row of 4 — Slides / DOI / Repo (pub:code, falls back to pub:data) / Cite; PDF button removed July 2026; green fill, azurite hover, unavailable = muted outline chips.

## Homepage research block (July 2026)

- index.html now ends with a "Current research" section (#research): three tab buttons (McCrory-style switcher) showing ONE theme's publication list at a time; hero CTA scrolls down to it (href="#research").
- The three PUBS + PUBCOUNT marker pairs are DUPLICATED on index.html; build.py injects into both research/index.html and index.html (root gets no ../ path fix).
- Copied research-page styles/scripts live inline in index.html; tf-head is hidden there (tabs replace fold headers).
- July 2026: Research DROPPED from topbar nav on all pages (homepage #research section replaces it; tab-switcher honors #livability/#workforce/#migration hashes). Footer Navigate links now point to index.html#research + theme hashes. research/index.html KEPT on disk (still built by build.py) but no longer linked — restore its navgroup from git history if ever needed.
- Abstracts (July 2026, per user): only REAL abstracts are shown — official texts in housing-health + move-stay-commit; other working papers have EMPTY abstract divs (expander shows only theme chips). Don't invent abstracts.
- pub:order meta (July 2026): optional integer; ordered papers sort first (ascending), rest follow year-desc. Used on workforce papers (target order 1-7: 1 recsys, 2 NLP, 3 clustering [pending], 4 Appalachia readiness [pending], 5 transition shock [pending], 6 dissertation, 7 wage premium). build.py sort updated to match.
- July 2026: "Make an Impact" links KEPT but flagged: topbar + footer show a plain link with an "in progress" chip (.nav-soon/.sf-soon, CSS at bottom of shared.css); the navgroup dropdown is removed (subpages reachable from the overview cards). Restore the dropdown from git history when complete.
