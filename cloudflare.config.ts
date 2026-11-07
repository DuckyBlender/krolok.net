import { bindings, defineConfig } from "cf/config";

import * as entrypoint from "./src/index.ts" with { type: "cf-worker" };

export default defineConfig({
  worker: {
    name: "krolok-net",
    compatibilityDate: "2026-11-01",
    entrypoint,
    env: {
      IMAGES: bindings.r2({ name: "krolok-net-images", dev: { remote: true } }),
    },
  },
});
