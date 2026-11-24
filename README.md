# The World Today — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Moustakimm/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Moustakimm/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Sum up 24 November's world news in one image: a dense 45-story broadsheet —
a giant date masthead, 3 illustrated leads, 10 illustrated medium stories,
a 32-item numbered list, a pinned world map with 13 pins, a date-check box
and a sources line.

## Leads

1. **Hormuz on fire** — Iran: three tankers hit mines in the Strait of
   Hormuz; Tehran vows to resist the US naval blockade.
2. **Huang is back** — Nvidia reinstates Jensen Huang as CEO after Trump
   intervenes; shares +31%, Nasdaq +7%.
3. **Russia pounds Ukraine** — overnight strikes hit homes in Zaporizhzhia:
   two killed, 40 wounded; 15 dead near Kyiv.

## How it is built

`render.py` draws `entry.png` (1024×1024, deterministic, PIL only — no
network, no randomness, no timestamps). `main.ts` (Node 22, standard library
only) copies `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`). Run it with:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

See `CAPTION.md` for all 45 stories with their sources.
