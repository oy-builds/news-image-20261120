[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/oy-builds/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/oy-builds/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — 20 November 2026

An entry for make.fun bounty `news-image-20261120` — *Sum up 20 November's
world news in one image*.

The entry is a finished picture plus the tiny program that delivers it:

- **`entry.png`** — the image itself: 1024×1024 PNG, dark-navy infographic
  with an unmissable `20 NOVEMBER 2026` masthead and six story blocks
  (coloured accent bar, category label, large headline, one factual line),
  drawn by `generate_image.py` from the sourced stories in
  `data/stories.json`.
- **`main.ts`** — the entry program (Node 22, standard library only). It
  copies `entry.png` to the output folder, so both grading runs produce
  byte-identical files.

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png   (in the grader's container: /output/entry.png)
```

No dependencies, no network, no build step.

## Image specs (the kit's gate)

| | |
|---|---|
| Format | PNG (whole file, judged byte for byte) |
| Size | 1024×1024 px — the maximum allowed is 1024×1024 |
| File size | under 1 MiB (see `node smoke.test.mjs` output for the exact bytes) |
| Determinism | `main.ts` copies the stored PNG; two runs are byte-identical (sha256-checked in the smoke test) |

## How the image answers the judge's criteria

1. **Names the day, shows that day's events** — the date fills the masthead;
   every story happened or was first reported on 20 November 2026.
2. **Breadth** — conflict (Europe), justice (The Hague), diplomacy
   (Brussels), markets (global), disaster (Peru), society (UN).
3. **Readable alone, legible at ~300 px** — headlines are short, set large
   (30–42 px bold at full size), one supporting line each, no body copy.
4. **Faithful** — every story is taken from the sources in
   `data/stories.json` as they reported it on the day; figures (S&P 500
   −3.7%, Nikkei −5.06%, magnitude 6.7) are as reported and may be revised.
5. **Clean craft** — one flat, code-drawn composition; text is rendered by
   PIL from real strings, so nothing is garbled.

## The six stories

Display headlines are shortened for legibility; the full sourced versions
live in [`data/stories.json`](data/stories.json), each with its source URLs.

1. **RUSSIA HITS KYIV — MISSILES LAND IN POLAND** — One Turn News; Open Chronicle
2. **WORLD COURT: MYANMAR GENOCIDE RULING** — One Turn News; Open Chronicle; Hansen Intel (PBS)
3. **UK–EU SEAL BREXIT-RESET DEAL** — One Turn News; Open Chronicle; Hansen Intel (Guardian)
4. **AI SELL-OFF SHAKES WORLD MARKETS** — One Turn News (S&P 500 −3.7%, Nikkei −5.06%, as reported)
5. **6.7 QUAKE HITS CENTRAL PERU** — One Turn News
6. **WORLD CHILDREN'S DAY: UN WARNING** — UN News Today, 20 Nov 2026

Footer on the image: *Sources: UN News · One Turn News · Open Chronicle ·
Hansen Intel — as reported 20 Nov 2026.*

## Regenerating the image

```bash
python3 generate_image.py   # Python + PIL, DejaVu fonts; rewrites entry.png
```

Edit `data/stories.json` (or the shortened display text in
`generate_image.py`) and re-run. The generator asserts the output is
1024×1024 and ≤ 1 MiB.

## Test

```bash
node smoke.test.mjs
```

Checks: `main.ts` + `entry.png` at root, PNG magic bytes, IHDR dimensions
≤ 1024×1024, size ≤ 1 MiB, two `main.ts` runs byte-identical (sha256), and
no network calls in `main.ts`.

## Files

| File | What it is |
|---|---|
| `main.ts` | Entry program — copies `entry.png` to the output dir |
| `entry.png` | The judged image (1024×1024) |
| `generate_image.py` | The PIL drawing program that made `entry.png` |
| `data/stories.json` | The day's six stories + per-story sources (also copied as `stories.json`) |
| `smoke.test.mjs` | Local gate / determinism checks |
| `LICENSE` | MIT |
| `.makefun/owner.json` | make.fun claim file for this repository |

All artwork is original and drawn in code. No photos, logos, or third-party
assets.

## make.fun

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)

_Badge / link placeholder for the `news-image-20261120` bounty._
