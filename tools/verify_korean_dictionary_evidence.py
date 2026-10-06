#!/usr/bin/env python3
"""Replay Korean inventory coordinates in the pinned external dictionary TSV.

This checks evidence identity and catalogue occurrence, not linguistic acceptance.
It does not generate or change translations. See the 2026-10-06 Korean recheck.
"""

import argparse
import csv
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
STDICT_SHA256 = "4e3796dfc85a16345b7c4395d89f68e23a5606fd03f62da5d197c77dc75c438a"
# The original inventory identifies these as compositions or synonym choices,
# rather than exact dictionary headwords. In particular 다시 is NOT read 재.
EDITORIAL_COMPONENTS = {
    ("다시 실행", "再實行"): ((27646, "재", "再"), (71281, "실행", "實行")),
    ("무손실", "無損失"): ((140878, "무", "無"), (100452, "손실", "損失")),
    ("미배치", "未配置"): ((114740, "미", "未"), (222169, "배치", "配置")),
    ("배경색", "背景色"): ((182042, "배경", "背景"), (187615, "색", "色")),
    ("전경색", "前景色"): ((33281, "전경", "前景"), (187615, "색", "色")),
    ("회색조", "灰色調"): ((140166, "회색", "灰色"), (203446, "조", "調")),
}


def catalogue(locale):
    path = ROOT / "Paintroid/src/main/res" / ("values-" + locale) / "strings.xml"
    return {e.get("name"): "".join(e.itertext()) for e in ET.parse(path).getroot()
            if e.tag in ("string", "plurals")}


def verify(path):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != STDICT_SHA256:
        raise ValueError("Dictionary hash differs from the pinned snapshot")
    lines = raw.decode("utf-8").splitlines()
    korean, mixed = catalogue("b+ko+KR"), catalogue("b+ko+Kore+KR")
    with (ROOT / "translations/KOREAN_HANJA_REVIEW.tsv").open(
            encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    seen, exact, editorial = set(), 0, 0

    def check_line(number, hangul, hanja):
        actual = lines[number - 1].split("\t")[:2]
        if actual != [hanja, hangul]:
            raise ValueError(f"Dictionary line {number}: expected {hanja}/{hangul}; {actual}")

    for row in rows:
        pair = row["hangul"], row["hanja"]
        if pair in seen:
            raise ValueError(f"Duplicate inventory pair: {pair}")
        seen.add(pair)
        if row["evidence"].startswith("stdict.tsv:"):
            check_line(int(row["evidence"].split(":")[1]), *pair)
            exact += 1
        else:
            if pair not in EDITORIAL_COMPONENTS:
                raise ValueError(f"Unspecified editorial evidence: {pair}")
            for number, hangul, hanja in EDITORIAL_COMPONENTS[pair]:
                if f"({number})" not in row["evidence"]:
                    raise ValueError(f"Changed component coordinate: {row}")
                check_line(number, hangul, hanja)
            editorial += 1
        key = row["example_resource"]
        if pair[0] not in korean.get(key, "") or pair[1] not in mixed.get(key, ""):
            raise ValueError(f"Inventory example is absent from the current catalogue: {row}")

    print(f"Mechanically verified {exact} exact dictionary rows and component rows "
          f"for {editorial} editorial choices; {len(rows)} current XML examples found.")
    print("This is lexical-coordinate evidence, not corpus attestation or semantic acceptance.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stdict_tsv", type=Path, help="Downloaded pinned stdict.tsv")
    verify(parser.parse_args().stdict_tsv)
