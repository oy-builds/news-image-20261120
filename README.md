# The World in One Image — 20 November 2026

A Node program that writes **one image** summing up the world news of
**Friday, 20 November 2026**: a 1600×1200 infographic with a dated masthead,
six story panels (headline, one-line summary, and an original icon drawn in
SVG shapes), and a sourced footer.

Built for make.fun bounty `news-image-20261120` — *Sum up 20 November's world
news in one image*.

## Run it

```bash
node main.mjs
# -> out/news-2026-11-20.svg
```

No dependencies, no network calls, no build step. Node builtins only.
Open the SVG in any browser or image viewer, or convert it with your usual
SVG→PNG tool if you need a raster copy. (PNG export is not built in: Node
builtins alone cannot rasterise SVG, and this entry stays dependency-free.)

Test it:

```bash
node smoke.test.mjs
```

## The six stories

All stories are data, in [`data/stories.json`](data/stories.json) — each item
carries its headline, summary, category, place, icon name, accent colour, and
the source(s) it was drawn from, with full URLs:

1. **Russian strikes hit Kyiv — missiles spill into Poland** — One Turn News; Open Chronicle
2. **World Court: Myanmar committed genocide against Rohingya** — One Turn News; Open Chronicle; Hansen Intel (PBS)
3. **Britain and the EU seal a Brexit-reset deal package** — One Turn News; Open Chronicle; Hansen Intel (Guardian)
4. **AI sell-off drags world markets sharply down** — One Turn News (S&P 500 −3.7%, Nikkei −5.06%, as reported)
5. **Magnitude 6.7 earthquake hits central Peru** — One Turn News
6. **On World Children's Day, UN warns of children in crisis** — UN News Today, 20 Nov 2026

Figures are reproduced as the cited sources reported them on the day and may
have been revised since; the image itself carries that note.

## Edit the stories

Edit `data/stories.json` and re-run `node main.mjs`. Fields per story:
`id`, `category`, `place`, `headline`, `summary`, `icon`
(one of `bridge`, `scales`, `flags`, `chart`, `quake`, `sun`),
`accent` (hex colour), and `sources` (`name` + `url`).
The layout takes the first six stories, in a 2×3 grid.

## Files

| File | What it is |
|---|---|
| `main.mjs` | The generator (SVG layout, text wrapping, icons) |
| `data/stories.json` | The day's stories + sources — the editable data |
| `smoke.test.mjs` | Runs the program and checks output, headlines, offline purity |
| `out/news-2026-11-20.svg` | The generated image |

All artwork is original and drawn in code. No photos, logos, or third-party
assets.

## make.fun

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)

_Badge / link placeholder for the `news-image-20261120` bounty._
