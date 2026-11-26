[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/draco-malfoy-ovo/the-day-in-full/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/draco-malfoy-ovo/the-day-in-full/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The Day in Full — 26 November 2026 in one image

An entry for make.fun's daily news-image contest
([news-image-20261126](https://make.fun/bounty/news-image-20261126)):
one image that sums up the world news of **Thursday 26 November 2026**.

The image is a newspaper front page: a red date band naming the day, the
tariff story as the lead, six more stories in panels (Cairo, Kyiv, Gaza
and the Red Sea, Brussels, North Korea, SpaceX), and an "Also Thursday"
strip along the bottom. Every story is real reporting from that day —
see [SOURCES.md](SOURCES.md) for the outlets behind each panel.

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies the committed
`entry.png` to the output directory. It runs offline and writes exactly
the same bytes every run.

## How the image was made

`entry.png` was drawn, not photographed: `tools/render.py` renders it
with Pillow from fixed layout code — masthead, panels, and small spot
illustrations drawn from primitives (containers and a % badge for the
tariff lead, a flame for Cairo, a skyline and missile for Kyiv, a ship
for the Red Sea, EU stars, an atom, a satellite). Regenerate it with:

```
python3 tools/render.py
```

The render is deterministic: same code, same fonts, same bytes.
