#!/usr/bin/env python3
"""Copy the front-page image into the entry output directory.

Reads news.png from beside this script and writes it as entry.png in the
directory named by MAKEFUN_OUTPUT_DIR (default /output). Refuses files
over 1 MiB. Copying bytes unchanged means repeated runs are byte-identical.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news.png")
MAX_BYTES = 1024 * 1024


def output_dir():
    """Resolve the destination directory from the environment."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    dest_dir = output_dir()
    if not os.path.isfile(SOURCE):
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"error: {SOURCE} is {size} bytes, over the "
              f"{MAX_BYTES}-byte limit", file=sys.stderr)
        return 1
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    copied = os.path.getsize(dest)
    if copied != size:
        print(f"error: copied {copied} bytes, expected {size}",
              file=sys.stderr)
        return 1
    print(f"wrote {dest}: {size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
