#!/usr/bin/env python3
"""make.fun entry: "Sum up 22 November's world news in one image".

Copies the pre-built front-page image (entry.png, sitting beside this
script) to $MAKEFUN_OUTPUT_DIR/entry.png. Stdlib only, no network,
deterministic: running it twice produces byte-identical output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"copied {SRC} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
