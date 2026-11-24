// The World Today — Tuesday 24 November 2026.
// Dense 45-story broadsheet: 3 illustrated leads, 10 illustrated mediums,
// a 32-item numbered list, a pinned world map, a date-check box, sources.
// This program copies the pre-rendered entry.png to the output directory.
// Deterministic: the same bytes go out on every run, with no network.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
