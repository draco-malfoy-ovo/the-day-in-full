// Entry for make.fun's "Sum up 26 November's world news in one image".
//
// The picture itself lives beside this file as entry.png: a one-page
// newspaper-style summary of Thursday 26 November 2026, drawn by the
// generator in tools/render.py (see SOURCES.md for the reporting each
// panel is based on). This program's whole job is to deliver those
// bytes, unchanged, to the output directory the grader points at:
//
//   - in the grader's container:  /output/entry.png
//   - anywhere else:              $MAKEFUN_OUTPUT_DIR/entry.png
//
// Copying a fixed file is what makes the run deterministic: two runs
// write byte-identical output, with no clock, randomness or network
// involved. Node 22, standard library only.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const source = new URL("./entry.png", import.meta.url);
const target = join(outDir, "entry.png");
copyFileSync(source, target);

console.log(`entry.png written to ${target} (${statSync(target).size} bytes)`);
