#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "images"
OUTPUT = ROOT / "images-manifest.json"
VALID_EXTENSIONS = {".webp"}


def build_manifest() -> dict[str, list[str]]:
    manifest: dict[str, list[str]] = {}

    if not IMAGES_DIR.exists():
        return manifest

    for folder in sorted(path for path in IMAGES_DIR.iterdir() if path.is_dir()):
        images = sorted(
            f"/images/{folder.name}/{file.name}"
            for file in folder.iterdir()
            if file.is_file() and file.suffix.lower() in VALID_EXTENSIONS
        )
        manifest[folder.name] = images

    return manifest


def main() -> None:
    manifest = build_manifest()
    OUTPUT.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    total = sum(len(images) for images in manifest.values())
    print(f"Wrote {OUTPUT.name} with {len(manifest)} folders and {total} images.")


if __name__ == "__main__":
    main()
