#!/usr/bin/env python3
"""Generate the static GitHub Pages site from artwork.json.

artwork.json lists each section's works in display order, with title, year,
medium, size and image files (in artwork/). Run `python3 build_site.py` (needs
Pillow) after editing it or the crops below, then commit the regenerated HTML
and cropped images.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
EMAIL = 'elsieambrose66@gmail.com'

COLLECTIONS = json.loads((ROOT / 'artwork.json').read_text())

# Crop boxes as fractions of the original (left, top, right, bottom). Cropped
# copies are written to artwork/cropped/; the originals are left untouched.
CROPS = {
    'plate-057.jpeg': (0.020, 0.010, 0.965, 0.960),
    'plate-022.jpeg': (0.035, 0.035, 0.960, 0.975),
    'plate-023.jpeg': (0.050, 0.055, 0.950, 0.950),
    'plate-027.jpeg': (0.010, 0.005, 0.990, 0.990),
    'plate-025.jpeg': (0.010, 0.008, 0.982, 0.988),
    'plate-026.jpeg': (0.012, 0.010, 0.978, 0.988),
    'plate-028.jpeg': (0.022, 0.016, 0.940, 0.980),
    'plate-042.jpeg': (0.040, 0.035, 0.965, 0.970),
    'plate-043.jpeg': (0.006, 0.004, 0.982, 0.994),
    'plate-044.jpeg': (0.018, 0.014, 0.982, 0.992),
    'plate-017.jpeg': (0.030, 0.040, 0.960, 0.970),
    'plate-034.jpeg': (0.045, 0.035, 0.950, 0.955),
}

esc = html.escape


def crop(name):
    """Write the cropped copy of an image; return (src, width, height)."""
    from PIL import Image
    with Image.open(ROOT / 'artwork' / name) as im:
        W, H = im.size
        l, t, r, b = CROPS[name]
        out = im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
        (ROOT / 'artwork' / 'cropped').mkdir(exist_ok=True)
        out.save(ROOT / 'artwork' / 'cropped' / name, quality=90)
        return 'cropped/' + name, out.width, out.height


def image_info(name):
    """Return (src, width, height) for an image, cropping it if listed in CROPS."""
    if name in CROPS:
        return crop(name)
    from PIL import Image
    with Image.open(ROOT / 'artwork' / name) as im:
        return name, im.width, im.height


def items_for(collection):
    items = []
    for work in collection['works']:
        details = [d for d in (work['year'], work['medium'], work['size']) if d]
        total = len(work['images'])
        for view, name in enumerate(work['images'], 1):
            src, width, height = image_info(name)
            items.append({
                'name': name,
                'src': src,
                'width': width,
                'height': height,
                'title': work['title'],
                'details': details,
                'alt': ', '.join([work['title']] + ([work['medium']] if work['medium'] else [])),
                'note': f'View {view} of {total}' if total > 1 else '',
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


def details_html(item):
    return '<br>'.join(esc(d) for d in item['details'])


def build():
    page('index.html', 'Elsie Ambrose — Artist',
         '<section class="home"><h1 class="sr-only">Elsie Ambrose</h1>'
         '<img class="home-art" src="artwork/cloudscape.jpeg" '
         'alt="Elsie Ambrose’s painting of turbulent clouds and shafts of light" '
         'width="2474" height="1536" fetchpriority="high"></section>', 0)

    covers = []
    for c in COLLECTIONS:
        cover = next(i for i in items_for(c) if i['name'] == c['cover'])
        covers.append(
            f'<a href="{c["slug"]}/" class="collection-cover"><div class="cover-image">'
            f'<img src="{cover["src"]}" width="{cover["width"]}" height="{cover["height"]}" '
            f'alt="{esc(cover["alt"])}"></div><h2>{esc(c["title"])}</h2></a>')
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
            f'width="{first["width"]}" height="{first["height"]}" alt="{esc(first["alt"])}"></div>'
            '<div class="painting-caption"><div aria-live="polite" aria-atomic="true">'
            f'<h2 data-title>{esc(first["title"])}</h2><p data-details>{details_html(first)}</p>'
            f'<span class="caption-note" data-note>{esc(first["note"])}</span></div>'
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
