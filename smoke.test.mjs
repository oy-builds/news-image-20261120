// Smoke test: runs the program, checks the SVG output, headlines, and offline purity.
// Run: node smoke.test.mjs
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
let pass = 0, fail = 0;
const check = (name, ok) => { console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}`); ok ? pass++ : fail++; };

execFileSync(process.execPath, [join(root, 'main.mjs')], { stdio: 'pipe' });
check('program runs (node main.mjs)', true);

const data = JSON.parse(readFileSync(join(root, 'data', 'stories.json'), 'utf8'));
const outFile = join(root, 'out', `news-${data.date}.svg`);
check('output file exists', existsSync(outFile));

const svg = readFileSync(outFile, 'utf8');
check('output is an SVG document', svg.trimStart().startsWith('<svg') && svg.includes('</svg>'));
check('canvas is 1600x1200', svg.includes('viewBox="0 0 1600 1200"'));

// Normalise rendered text: decode XML entities, strip tags, collapse spaces.
const textOnly = svg.replace(/&apos;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<')
  .replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
for (const s of data.stories) {
  check(`headline present: ${s.id}`, textOnly.includes(s.headline.replace(/\s+/g, ' ')));
}
check('date label present', textOnly.includes('20 NOVEMBER 2026'));
check('footer sources present', textOnly.includes('UN News'));

const main = readFileSync(join(root, 'main.mjs'), 'utf8');
check('no fetch in main.mjs', !main.includes('fetch('));
// The SVG xmlns identifier is a namespace name, not a network call — exclude it.
check('no http/https URLs in main.mjs (xmlns aside)', !/https?:\/\//.test(main.replace('http://www.w3.org/2000/svg', '')));
check('no network imports in main.mjs', !/node:(http|https|net|dgram)/.test(main));
check('no external image references in SVG', !svg.includes('<image'));

console.log(`\n${fail === 0 ? 'All smoke tests passed.' : fail + ' check(s) FAILED'} (${pass} passed)`);
process.exit(fail === 0 ? 0 : 1);
