#!/usr/bin/env python3
"""
build.py — Template-driven content generator for the Yang Cheng website.

Scans `posts/` and every `content/<type>/` folder, reads metadata from each
file's <head>, and injects rendered HTML into marker comments across the site.

USAGE
─────
From the project root (the folder containing this file):

    python3 build.py

WHAT IT HANDLES
───────────────
1. posts/*.html             → resources.html (grid + sections)
2. content/publications/    → research/{livability,workforce,migration}.html · resources.html
3. content/code-data/       → resources.html (datasets/code sections + grid) · impact/public-good.html
4. content/talks/           → impact/talks.html (when implemented)
5. content/briefings/       → impact/policy-briefings.html (when implemented)
6. content/teaching/        → impact/teaching.html (when implemented)

Each file's metadata is in <meta name="ns:field" content="value"> tags
(`pub:` for publications, `code:` for code-data, etc.).

See content/README.md for full schemas.
"""

from __future__ import annotations
import os, re, sys, glob

# ─── Constants ────────────────────────────────────────────────────────────────
RESOURCES_FILE  = 'resources.html'
TEMPLATE_NAMES  = {'_template-post.html', '_template.html'}
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

THUMB_CLASS = {
    'ai': 't-ai', 'datasci': 't-datasci', 'rural': 't-rural',
    'qol': 't-qol', 'green': 't-green', 'housing': 't-housing', 'health': 't-health',
}
THEME_LABEL = {
    'ai': 'AI', 'datasci': 'Data Science', 'rural': 'Rural Livability',
    'qol': 'Quality of Life', 'green': 'Green Economy', 'housing': 'Housing', 'health': 'Health',
}
POST_TYPE_LABEL = {
    'tutorial': 'Tutorial', 'post': 'Post', 'news': 'News', 'paper': 'Paper', 'event': 'Event',
}
PUB_TYPE_LABEL = {
    'article': 'Article', 'working-paper': 'Working paper',
    'book-chapter': 'Book chapter', 'dissertation': 'Dissertation', 'report': 'Report',
}
PUB_STATUS_LABEL = {
    'published': 'Published', 'in-revision': 'In revision',
    'in-progress': 'In progress', 'drafted': 'Drafted',
}


# ─── Helpers ──────────────────────────────────────────────────────────────────
def fmt_date(yyyymmdd: str) -> str:
    try:
        y, m, d = yyyymmdd.split('-')
        return f'{MONTHS[int(m)-1]} {int(d):02d}, {y}'
    except Exception:
        return yyyymmdd


def first_thumb(themes_str: str) -> str:
    """Pick the first theme's thumb class."""
    for t in themes_str.split():
        if t in THUMB_CLASS:
            return THUMB_CLASS[t]
    return 't-rural'


def first_theme_label(themes_str: str) -> str:
    for t in themes_str.split():
        if t in THEME_LABEL:
            return THEME_LABEL[t]
    return themes_str.split()[0] if themes_str.split() else ''


def normalize_section(sec: str) -> str:
    """Map legacy sub-section keys (livability-A, workforce-B, ...) to the theme key.
    July 2026 simplification: each theme page shows ONE flat publication list."""
    for theme in ('livability', 'workforce', 'migration'):
        if sec == theme or sec.startswith(theme + '-'):
            return theme
    return sec


def parse_file(path: str, ns: str) -> dict | None:
    """Read meta tags + body content from an HTML file. ns is the metadata namespace ('pub', 'code', etc.)."""
    with open(path) as f:
        html = f.read()

    meta = {}
    for m in re.finditer(r'<meta\s+name="' + ns + r':([^"]+)"\s+content="([^"]*)"', html):
        meta[m.group(1)] = m.group(2)

    # Body content (after <body>, before </body>) — used for abstracts/descriptions
    body_m = re.search(r'<body>\s*(.*?)\s*</body>', html, re.DOTALL)
    body = body_m.group(1).strip() if body_m else ''

    if not meta:
        return None
    return {'path': path, 'meta': meta, 'body': body}


def load_files(folder: str, ns: str) -> list[dict]:
    """Load all files in a folder (skipping templates), return parsed entries."""
    if not os.path.isdir(folder):
        return []
    out = []
    for path in sorted(glob.glob(f'{folder}/*.html')):
        if os.path.basename(path) in TEMPLATE_NAMES:
            continue
        item = parse_file(path, ns)
        if item:
            out.append(item)
    return out


def replace_marker(html: str, marker_label: str, body_html: str) -> str:
    """Replace content between <!-- AUTO-GENERATED {label} START ... --> and END markers."""
    # The START marker may have a trailing comment (like "· run python3 build.py …")
    pattern = re.compile(
        r'(<!-- AUTO-GENERATED ' + re.escape(marker_label) + r' START[^>]*-->)'
        r'\s*?\n?'
        r'(?:.*?)'
        r'\n?\s*?'
        r'(<!-- AUTO-GENERATED ' + re.escape(marker_label) + r' END -->)',
        re.DOTALL
    )
    if not pattern.search(html):
        print(f'  ⚠ marker not found: {marker_label}')
        return html
    indent = '        '  # most markers sit at this depth
    body = ('\n' + body_html.rstrip() + '\n' + indent) if body_html else '\n' + indent
    replacement = lambda m: m.group(1) + body + m.group(2)
    return pattern.sub(replacement, html, count=1)


def write_if_changed(path: str, new_content: str) -> bool:
    with open(path) as f:
        old = f.read()
    if old == new_content:
        return False
    with open(path, 'w') as f:
        f.write(new_content)
    return True


# ─── Generators: posts ───────────────────────────────────────────────────────
def gen_post_grid_card(p: dict) -> str:
    m = p['meta']
    type_lbl = POST_TYPE_LABEL.get(m.get('type', ''), m.get('type', ''))
    theme_lbl = THEME_LABEL.get(m.get('theme', ''), m.get('theme', ''))
    thumb = THUMB_CLASS.get(m.get('theme', ''), 't-rural')
    title_m = re.search(r'<title>\s*(.*?)\s*(?:—\s*Yang Cheng)?\s*</title>', open(p['path']).read())
    title = title_m.group(1).strip() if title_m else m.get('title', '')
    return (
        f'      <a class="post-card" href="{p["path"]}" data-type="{m.get("type", "")}" data-theme="{m.get("theme", "")}">\n'
        f'        <div class="pc-thumb thumb {thumb}"></div>\n'
        f'        <div class="pc-tags"><span class="pc-chip pc-type">{type_lbl}</span><span class="pc-chip">{theme_lbl}</span></div>\n'
        f'        <h3>{title}</h3>\n'
        f'        <p class="pc-desc">{m.get("description", "")}</p>\n'
        f'        <div class="pc-date">{fmt_date(m.get("date", ""))}</div>\n'
        f'      </a>'
    )


def gen_post_section_row(p: dict) -> str:
    m = p['meta']
    type_lbl = POST_TYPE_LABEL.get(m.get('type', ''), m.get('type', ''))
    theme_lbl = THEME_LABEL.get(m.get('theme', ''), m.get('theme', ''))
    title_m = re.search(r'<title>\s*(.*?)\s*(?:—\s*Yang Cheng)?\s*</title>', open(p['path']).read())
    title = title_m.group(1).strip() if title_m else m.get('title', '')
    return (
        f'        <a class="record-row" href="{p["path"]}" data-type="{m.get("type", "")}" data-theme="{m.get("theme", "")}">'
        f'<span class="rr-date">{fmt_date(m.get("date", ""))}</span>'
        f'<h4>{title}</h4>'
        f'<span class="rr-venue">{theme_lbl} · {type_lbl}</span>'
        f'<span class="rr-arrow">Read →</span></a>'
    )


# ─── Generators: publications ────────────────────────────────────────────────
def apa_authors(authors: str) -> str:
    """'Yang Cheng, Tessa Conroy & Steven Deller' → 'Cheng, Y., Conroy, T., & Deller, S.'"""
    authors = re.sub(r'\s*\([^)]*\)', '', authors)  # drop parentheticals like '(advisor: ...)'
    names = [n.strip() for n in re.split(r',|&', authors) if n.strip()]
    out = []
    for n in names:
        parts = n.split()
        if len(parts) == 1:
            out.append(parts[0])
            continue
        family = parts[-1]
        initials = ' '.join(p[0] + '.' for p in parts[:-1])
        out.append(f'{family}, {initials}')
    if len(out) > 1:
        return ', '.join(out[:-1]) + ', & ' + out[-1]
    return out[0] if out else ''


def apa_citation(m: dict) -> str:
    """APA-style one-liner for the Cite button. pub:cite (non-URL) overrides the generated text."""
    custom = m.get('cite', '').strip()
    if custom and not custom.startswith('http'):
        apa = custom
    else:
        venue_plain = re.sub(r'<[^>]+>', '', m.get('venue', ''))
        doi = m.get('doi', '').strip()
        if doi and not doi.startswith('http'):
            doi = 'https://doi.org/' + doi
        title = m.get('title', '').rstrip()
        title_sep = '' if title.endswith('.') else '.'  # avoid ".." after titles ending in "U.S." etc.
        apa = f"{apa_authors(m.get('authors', ''))} ({m.get('year', '')}). {title}{title_sep} {venue_plain}."
        if doi:
            apa += f' {doi}'
    return apa.replace('&', '&amp;').replace('"', '&quot;')


def gen_pub_full_block(p: dict) -> str:
    """Render a paper as a <div class="pub-full"> for theme pages."""
    m = p['meta']
    title    = m.get('title', '')
    authors  = m.get('authors', '')
    venue    = m.get('venue', '')
    year     = m.get('year', '')
    status   = PUB_STATUS_LABEL.get(m.get('status', ''), m.get('status', ''))
    type_lbl = PUB_TYPE_LABEL.get(m.get('type', ''), m.get('type', ''))
    abstract = p['body']  # whatever's in <body>, typically a <div class="abstract"><p>...</p></div>
    abstract_text = re.sub(r'<[^>]+>', '', abstract).strip()  # plaintext fallback
    abstract_html = re.search(r'<div class="abstract">\s*(.*?)\s*</div>', abstract, re.DOTALL)
    abstract_inner = abstract_html.group(1).strip() if abstract_html else f'<p>{abstract_text}</p>'

    keywords = ' '.join(f'<span>{t}</span>' for t in m.get('themes', '').split())

    links = []
    for label, key in [('Slides', 'slides'), ('DOI', 'doi')]:
        url = m.get(key, '').strip()
        if key == 'doi' and url and not url.startswith('http'):
            url = 'https://doi.org/' + url
        if url:
            links.append(f'<a href="{url}" target="_blank" rel="noopener">{label}</a>')
        else:
            links.append(f'<a href="#">{label}</a>')
    # Repo: one button for code/data (pub:code, falling back to pub:data)
    repo = m.get('code', '').strip() or m.get('data', '').strip()
    if repo:
        links.append(f'<a href="{repo}" target="_blank" rel="noopener">Repo</a>')
    else:
        links.append('<a href="#">Repo</a>')
    # Cite always works: copies an APA citation to the clipboard (JS in research/index.html)
    links.append(f'<a href="#cite" class="pf-cite" data-cite="{apa_citation(m)}">Cite</a>')
    links_html = '\n            '.join(links)

    return (
        f'      <div class="pub-full">\n'
        f'        <div class="pf-row">\n'
        f'        <div class="pf-year">{year}<small>{type_lbl}</small></div>\n'
        f'        <h3>{title}</h3>\n'
        f'        <div class="pf-meta">\n'
        f'          <div class="pf-authors">{authors}</div>\n'
        f'          <div class="pf-venue">{venue}.</div>\n'
        f'        </div>\n'
        f'        <div class="pf-links">\n'
        f'            {links_html}\n'
        f'        </div>\n'
        f'        <div class="pf-toggle">›</div>\n'
        f'        </div>\n'
        f'        <div class="pf-abstract"><div class="pf-abstract-inner">\n'
        f'          {abstract_inner}\n'
        f'          <div class="pf-keywords">{keywords}</div>\n'
        f'        </div></div>\n'
        f'      </div>'
    )


def gen_pub_grid_card(p: dict) -> str:
    """Render a paper as a post-card for resources.html grid view."""
    m = p['meta']
    title    = m.get('title', '')
    venue    = m.get('venue', '')
    year     = m.get('year', '')
    abstract = p['body']
    desc_m = re.search(r'<p>(.*?)</p>', abstract, re.DOTALL)
    desc = desc_m.group(1).strip() if desc_m else ''
    # Truncate long abstracts for the card
    if len(desc) > 240:
        desc = desc[:237] + '...'

    themes = m.get('themes', '')
    primary_theme = themes.split()[0] if themes.split() else 'rural'
    thumb = THUMB_CLASS.get(primary_theme, 't-rural')
    theme_lbl = THEME_LABEL.get(primary_theme, primary_theme)

    return (
        f'      <a class="post-card" href="#" data-type="paper" data-theme="{primary_theme}">\n'
        f'        <div class="pc-thumb thumb {thumb}"></div>\n'
        f'        <div class="pc-tags"><span class="pc-chip pc-type">Paper</span><span class="pc-chip">{theme_lbl}</span></div>\n'
        f'        <h3>{title}</h3>\n'
        f'        <p class="pc-desc">{desc}</p>\n'
        f'        <div class="pc-date">{venue}</div>\n'
        f'      </a>'
    )


def gen_pub_section_row(p: dict) -> str:
    """Render a paper as a record-row for resources.html sections view."""
    m = p['meta']
    title    = m.get('title', '')
    authors  = m.get('authors', '')
    venue    = m.get('venue', '')
    year     = m.get('year', '')
    status   = PUB_STATUS_LABEL.get(m.get('status', ''), m.get('status', ''))
    themes = m.get('themes', '')
    primary_theme = themes.split()[0] if themes.split() else 'rural'
    return (
        f'        <a class="record-row" href="#" data-type="paper" data-theme="{primary_theme}">'
        f'<span class="rr-date">{venue.split(",")[0] if "," in venue else venue} · {year}</span>'
        f'<h4>{title}</h4>'
        f'<span class="rr-venue">{authors}</span>'
        f'<span class="rr-arrow">PDF →</span></a>'
    )


# ─── Generators: code-data ───────────────────────────────────────────────────
def gen_code_grid_card(c: dict) -> str:
    m = c['meta']
    title = m.get('title', '')
    subtype = m.get('subtype', 'code')
    type_lbl = 'Code' if subtype == 'code' else 'Dataset'
    desc_m = re.search(r'<p>(.*?)</p>', c['body'], re.DOTALL)
    desc = desc_m.group(1).strip() if desc_m else ''
    themes = m.get('themes', '')
    primary_theme = themes.split()[0] if themes.split() else 'rural'
    thumb = THUMB_CLASS.get(primary_theme, 't-rural')
    theme_lbl = THEME_LABEL.get(primary_theme, primary_theme)
    href = m.get('github_url') or m.get('download_url') or '#'
    target = ' target="_blank" rel="noopener"' if href != '#' else ''
    version_year = f'{m.get("version", "")} · {m.get("year", "")}'.strip(' ·')

    return (
        f'      <a class="post-card" href="{href}"{target} data-type="{subtype}" data-theme="{primary_theme}">\n'
        f'        <div class="pc-thumb thumb {thumb}"></div>\n'
        f'        <div class="pc-tags"><span class="pc-chip pc-type">{type_lbl}</span><span class="pc-chip">{theme_lbl}</span></div>\n'
        f'        <h3>{title}</h3>\n'
        f'        <p class="pc-desc">{desc}</p>\n'
        f'        <div class="pc-date">{version_year}</div>\n'
        f'      </a>'
    )


def gen_code_section_row(c: dict) -> str:
    m = c['meta']
    title = m.get('title', '')
    subtype = m.get('subtype', 'code')
    desc_m = re.search(r'<p>(.*?)</p>', c['body'], re.DOTALL)
    desc = desc_m.group(1).strip() if desc_m else ''
    themes = m.get('themes', '')
    primary_theme = themes.split()[0] if themes.split() else 'rural'
    theme_lbl = THEME_LABEL.get(primary_theme, primary_theme)
    href = m.get('github_url') or m.get('download_url') or '#'
    target = ' target="_blank" rel="noopener"' if href != '#' else ''
    arrow = 'GitHub →' if 'github' in href else ('Download →' if href != '#' else 'Link →')
    version_year = f'{m.get("version", "")} · {m.get("year", "")}'.strip(' ·')

    return (
        f'        <a class="record-row" href="{href}"{target} data-type="{subtype}" data-theme="{primary_theme}">'
        f'<span class="rr-date">{version_year}</span>'
        f'<h4>{title}</h4>'
        f'<span class="rr-venue">{theme_lbl} · {desc[:60]}{"..." if len(desc) > 60 else ""}</span>'
        f'<span class="rr-arrow">{arrow}</span></a>'
    )


# ─── Inject: theme pages (livability / workforce / migration) ────────────────
def inject_publications_to_theme_pages(pubs: list[dict]):
    by_section: dict[str, list[dict]] = {}
    for p in pubs:
        for sec in p['meta'].get('sections', '').split(','):
            sec = normalize_section(sec.strip())
            if sec and p not in by_section.setdefault(sec, []):
                by_section[sec].append(p)

    # Sort each section: explicit pub:order first (ascending), then year desc
    for sec in by_section:
        by_section[sec].sort(key=lambda p: p['meta'].get('year', ''), reverse=True)
        by_section[sec].sort(key=lambda p: (0, int(p['meta']['order'])) if p['meta'].get('order', '').strip().isdigit() else (1, 0))

    # July 2026: all three lists live on the one-page research/index.html.
    # The old per-theme pages are retired (kept on disk, no longer injected).
    targets = [
        ('research/index.html', ['livability', 'workforce', 'migration']),
        ('index.html', ['livability', 'workforce', 'migration']),
    ]

    for filepath, sections in targets:
        if not os.path.isfile(filepath):
            continue
        with open(filepath) as f:
            html = f.read()
        for sec in sections:
            items = by_section.get(sec, [])
            body = '\n'.join(gen_pub_full_block(p) for p in items)
            # research/ pages live one level down — fix root-relative asset/post links there only
            if filepath.startswith('research/'):
                body = body.replace('href="assets/', 'href="../assets/').replace('href="posts/', 'href="../posts/').replace('href="papers/', 'href="../papers/')
            html = replace_marker(html, f'PUBS:{sec}', body)
        write_if_changed(filepath, html)


# ─── Inject: research overview (publication count per theme card) ───────────
def inject_theme_counts(pubs: list[dict]):
    counts: dict[str, int] = {}
    for p in pubs:
        secs = {normalize_section(s.strip()) for s in p['meta'].get('sections', '').split(',')}
        for t in ('livability', 'workforce', 'migration'):
            if t in secs:
                counts[t] = counts.get(t, 0) + 1
    for path in ('research/index.html', 'index.html'):
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            html = f.read()
        for t in ('livability', 'workforce', 'migration'):
            n = counts.get(t, 0)
            label = (f'{n} publication' + ('s' if n != 1 else '')) if n else 'Lit-review stage'
            html = replace_marker(html, f'PUBCOUNT:{t}', label)
        write_if_changed(path, html)


# ─── Inject: resources.html ──────────────────────────────────────────────────
def inject_into_resources(posts: list[dict], pubs: list[dict], code_data: list[dict]):
    """resources.html = tutorials + posts + datasets + reading lists + CV.
    News-type posts are retired; code-subtype releases live under
    impact/public-good.html (Research Tools, hand-edited)."""
    if not os.path.isfile(RESOURCES_FILE):
        return
    with open(RESOURCES_FILE) as f:
        html = f.read()

    def by_date(items):
        return sorted(items, key=lambda p: p['meta'].get('date', ''), reverse=True)

    tutorials = by_date([p for p in posts if p['meta'].get('type') == 'tutorial'])
    gen_posts = by_date([p for p in posts if p['meta'].get('type') == 'post'])
    datasets = sorted([c for c in code_data
                       if c['meta'].get('subtype') == 'dataset' and 'resources' in c['meta'].get('sections', '')],
                      key=lambda c: c['meta'].get('year', ''), reverse=True)

    # === GRID VIEW: tutorials + posts + datasets ===
    grid = ([gen_post_grid_card(p) for p in tutorials + gen_posts]
            + [gen_code_grid_card(c) for c in datasets])
    html = replace_marker(html, 'RESOURCES GRID', '\n'.join(grid))

    # === SECTIONS VIEW ===
    html = replace_marker(html, 'POSTS SECTION:tutorial', '\n'.join(gen_post_section_row(p) for p in tutorials))
    html = replace_marker(html, 'POSTS SECTION:post', '\n'.join(gen_post_section_row(p) for p in gen_posts))
    html = replace_marker(html, 'DATASET', '\n'.join(gen_code_section_row(c) for c in datasets))
    html = replace_marker(html, 'READING', '')

    write_if_changed(RESOURCES_FILE, html)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    print('Scanning content/ + posts/ ...')
    posts      = load_files('posts',                 'post')
    pubs       = load_files('content/publications',  'pub')
    code_data  = load_files('content/code-data',     'code')
    talks      = load_files('content/talks',         'talk')
    briefings  = load_files('content/briefings',     'brief')
    teaching   = load_files('content/teaching',      'teach')

    print(f'  posts:        {len(posts)}')
    print(f'  publications: {len(pubs)}')
    print(f'  code-data:    {len(code_data)}')
    print(f'  talks:        {len(talks)}')
    print(f'  briefings:    {len(briefings)}')
    print(f'  teaching:     {len(teaching)}')

    print('\nInjecting into theme pages...')
    inject_publications_to_theme_pages(pubs)

    print('Injecting theme pub counts into research/index.html...')
    inject_theme_counts(pubs)

    print('Injecting into resources.html...')
    inject_into_resources(posts, pubs, code_data)

    # Future: inject_talks_to_impact, inject_briefings_to_impact, inject_teaching_to_impact
    # (skipped for now — those impact subpages need markers added first)

    print('\n✓ build complete')


if __name__ == '__main__':
    main()
