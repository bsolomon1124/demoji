#!/usr/bin/env python3

"""Download emoji data to package data.

Run from the project root: `uv run scripts/download_codes.py`.
Refreshes `src/demoji/codes.json` and the `_LDT` timestamp in the package.
"""

from __future__ import annotations

import datetime
import json
import pathlib
import re
import time
import urllib.request

from demoji import URL

ROOT = pathlib.Path(__file__).parent.parent.resolve()
PACKAGE_DIR = ROOT / "src" / "demoji"
CACHEPATH = PACKAGE_DIR / "codes.json"
MODULEPATH = PACKAGE_DIR / "__init__.py"


def download_codes(dest: pathlib.Path = CACHEPATH) -> None:
    codes = dict(stream_unicodeorg_emojifile(URL))
    _write_codes(codes, dest)


def _write_codes(codes: dict[str, str], dest: pathlib.Path) -> None:
    print(f"Writing emoji data to {dest} ...")
    with dest.open("w", encoding="utf-8") as f:
        json.dump(codes, f, separators=(",", ":"), ensure_ascii=False)
        f.write("\n")
    print("... OK")


def stream_unicodeorg_emojifile(url: str = URL):
    for codes, desc in _raw_stream_unicodeorg_emojifile(url):
        if ".." in codes:
            for cp in parse_unicode_range(codes):
                yield cp, desc
        else:
            yield parse_unicode_sequence(codes), desc


def parse_unicode_sequence(string: str) -> str:
    return "".join(chr(int(i.zfill(8), 16)) for i in string.split())


def parse_unicode_range(string: str):
    start, _, end = string.partition("..")
    start_i, end_i = (int(i.zfill(8), 16) for i in (start, end))
    return (chr(i) for i in range(start_i, end_i + 1))


def _raw_stream_unicodeorg_emojifile(url: str):
    print(f"Downloading emoji data from {url} ...")
    start = time.monotonic()
    with urllib.request.urlopen(url) as resp:
        body = resp.read().decode("utf-8")
    print(f"... OK (Got response in {time.monotonic() - start:.2f} seconds)")

    for line in body.splitlines():
        if not line or line.startswith("#"):
            continue
        codes, _, rest = line.partition(";")
        _, _, after_hash = rest.partition("#")
        # after_hash looks like: " 😀 E1.0 grinning face"
        parts = after_hash.strip().split(" ", 2)
        if len(parts) < 3:
            continue
        desc = parts[-1]
        yield codes.strip(), desc.strip()


def replace_lastdownloaded_timestamp() -> None:
    text = MODULEPATH.read_text(encoding="utf-8")
    now = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)
    ldt_re = re.compile(r"^_LDT = .*?(?:\n\s+.*?)*\)\s*(?:#.*)?$", re.M)
    replacement = f"_LDT = {now!r}  # noqa: E501"
    new_text, n = ldt_re.subn(replacement, text, count=1)
    if n != 1:
        raise RuntimeError("Failed to locate _LDT assignment to update")
    MODULEPATH.write_text(new_text, encoding="utf-8")
    print(f"Replaced timestamp with {now!r} in {MODULEPATH}")


if __name__ == "__main__":
    download_codes()
    replace_lastdownloaded_timestamp()
