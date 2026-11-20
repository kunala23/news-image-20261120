#!/usr/bin/env python3
"""Hand the finished front page to the grader.

The newspaper image ships in this repository as entry.png. This program
only verifies it is a genuine PNG of a sane size, then copies it into
the output directory the grader reads (MAKEFUN_OUTPUT_DIR, or ./out).
"""

import os
import shutil
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def complain(message):
    print(f"entry: {message}", file=sys.stderr)
    return 1


def find_image():
    folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(folder, "entry.png")


def inspect(path):
    if not os.path.isfile(path):
        return f"no image found at {path}"
    size = os.path.getsize(path)
    if size <= 0 or size > MAX_BYTES:
        return f"image is {size} bytes, expected 1..{MAX_BYTES}"
    with open(path, "rb") as handle:
        prefix = handle.read(len(PNG_SIGNATURE))
    if prefix != PNG_SIGNATURE:
        return "image does not begin with the PNG magic bytes"
    return None


def verify_copy(source, target):
    if os.path.getsize(target) != os.path.getsize(source):
        return "copied file size does not match the source"
    with open(target, "rb") as handle:
        prefix = handle.read(len(PNG_SIGNATURE))
    if prefix != PNG_SIGNATURE:
        return "copied file does not begin with the PNG magic bytes"
    return None


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    out_dir = args[0] if args else os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    source = find_image()
    problem = inspect(source)
    if problem:
        return complain(problem)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    problem = verify_copy(source, target)
    if problem:
        return complain(problem)
    print(f"entry: wrote {target} ({os.path.getsize(target)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
