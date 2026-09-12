#!/usr/bin/env python3
"""Inspect the exact removed upstream fonts; emit metadata, never font binaries.

Requires fonttools. This is a provenance investigation, not a build dependency
or a licence grant. Font data exists only in memory and is not added to the APK,
source archive or CI artifacts.
"""

import argparse
import hashlib
import io
import json
from pathlib import Path
import urllib.request

from fontTools.ttLib import TTFont


REVISION = "853ce3c346910ea73aa4de5514f2a76ace1396fb"
FILES = {
    "dubai.ttf": ("9d9cea18ffa0cdf7b659da4c2460d9e63c42e944", 181484),
    "stc_regular.otf": ("efb515fd324deec591e750d5d8273d32d8bf6b9f", 21448),
}
NAME_IDS = {
    0: "copyright", 1: "family", 2: "subfamily", 3: "unique_identifier",
    4: "full_name", 5: "version", 6: "postscript_name", 7: "trademark",
    8: "manufacturer", 9: "designer", 10: "description", 11: "vendor_url",
    12: "designer_url", 13: "licence_description", 14: "licence_url",
    16: "typographic_family", 17: "typographic_subfamily",
}


def inspect(filename, expected_blob, expected_size):
    path = "Paintroid/src/main/res/font/" + filename
    url = f"https://raw.githubusercontent.com/Catrobat/Paintroid/{REVISION}/{path}"
    request = urllib.request.Request(url, headers={"User-Agent": "AN-Paint-font-provenance-review"})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read(expected_size + 1)
    blob_sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if len(data) != expected_size or blob_sha != expected_blob:
        raise ValueError(f"{filename}: downloaded bytes do not match pinned upstream blob")
    names = []
    with TTFont(io.BytesIO(data)) as font:
        for record in font["name"].names:
            if record.nameID not in NAME_IDS:
                continue
            names.append({
                "name_id": record.nameID, "field": NAME_IDS[record.nameID],
                "platform_id": record.platformID, "encoding_id": record.platEncID,
                "language_id": record.langID, "text": record.toUnicode(),
            })
        os2 = font.get("OS/2")
        return {
            "upstream_path": path, "revision": REVISION, "source_url": url,
            "git_blob_sha1": blob_sha, "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": len(data), "sfnt_version": repr(font.sfntVersion),
            "os2_fsType": None if os2 is None else os2.fsType,
            "names": names,
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path("build/reports/legacy-font-metadata.json"))
    args = parser.parse_args()
    result = {
        "purpose": "Historical font identity and licence provenance review; fonts remain excluded",
        "embedding_bits_note": "fsType is technical metadata and does not replace the applicable licence/EULA",
        "fonts": [inspect(name, blob, size) for name, (blob, size) in FILES.items()],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote metadata for {len(result['fonts'])} pinned fonts to {args.output}; no font binaries saved")


if __name__ == "__main__":
    main()
