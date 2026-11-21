// news-image-20261120 — writes ONE SVG image summing up 20 November 2026 world news.
// Node builtins only. No network calls. Edit data/stories.json to change the stories.
// Run: node main.mjs  ->  out/news-2026-11-20.svg
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const dataPath = existsSync(join(root, 'data', 'stories.json'))
  ? join(root, 'data', 'stories.json')
  : join(root, 'stories.json');
const data = JSON.parse(readFileSync(dataPath, 'utf8'));

const W = 1600, H = 1200;
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&apos;');

// Greedy word wrap by approximate character count.
function wrap(text, maxChars) {
  const words = String(text).split(/\s+/);
  const lines = [];
  let line = '';
  for (const w of words) {
    const next = line ? line + ' ' + w : w;
    if (next.length > maxChars && line) { lines.push(line); line = w; } else line = next;
  }
  if (line) lines.push(line);
  return lines;
}
const tspans = (lines, x, y, dy) =>
  lines.map((l, i) => `<text x="${x}" y="${y + i * dy}" class="t">${esc(l)}</text>`).join('\n');

// ---- Original icons, drawn in SVG shapes only (100x100 local box) ----
function icon(kind, accent) {
  const c = accent;
  switch (kind) {
    case 'bridge': return `<g stroke="${c}" stroke-width="7" fill="none" stroke-linecap="round">
      <path d="M5 78 Q50 20 95 78"/><path d="M5 78 H95"/><path d="M25 62 V78 M50 50 V78 M75 62 V78"/>
      <g fill="${c}" stroke="none"><path d="M78 8 l3 7 7 1 -5 5 1 7 -6-3 -6 3 1-7 -5-5 7-1z"/></g></g>`;
    case 'scales': return `<g stroke="${c}" stroke-width="6" fill="none" stroke-linecap="round">
      <path d="M50 12 V78 M28 84 H72 M50 22 H22 M50 22 H78"/>
      <path d="M22 22 L12 44 M22 22 L32 44 M12 44 Q22 54 32 44"/>
      <path d="M78 22 L68 44 M78 22 L88 44 M68 44 Q78 54 88 44"/></g>`;
    case 'flags': return `<g stroke-linecap="round">
      <rect x="10" y="18" width="36" height="26" rx="4" fill="#2563eb"/>
      <rect x="54" y="18" width="36" height="26" rx="4" fill="${c}"/>
      <g stroke="#fff" stroke-width="5" fill="none"><path d="M28 56 V86 M72 56 V86"/><path d="M28 70 H72"/></g>
      <circle cx="50" cy="70" r="6" fill="#fff"/></g>`;
    case 'chart': return `<g stroke="${c}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M8 14 V90 H92"/><path d="M18 30 L42 46 L58 38 L86 74"/><path d="M86 74 l-14 -2 M86 74 l-1 -14"/></g>`;
    case 'quake': return `<g stroke="${c}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M8 82 L34 40 L50 62 L64 34 L92 82 Z"/>
      <path d="M50 62 l-6 10 10 4 -8 8"/></g>
      <g stroke="${c}" stroke-width="4" fill="none" opacity="0.65"><path d="M14 22 q6 6 0 12 M86 22 q-6 6 0 12"/></g>`;
    case 'sun': return `<g stroke="${c}" stroke-width="6" fill="none" stroke-linecap="round">
      <circle cx="50" cy="42" r="16" fill="${c}" stroke="none"/>
      <path d="M50 12 V20 M50 64 V72 M20 42 H28 M72 42 H80 M29 21 L35 27 M65 57 L71 63 M71 21 L65 27 M35 57 L29 63"/>
      <path d="M18 90 Q34 78 50 90 Q66 102 82 90"/></g>`;
    default: return `<circle cx="50" cy="50" r="30" fill="${accent}"/>`;
  }
}

function panel(story, x, y, w, h, idx) {
  const headLines = wrap(story.headline, 34).slice(0, 3);
  const sumLines = wrap(story.summary, 52).slice(0, 4);
  const headY = y + 118;
  const sumY = headY + headLines.length * 36 + 16;
  return `<g>
  <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="#ffffff" opacity="0.97"/>
  <rect x="${x}" y="${y}" width="${w}" height="10" rx="5" fill="${story.accent}"/>
  <text x="${x + 28}" y="${y + 48}" class="cat" fill="${story.accent}">${esc(story.category)}</text>
  <text x="${x + w - 28}" y="${y + 48}" class="place">${esc(story.place)}</text>
  <g transform="translate(${x + 26},${y + 58}) scale(0.72)">${icon(story.icon, story.accent)}</g>
  <text x="${x + 112}" y="${y + 92}" class="num" fill="${story.accent}">0${idx + 1}</text>
  ${tspans(headLines, x + 28, headY, 36).replaceAll('class="t"', 'class="head"')}
  ${tspans(sumLines, x + 28, sumY, 27)}
</g>`;
}

const panels = data.stories.slice(0, 6).map((s, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  return panel(s, 48 + col * 768, 252 + row * 282, 736, 262, i);
}).join('\n');

const allHeadlines = data.stories.map((s) => s.headline).join(' | ');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img">
<title>${esc(data.title)} — ${esc(data.dateLabel)}</title>
<desc>${esc(allHeadlines)}</desc>
<style>
  .mast{font:900 74px Arial,Helvetica,sans-serif;fill:#fff;letter-spacing:1px}
  .datelab{font:700 30px Arial,Helvetica,sans-serif;fill:#fbbf24;letter-spacing:4px}
  .sub{font:400 27px Arial,Helvetica,sans-serif;fill:#cbd5e1}
  .cat{font:800 21px Arial,Helvetica,sans-serif;letter-spacing:2px}
  .place{font:600 20px Arial,Helvetica,sans-serif;fill:#64748b;text-anchor:end}
  .num{font:900 44px Arial,Helvetica,sans-serif;opacity:0.28}
  .head{font:800 31px Arial,Helvetica,sans-serif;fill:#0f172a}
  .t{font:400 23px Arial,Helvetica,sans-serif;fill:#334155}
  .foot{font:400 19px Arial,Helvetica,sans-serif;fill:#94a3b8}
  .note{font:italic 400 18px Arial,Helvetica,sans-serif;fill:#64748b}
</style>
<rect width="${W}" height="${H}" fill="#0b1220"/>
<rect x="0" y="0" width="${W}" height="216" fill="#12233f"/>
<rect x="0" y="216" width="${W}" height="6" fill="#fbbf24"/>
<circle cx="1480" cy="86" r="52" fill="none" stroke="#fbbf24" stroke-width="5"/>
<circle cx="1480" cy="86" r="34" fill="none" stroke="#38bdf8" stroke-width="4"/>
<path d="M1428 86 H1532 M1480 34 V138" stroke="#475569" stroke-width="3"/>
<text x="48" y="72" class="datelab">${esc(data.dateLabel)}</text>
<text x="48" y="152" class="mast">${esc(data.title)}</text>
<text x="48" y="196" class="sub">${esc(data.subtitle)}</text>
${panels}
<text x="48" y="1136" class="note">${esc(data.note)}</text>
<text x="48" y="1170" class="foot">${esc(data.footerSources)}</text>
</svg>
`;

const outDir = join(root, 'out');
mkdirSync(outDir, { recursive: true });
const outFile = join(outDir, `news-${data.date}.svg`);
writeFileSync(outFile, svg, 'utf8');
console.log(`Wrote ${outFile} (${svg.length} bytes, ${data.stories.length} stories)`);
