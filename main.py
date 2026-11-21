#!/usr/bin/env python3
"""Entry for news-image-20261121: copy the front page to /output/entry.png.

The image (news.png) is drawn by draw_news.py at build time and shipped
in this repository. This program only copies it, so both grader runs
write identical bytes. Standard library only, no network.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    src = os.path.join(here, "news.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("news.png is missing from the repository")
    if os.path.getsize(src) > 1048576:
        raise SystemExit("news.png is over the 1 MiB gate limit")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
