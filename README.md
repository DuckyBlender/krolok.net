# krolok.net

Static pet gallery for Cloudflare Pages. No Lambda, no S3 bucket listing, no backend.

## How it works

- `index.html` is the whole app.
- Images live in `images/<folder>/*.webp`.
- `generate_manifest.py` scans those folders and writes `images-manifest.json`.
- The frontend fetches `images-manifest.json` and renders the selected folder.
- `track.mp3` is loaded locally from the site root.

## Current structure

```text
.
├── index.html
├── generate_manifest.py
├── images-manifest.json
├── track.mp3
└── images/
    ├── batman/
    ├── gamma/
    ├── krolok/
    ├── kudlata/
    └── pajda/
```

## Adding or removing images

1. Put `.webp` files into the correct `images/<folder>/` directory.
2. Run:

```bash
python3 generate_manifest.py
```

3. Deploy the updated files to Cloudflare Pages.

If you add a new folder, the script will include it automatically.

## Local development

Serve the repo as a static site with any simple server. For example:

```bash
python3 -m http.server
```

Then open the local URL and test the gallery.

## Deploying to Cloudflare Pages

- Build command: `python3 generate_manifest.py`
- Build output directory: `.`

That is enough because the site is plain static HTML plus assets.

## Notes

- The preloader only appears on the first visit because `index.html` stores a `visited` flag in `localStorage`.
- If you want to force the preloader again while testing, clear site storage in the browser.
- The social preview image and the preloader image both use `images/krolok/krolok.webp`.
