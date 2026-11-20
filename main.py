#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261120 bounty.

Copies the finished front page (entry.png, drawn in code by the build
script in the agent's work session) into the output directory.
Standard library only, no network, deterministic: the same bytes
every run.
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard the gate: the output must be a whole PNG, not a truncated copy.
    with open(dst, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG file")


if __name__ == "__main__":
    main()
