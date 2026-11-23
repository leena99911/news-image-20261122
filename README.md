# The World in One Day — 22 November 2026

A newspaper front page that sums up Sunday 22 November 2026 in a single
1024×1024 image: the COP31 collapse in Antalya leads, with the Hormuz
tanker mines and the Democrats' historic House majority below it, then
three columns of dated items covering the Middle East, Ukraine, Europe,
Asia-Pacific, the Americas and the wider world. Every story was first
reported on 22 November 2026 (UTC).

## Files

- `entry.png` — the finished front page (1024×1024 PNG).
- `build_image.py` — draws `entry.png` from scratch with PIL (DejaVu
  fonts). Run it to regenerate the image.
- `main.py` — the make.fun entry point: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

## Run

```sh
python3 build_image.py   # regenerate entry.png
python3 main.py          # copy it to /output/entry.png
```

Python 3, stdlib only (plus Pillow for the builder). No network, no
randomness — repeated runs are byte-identical.
