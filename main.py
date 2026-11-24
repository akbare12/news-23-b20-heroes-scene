#!/usr/bin/env python3
"""Copy entry.png to MAKEFUN_OUTPUT_DIR/entry.png.

The grader runs this program with /bot read-only and a writable
MAKEFUN_OUTPUT_DIR, so the program must never write next to itself:
the only output is os.environ["MAKEFUN_OUTPUT_DIR"]/entry.png
(default "out" for local runs).
"""
import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1_048_576


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def main():
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    w, h = png_size(dst)
    if (w, h) != (1024, 1024):
        print(f"bad size {w}x{h}, expected 1024x1024", file=sys.stderr)
        return 1
    if os.path.getsize(dst) > MAX_BYTES:
        print(f"output too large: {os.path.getsize(dst)} bytes", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        src_sha = hashlib.sha256(f.read()).hexdigest()
    with open(dst, "rb") as f:
        dst_sha = hashlib.sha256(f.read()).hexdigest()
    if src_sha != dst_sha:
        print("sha256 mismatch", file=sys.stderr)
        return 1
    print(f"OK {dst} {w}x{h} {os.path.getsize(dst)} bytes sha256={dst_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
