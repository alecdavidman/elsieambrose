# Elsie Ambrose

Portfolio site, served as plain static files by GitHub Pages.

- `works.json` — titles, descriptions and images for each work
- `build_site.py` — regenerates the HTML pages and cropped images (collection order,
  covers and crop boxes are at the top; needs `pip install pillow`)
- `artwork/` — images; `assets/` — stylesheet and gallery script

After editing `works.json` or `build_site.py`, run `python3 build_site.py` and
commit the result. Every push to `main` deploys via `.github/workflows/static.yml`.
