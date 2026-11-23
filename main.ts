// The World in One Day - entry program for make.fun's news-image-20261123 bounty.
// Written for this entry: it delivers the poster that sits beside it in this
// repository to the grader's output directory, and sanity-checks the file on
// the way so a truncated copy can never be judged as our image.

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const posterPath = new URL('./entry.png', import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const destination = join(outputDir, 'entry.png');

mkdirSync(outputDir, { recursive: true });
copyFileSync(posterPath, destination);

const posterBytes = statSync(posterPath).size;
const deliveredBytes = statSync(destination).size;
if (deliveredBytes !== posterBytes) {
  throw new Error(`poster copy mismatch: ${deliveredBytes} of ${posterBytes} bytes delivered`);
}
console.log(`entry.png delivered to ${destination} (${deliveredBytes} bytes)`);
