#!/usr/bin/env python3
"""Generate the static GitHub Pages site from works.json.

Run `python3 build_site.py` after editing works.json or the collections below,
then commit the regenerated HTML files.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = 'elsieambrose66@gmail.com'

COLLECTIONS = [
    {'slug': 'paintings', 'title': 'Paintings', 'cover': 'plate-037.jpeg',
     'plates': ['016', '004', '015', '026', '013', '017', '028']},
    {'slug': 'drawings', 'title': 'Drawings', 'cover': 'plate-055.jpeg',
     'plates': ['027', '005', '001', '002', '006', '007', '008', '009', '010',
                '011', '012', '018', '019', '020', '021', '022', '023', '024']},
    {'slug': 'sculptures', 'title': 'Sculptures', 'cover': 'plate-002.jpeg',
     'plates': ['003', '014', '025']},
]

works = {w['plate']: w for w in json.loads((ROOT / 'works.json').read_text())}
esc = html.escape


def items_for(collection):
    items = []
    for plate in collection['plates']:
        work = works[plate]
        total = len(work['images'])
        for view, image in enumerate(work['images'], 1):
            items.append({
                'src': Path(image['src']).name,
                'width': image['width'],
                'height': image['height'],
                'title': work['title'],
                'description': work['description'],
                'view': view,
                'totalViews': total,
            })
    return items


def page(path, title, body, depth):
    r = '../' * depth or './'
    out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="Paintings, drawings, and sculptures by Elsie Ambrose, New York.">
<link rel="stylesheet" href="{r}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="{r}">Elsie Ambrose</a><nav aria-label="Main navigation"><a href="{r}">Home</a><a href="{r}artwork/">Artwork</a><a href="{r}contact/">Contact</a><a href="{r}cv/">CV</a></nav></header>
<main id="main">{body}</main>
<footer><a href="mailto:{EMAIL}">{EMAIL}</a><span>New York, NY</span></footer>
</body>
</html>
'''
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out)


def caption_note(item):
    views = f' · View {item["view"]} of {item["totalViews"]}' if item['totalViews'] > 1 else ''
    return 'Provisional title' + views


def build():
    page('index.html', 'Elsie Ambrose — Artist',
         '<section class="home"><h1 class="sr-only">Elsie Ambrose</h1>'
         '<img class="home-art" src="artwork/cloudscape.jpeg" '
         'alt="Elsie Ambrose’s painting of turbulent clouds and shafts of light" '
         'width="2474" height="1536" fetchpriority="high"></section>', 0)

    covers = []
    for c in COLLECTIONS:
        cover = next(i for i in items_for(c) if i['src'] == c['cover'])
        covers.append(
            f'<a href="{c["slug"]}/" class="collection-cover"><div class="cover-image">'
            f'<img src="{cover["src"]}" width="{cover["width"]}" height="{cover["height"]}" '
            f'alt="{esc(cover["description"])}"></div><h2>{esc(c["title"])}</h2></a>')
    page('artwork/index.html', 'Artwork — Elsie Ambrose',
         '<section class="artwork-index"><h1 class="sr-only">Artwork</h1>'
         f'<div class="collection-grid">{"".join(covers)}</div></section>', 1)

    for c in COLLECTIONS:
        items = items_for(c)
        first = items[0]
        n = len(items)
        thumbs = ''.join(
            f'<button type="button" class="art-thumbnail{" is-selected" if i == 0 else ""}" '
            f'data-index="{i}" aria-pressed="{"true" if i == 0 else "false"}" '
            f'aria-label="{esc(it["title"])}{", view " + str(it["view"]) if it["totalViews"] > 1 else ""}">'
            f'<img src="../{it["src"]}" width="{it["width"]}" height="{it["height"]}" alt="" loading="lazy">'
            f'<span>{i + 1:02d}</span></button>'
            for i, it in enumerate(items))
        data = json.dumps(items, ensure_ascii=False).replace('</', '<\\/')
        body = (
            '<section class="collection-page" data-viewer>'
            f'<div class="collection-heading"><a class="label" href="../">All artwork</a><h1>{esc(c["title"])}</h1></div>'
            f'<div class="large-artwork"><img class="collection-art" src="../{first["src"]}" '
            f'width="{first["width"]}" height="{first["height"]}" alt="{esc(first["description"])}"></div>'
            '<div class="painting-caption"><div aria-live="polite" aria-atomic="true">'
            f'<h2 data-title>{esc(first["title"])}</h2><p data-description>{esc(first["description"])}</p>'
            f'<span class="caption-note" data-note>{esc(caption_note(first))}</span></div>'
            '<div class="sequence-controls">'
            '<button type="button" aria-label="Previous artwork" data-prev disabled>Previous</button>'
            f'<span data-counter>01 / {n:02d}</span>'
            f'<button type="button" aria-label="Next artwork" data-next{" disabled" if n == 1 else ""}>Next</button>'
            '</div></div>'
            f'<fieldset class="thumbnail-row" aria-label="Choose an artwork">{thumbs}</fieldset>'
            f'<script type="application/json" data-items>{data}</script>'
            '</section><script src="../../assets/viewer.js"></script>')
        page(f'artwork/{c["slug"]}/index.html', f'{c["title"]} — Elsie Ambrose', body, 2)

    page('contact/index.html', 'Contact — Elsie Ambrose',
         '<section class="contact-page"><h1 class="sr-only">Contact</h1>'
         '<p>For exhibitions, commissions, and collaborations:</p>'
         f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
         '<a href="https://www.instagram.com/elsieambrose/" target="_blank" rel="noopener noreferrer">'
         'Instagram / @elsieambrose</a></section>', 1)

    page('cv/index.html', 'CV — Elsie Ambrose',
         '<section class="cv-page"><h1>CV</h1>'
         '<p class="cv-empty">Curriculum vitae forthcoming.</p></section>', 1)


if __name__ == '__main__':
    build()
