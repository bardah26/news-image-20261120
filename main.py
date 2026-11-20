#!/usr/bin/env python3
"""news-image-20261120 — copy the bundled newspaper front page to output.

The entry image (entry.png) sits next to this script. This program copies
it byte-for-byte into the output directory (OUTPUT_DIR, default /output)
as entry.png. Deterministic: identical bytes on every run.

Rules honoured here:
- Python 3.13, standard library only, no network access.
- Never delete the output directory itself; only create it if missing.
- Reject the entry if it is larger than 1 MiB.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576  # 1 MiB limit for the entry image


def _source_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main() -> int:
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    # Create the output directory if missing; never remove it or its parent.
    os.makedirs(output_dir, exist_ok=True)

    source = _source_path()
    if not os.path.isfile(source):
        print(f"error: entry.png not found next to main.py ({source})",
              file=sys.stderr)
        return 1

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1

    dest = os.path.join(output_dir, "entry.png")
    shutil.copyfile(source, dest)

    digest = hashlib.sha256()
    with open(dest, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)

    print(f"entry.png: {size} bytes, sha256={digest.hexdigest()}")
    print(f"wrote {dest} (deterministic copy, byte-identical every run)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
