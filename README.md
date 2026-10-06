# Elsie Ambrose

Portfolio site, served as plain static files by GitHub Pages.

- `artwork.json` — each section's works in display order: title, year, medium,
  size and image files, plus the section cover
- `build_site.py` — regenerates the HTML pages and cropped images (crop boxes are
  at the top; needs `pip install pillow`)
- `cv.json` — CV sections and entries shown on the CV page (`"italicTitles": true`
  italicizes each entry's text before the first comma)
- `artwork/` — images; `assets/` — stylesheet and gallery script

After editing `artwork.json` or `build_site.py`, run `python3 build_site.py` and
commit the result. Every push to `main` deploys via `.github/workflows/static.yml`.
