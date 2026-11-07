// Static files (index.html, track.mp3) are served as assets before this runs.
// Images come from R2: keys are "<folder>/<file>.webp".

const FOLDER_PATTERN = /^[a-z0-9_-]+$/i;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // List image URLs for one folder, e.g. /api/images?folder=foster
    if (url.pathname === "/api/images") {
      const folder = url.searchParams.get("folder") ?? "";
      if (!FOLDER_PATTERN.test(folder)) {
        return Response.json({ error: "invalid folder" }, { status: 400 });
      }

      const images: string[] = [];
      let cursor: string | undefined;
      do {
        const page = await env.IMAGES.list({ prefix: `${folder}/`, cursor });
        images.push(...page.objects.map((object) => `/images/${object.key}`));
        cursor = page.truncated ? page.cursor : undefined;
      } while (cursor);

      return Response.json(images.sort(), {
        headers: { "cache-control": "public, max-age=60" },
      });
    }

    // Serve an image, e.g. /images/foster/IMG_1229.webp
    if (url.pathname.startsWith("/images/")) {
      const key = decodeURIComponent(url.pathname.slice("/images/".length));
      const object = await env.IMAGES.get(key);
      if (!object) {
        return new Response("Not found", { status: 404 });
      }

      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("etag", object.httpEtag);
      headers.set("cache-control", "public, max-age=86400");
      return new Response(object.body, { headers });
    }

    return new Response("Not found", { status: 404 });
  },
} satisfies ExportedHandler<{ IMAGES: R2Bucket }>;
