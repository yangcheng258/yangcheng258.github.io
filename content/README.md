# content/ — source-of-truth for everything on the site

Every paper, dataset, code release, talk, briefing, and course on the site is a single HTML file in one of these folders:

```
content/
├── publications/   ← papers (article, working paper, book chapter, dissertation, report)
├── code-data/      ← datasets and code releases
├── talks/          ← conference talks
├── briefings/      ← policy briefings
└── teaching/       ← courses taught
```

Each folder has a `_template.html` you copy for new entries. The build script (`python3 build.py` from project root) scans all folders and injects cards/rows into the right places across the site.

---

## Quick workflow

1. Copy a template: `cp content/publications/_template.html content/publications/2026-my-slug.html`
2. Edit the meta tags (the routing — `sections=...` — controls where it shows up) and the body content
3. Run `python3 build.py`
4. Done. Card appears wherever `sections` says.

---

## Allowed values (don't typo these)

### `themes` (space-separated, used everywhere)
`rural` · `qol` · `green` · `housing` · `health` · `datasci` · `ai`

### Publication `type`
`article` · `working-paper` · `book-chapter` · `dissertation` · `report`

### Publication `status`
`published` · `in-revision` · `in-progress` · `drafted`

### Publication `sections` (comma-separated)
`livability` · `workforce` · `migration` — one flat publication list per theme page (legacy `livability-A`-style keys are normalized automatically)

### Code/data `subtype`
`dataset` · `code`

### Code/data `sections`
`resources` · `impact-public-good`

### Talk `type`
`keynote` · `plenary` · `paper` · `discussant` · `panel` · `workshop`

### Teaching `role`
`taught` · `co-taught` · `TA`

---

## AI prompts (paste these into Claude/ChatGPT)

### Adding a publication

> Generate a file at `content/publications/[slug].html` using the schema in `content/publications/_template.html`. Here are the details:
>
> - **Title:** [paste title]
> - **Authors:** [Full Name, Full Name & Full Name — spelled out]
> - **Venue:** [journal name + volume OR "Working paper, targeting X"]
> - **Year:** [YYYY]
> - **Type:** article | working-paper | book-chapter | report | dissertation
> - **Status:** published | in-revision | in-progress | drafted
> - **Themes:** [from allowed list above]
> - **Sections:** [livability, workforce, migration — pick all that apply]
> - **PDF / Slides / DOI / Code / Data URLs:** [optional, leave blank if not available]
> - **Abstract:** [paste 1-3 paragraphs]
>
> Reply with the full file contents I can save directly. Filename should be `YYYY-short-slug.html`.

### Adding a code release / dataset

> Generate a file at `content/code-data/[slug].html` using the schema in `content/code-data/_template.html`. Details:
>
> - **Name:** [tool/dataset name]
> - **Subtype:** dataset | code
> - **What it does:** [1-2 sentences]
> - **Year:** [YYYY]
> - **Version:** [optional]
> - **License:** [MIT / CC-BY / etc.]
> - **Themes:** [from allowed list]
> - **Sections:** resources | impact-public-good (or both)
> - **GitHub URL:** [optional]
> - **Download URL:** [optional]

### Adding a talk

> Generate a file at `content/talks/[slug].html` using the schema in `content/talks/_template.html`. Details:
>
> - **Title:** ...
> - **Venue:** ...
> - **Year + Date:** ...
> - **Location:** [City, Country]
> - **Type:** keynote | plenary | paper | discussant | panel | workshop
> - **Co-authors:** [if any]
> - **Slides / Video URLs:** [optional]
> - **One-line description:** ...

### Adding a briefing

> Generate a file at `content/briefings/[slug].html`. Details:
>
> - **Title:** ...
> - **Audience:** [county board / agency name]
> - **Year + Date:** ...
> - **PDF URL:** [optional]
> - **One-line description:** ...

### Adding a course

> Generate a file at `content/teaching/[slug].html`. Details:
>
> - **Course title:** ...
> - **Course code:** [e.g. PA 856]
> - **Institution:** UW–Madison
> - **Term:** Spring 2026
> - **Role:** taught | co-taught | TA
> - **Syllabus URL:** [optional]
> - **One-line description:** ...

---

## Where each content type ends up

| Content type | Where it appears on the site |
|---|---|
| Publication (`pub:sections=livability`) | livability.html pub list + auto page at papers/<slug>.html |
| Code/data (`code:sections=resources`) | resources.html Datasets / Code section |
| Code/data (`code:sections=impact-public-good`) | impact/public-good.html record list |
| Talk (`talk:sections=impact-talks`) | impact/talks.html record list |
| Briefing (`brief:sections=impact-briefings`) | impact/policy-briefings.html record list |
| Course (`teach:sections=impact-teaching`) | impact/teaching.html record list |

You can list multiple sections in one entry — e.g. `pub:sections="livability,workforce"` puts a paper on BOTH theme pages.

---

## When build.py runs

```
$ python3 build.py
Scanning content/...
  publications:  9 found
  code-data:     2 found
  talks:         0 found
  briefings:     1 found
  teaching:      0 found
  posts:         1 found
✓ injected into 7 pages
```

If you see warnings, it usually means a typo in a meta value (an unknown theme or section). Fix the file and re-run.
