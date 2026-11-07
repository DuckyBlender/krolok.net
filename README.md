# krolok.net

Pet gallery served by a small Cloudflare Worker. Images live in R2, so adding photos needs no build or deploy.

## How it works

- `index.html` is the whole frontend. `public/track.mp3` is served from the site root.
- Images live in the R2 bucket `krolok-net-images` under `<folder>/<file>.webp`.
- `src/index.ts` is the Worker. It handles two routes:
  - `/api/images?folder=<folder>` lists the images in that folder.
  - `/images/<folder>/<file>.webp` serves an image from R2.
- Everything else (`index.html`, `track.mp3`) is served as static assets.

## Current structure

```text
.
├── index.html
├── public/track.mp3
├── src/index.ts
├── cloudflare.config.ts
└── vite.config.ts
```

Folders in R2: `batman`, `foster`, `krolok`, `kudlata`, `pajda`.

## Adding or removing images

Upload a `.webp` to R2 and it shows up on the next page load:

```bash
cf r2 objects put "<folder>/<file>.webp" --bucket-name krolok-net-images --file path/to/<file>.webp --content-type image/webp
```

Remove one with `cf r2 objects delete "<folder>/<file>.webp" --bucket-name krolok-net-images`.

## Adding a new pet

1. Upload the images to R2 under a new `<folder>/` prefix.
2. Add a nav link in `index.html`: `<a onclick="changePage('<folder>')">Name</a>`.
3. If the folder name doesn't end in "a" but the pet is female, add it to `femaleNames` in `index.html`.
4. Deploy.

## Local development and deploy

```bash
npm install
npm run dev     # cf dev
npm run deploy  # cf deploy
```

## Notes

- The preloader only appears on the first visit because `index.html` stores a `visited` flag in `localStorage`.
- If you want to force the preloader again while testing, clear site storage in the browser.
- The social preview image and the preloader image both use `/images/krolok/krolok.webp` (from R2).
